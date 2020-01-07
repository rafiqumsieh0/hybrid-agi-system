# Hybrid AGI system that combines neural networks with computer memory

This repository contains the code that was used in the paper I wrote on the Hybrid AGI system. It contains the following:  The program’s main entry file, the short-term memory module ( STM ), the long-term memory module (LTM ), Item’s model file, database constants db_constants file.

## Getting Started

### Prerequisites

1-) You will need to have a MySQL server instance either running on your machine or a remote one where you have the connection string. Edit this information in the db_constants.py file. Create a schema and call it : “ltm” . Then create a table called “items” and follow the structure in the pdf paper.

2-)You will also need to have a Redis Instance either locally or a remote one. Edit the corresponding information in the db_constants.py file.

3-)You will need a recent version of Python. The project was written in Python 3.7 but you might be able to run it with a lower version. You will need to install some Python packages to handle databases: mysqlclient, sqlalchemy, py-redis, and possibly more Python packages and dependencies. If you are using PyCharm, it should tell you what you need to install.

### Installing

Just download the zip file and extract the content into a Python directory of your choice. Run the main file and you should get results for the default network settings.


### Usage

Try running : learn Hello Moto
Then run: predict Hello
It should output : Moto

## Experimenting with the model

Feel free to change the code in the LTM and STM modules to alter their behaviors. You can also add/integrate a feature extracting layer prior to sending anything to LTM and STM. So far, the system can only learn text separated by spaces. Keep in mind that the model will probably need a lot of data before it starts showing any useful results.

## Built With

* [Miniconda](http://anaconda.com)
* [MySQL]
* [Redis]

## Contributing

Please message me if you want to contribute to this project.

## Authors

* **Rafi Qumsieh** - *Initial work* - (https://github.com/rafiqumsieh0)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Thanks to everyone who provided the libraries needed to complete this project.

