# Project Title

Maple

## Getting Started

Run main.py to do following things:
-Get data from given url.
-Write it to mongodb.
-Get most used words and creates two plot for it(one is most used 10 words the other one is adjectives is given with different color).
-Write most used words to mongodb.
-Log timeouts,connection errors and encoding errors.

### Prerequisites

You need to have following python libraries to run project
-requests
-BeautifulSoup
-threading
-pymongo
-logging
-matplotlib

You need to have a database named ayberk_deringoz and also have 2 collections named news,word_frequency

### Usage Instructions
Go to the project directory
run main.py

Instructions for Data Manipulation:
-Go to the project directory
-Run python PrintNews.py on terminal
-Prints all data stored in news collection, does not removes unnecessary data since the needs is not implemented in document.


## Missing Features
The project does not contain stats written in mongodb that are given in documentation.

Sleep method can be added to prevent Connection Errors but increases running time.

## Python Version
3.9.12

## Authors

* **Ayberk Deringöz** - *Initial work* - [Maple](https://github.com/ayberkderingoz/Maple)

