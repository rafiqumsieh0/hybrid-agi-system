from pip._vendor.distlib.compat import raw_input
from short_term_memory import STM


class Main:

    def __init__(self):
        self.stm = STM(item_expiration=7, max_num_items=10)
        self.ltm = self.stm.ltm
        self.start_program()

    # Starts the main program, initializes the STM and LTM modules.
    # Valid commands: learn, predict, quit/exit.
    def start_program(self):
        print("Program Started \n To learn, type: learn item1 item2 \n"
              " To predict, type: predict item \n To quit, type: quit or exit ")
        user_quit = False
        while not user_quit:
            user_input = raw_input("Enter Command : ")
            input_array = user_input.split(sep=" ")
            [command, *rest] = input_array

            if command == "predict":
                if len(rest) == 0:
                    print("Please provide at least a second argument for predict. For example: predict usa")
                    continue
                elif len(rest) == 1:
                    result = self.ltm.retrieve_item_using_connection(rest[0])
                    print("Result : {0}".format(result))
                elif len(rest) > 1:
                    result = self.ltm.retrieve_items_using_connection(rest)
                    print("Result : {0}".format(result))
            elif command == "learn":
                if len(rest) == 0:
                    print("Please provide at least a second argument for learn. For example:"
                          " learn capital usa washington")
                    continue
                for item in rest:
                    self.stm.add_item_from_input(item)
            elif command == "quit" or command == "exit":
                print("Exiting Program")
                self.ltm.close_sql_connection()
                user_quit = True
            else:
                print("Please type a valid command, to quit, type: quit or exit")


Main()


