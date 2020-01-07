import redis
import time
from long_term_memory import LTM
from db_constants import REDIS_INFO

"""Short-term memory module. Is initialized with:
 1-) item_expiration: An item expiration property that determines the number of seconds that
each item lives in the STM before it expires.
 2-) max_num_items: The maximum number of items that can exist in the STM at any given moment. """


class STM(object):
    # Initialize the STM object
    def __init__(self, item_expiration=7, max_num_items=10):
        # Connect to Redis
        try:
            pool = redis.ConnectionPool(host=REDIS_INFO["ip"], port=REDIS_INFO["port"], db=0)
            self.redis = redis.Redis(connection_pool=pool)
        except IOError:
            print("Error connecting to redis")
        # If connected, initialize the long term memory.
        finally:
            self.item_expiration = item_expiration
            self.max_num_items = max_num_items
            self.ltm = LTM()

    # Add an item that is received from the input layer to the STM along with the current timestamp as its entry time.
    def add_item_from_input(self, item):
        item_time = time.time()
        self.trim_items_in_stm()
        stored = self.redis.set(name=str(item_time), value=item, ex=self.item_expiration)
        if stored:
            self.send_items_to_ltm()
            return True
        return False

    # Trim/Remove the oldest items in the STM if the number of items exceeds max_num_items
    def trim_items_in_stm(self):
        all_keys = self.redis.keys()
        if all_keys is not None and len(all_keys) > self.max_num_items:
            all_keys_float = [float(key) for key in all_keys]
            sorted(all_keys_float)
            oldest_key_float = all_keys_float[0]
            oldest_key_string = str(oldest_key_float)
            self.redis.delete(oldest_key_string)

    # Add an item to the STM
    def add_item(self, item):
        item_time = time.time()
        status = self.redis.set(name=str(item_time), value=item, ex=self.item_expiration)
        if status == "OK":
            return True
        return False

    # Get all items in the STM, and send them to the LTM
    def send_items_to_ltm(self):
        items = []
        all_keys = self.redis.keys()
        for timestamp1 in all_keys:
            item1 = self.redis.get(timestamp1)
            for timestamp2 in all_keys:
                item2 = self.redis.get(timestamp2)
                if timestamp1 != timestamp2:
                    items.append((item1, item2, abs(float(timestamp1) - float(timestamp2))))
        if len(items) > 0:
            self.ltm.store_items(items)
        # DELETE ALL ITEMS
        # self.redis.delete()

    # Receives items from LTM and stores them in STM. This usually happens after recalling a memory from the LTM.
    def store_items_from_ltm(self, items_tuple):
        item_row = self.ltm.get_items_using_connection(items_tuple)
        if item_row:
            item1, item2, last_updated, score = item_row
            self.add_item(item2)



