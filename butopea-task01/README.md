# Introduction
This code is designed to generate a product feed in **XML** format based on data stored in a **SQLite** database. The generated product feed follows the specifications provided by **Google Merchants** for product data.

# Requirements
- `Python 3.6` or higher

# Setup

Not required since the code uses only built-in modules.

# Running the Code
To run the code and generate the product feed, follow these steps:

1. Make sure the SQLite database file (data.sqlite) is located in the same directory as the code files.
2. Navigate to the directory containing the code files.
   ```shell
   cd butopea-task01
   ```
3. Run the following command: 
    ```shell
    python3 main.py
    ```
    or
    ```shell
    python main.py
    ```
4. The product feed will be generated in the same directory as the code files and will be named `feed.xml`.
   
# Code explanation
## Db Class
The `Db` class provides methods for interacting with the **SQLite** database. This class uses `sqlite3` module for SQL queries, which is not my personal preference but more than enough for provided task.

It includes functions to fetch products, product data, product images, and manufacturer information.

## XMLGenerator Class
The `XMLGenerator` class is responsible for generating the XML product feed. It uses the `lxml` module to generate the XML.

It takes product data, product images, and manufacturer information as input and creates the XML according to the specifications provided by **Google Merchants**.

## ProductFeedGenerator Class
The `ProductFeedGenerator` class coordinates the generation of the product feed. It retrieves the necessary data from the database using the `Db` class and passes it to the `XMLGenerator` class to generate the XML feed for each product and then to save the generated XML to a file.

## Main Execution
The main execution block at the end of the code initializes the `Db`, `XMLGenerator`, and `ProductFeedGenerator` objects. It then calls the `generate_product_feed` method of the `ProductFeedGenerator` object to generate the product feed.


# Sources
- [Google Merchants: Product data specification](https://support.google.com/merchants/answer/7052112)
- [RSS 2.0 Specification](https://support.google.com/merchants/answer/160589)
