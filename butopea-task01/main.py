import os
import sqlite3
from typing import List, NamedTuple, Union
import xml.etree.ElementTree as ET

DB_NAME = "data.sqlite"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_NAME)

BASE_URL = "https://butopea.com/"


# I do know about dataclasses and collections.namedtuple, but I've decided to
# use NamedTuple for the sake of consistency.
class Product(NamedTuple):
    id: int
    image_link: str
    price: float
    manufacturer_id: int


class ProductData(NamedTuple):
    name: str
    description: str


class Manufacturer(NamedTuple):
    name: str


class Image(NamedTuple):
    image_link: str


# I was not sure if you'd rather want me to do single SQL query with JOINs
# or use ORM, so I've decided to do it the Python way :)
class Db:
    """Database class for fetching data from the provided db."""

    def __init__(self, db_name: str) -> None:
        """Initialize the database connection and cursor."""
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def fetch_products(
        self, only_active: bool = True
    ) -> Union[List[Product], List]:
        """
        Fetch all products from the database. By default only active products
        are returned.
        """
        if only_active:
            self.cursor.execute("SELECT * FROM product WHERE status = '1'")
        else:
            self.cursor.execute("SELECT * FROM product")

        rows = self.cursor.fetchall()
        products = []
        for row in rows:
            products.append(
                Product(
                    id=row[0],
                    image_link=row[4],
                    price=row[6],
                    manufacturer_id=row[5],
                )
            )
        return products

    def fetch_product_data(self, product_id: int) -> Union[ProductData, None]:
        """Fetch product data from the database by product id."""
        self.cursor.execute(
            "SELECT * FROM product_description WHERE product_id = ?",
            (product_id,),
        )
        row = self.cursor.fetchone()
        if not row:
            return None
        return ProductData(name=row[1], description=row[2])

    def fetch_product_images(
        self, product_id: int
    ) -> Union[List[Image], List]:
        """Fetch product images from the database by product id."""
        self.cursor.execute(
            "SELECT * FROM product_image WHERE product_id = ? ORDER BY sort_order ASC",
            (product_id,),
        )
        rows = self.cursor.fetchall()
        images = []
        for row in rows:
            images.append(Image(image_link=row[2]))
        return images

    def fetch_manufacturer(
        self, manufacturer_id: int
    ) -> Union[Manufacturer, None]:
        """Fetch manufacturer from the database by manufacturer id."""
        self.cursor.execute(
            "SELECT * FROM manufacturer WHERE manufacturer_id = ?",
            (manufacturer_id,),
        )
        row = self.cursor.fetchone()
        if not row:
            return None
        return Manufacturer(name=row[1])

    def close(self) -> None:
        """Close the database connection."""
        self.conn.close()


class XMLGenerator:
    """XML generator class for generating the product feed."""

    def __init__(self) -> None:
        # Create base structure according to the Google Merchant Center documentation
        self.root = ET.Element(
            "rss",
            {
                "xmlns:g": "http://base.google.com/ns/1.0",
                "version": "2.0",
            },
        )
        self.channel = ET.SubElement(self.root, "channel")

    def generate_product_feed(
        self,
        product: Product,
        product_data: ProductData,
        product_images: Union[List[Image], List],
        manufacturer: Manufacturer,
    ) -> None:
        """Generate product feed for a single product."""

        # Create the product element and add the required fields with tags
        # according to the Google Merchant Center documentation
        product_element = ET.SubElement(self.channel, "item")
        # probably should've used dicts or dataclasses for this, but this already looks
        ET.SubElement(product_element, "g:id").text = str(product.id)
        ET.SubElement(product_element, "g:title").text = product_data.name
        ET.SubElement(
            product_element, "g:description"
        ).text = product_data.description
        ET.SubElement(
            product_element, "g:link"
        ).text = f"{BASE_URL}{product.id}"
        ET.SubElement(
            product_element, "g:image_link"
        ).text = f"{BASE_URL}{product.image_link}"

        if product_images:
            # Google Merchant Center only accepts 10 images per product
            if len(product_images) > 10:
                product_images = product_images[:10]
            for img in product_images:
                ET.SubElement(
                    product_element, "g:additional_image_link"
                ).text = f"{BASE_URL}{img.image_link}"

        ET.SubElement(product_element, "g:availability").text = "in_stock"
        price = round(float(product.price))
        ET.SubElement(product_element, "g:price").text = f"{price} HUF"
        ET.SubElement(product_element, "g:brand").text = manufacturer.name
        ET.SubElement(product_element, "g:condition").text = "new"

    def write_to_file(self) -> None:
        """Write the generated XML to file."""
        tree = ET.ElementTree(self.root)
        tree.write("feed.xml", encoding="utf-8", xml_declaration=True)


class ProductFeedGenerator:
    """Class that puts together the database and XML generator."""

    def __init__(self, database: Db, xml_generator: XMLGenerator) -> None:
        self.database = database
        self.xml_generator = xml_generator

    def generate_product_feed(self) -> None:
        """Generate the product feed."""
        # Fetch all products from the database
        products = self.database.fetch_products()

        # Add each product to the XML feed
        for product in products:
            product_data = self.database.fetch_product_data(product.id)
            product_images = self.database.fetch_product_images(product.id)
            manufacturer = self.database.fetch_manufacturer(
                product.manufacturer_id
            )
            if not product_data or not manufacturer:
                continue
            self.xml_generator.generate_product_feed(
                product, product_data, product_images, manufacturer
            )

        # Write the generated XML to file and close the database connection
        self.xml_generator.write_to_file()
        self.database.close()


if __name__ == "__main__":
    database = Db(DB_PATH)
    xml_generator = XMLGenerator()
    generator = ProductFeedGenerator(database, xml_generator)
    generator.generate_product_feed()
