# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter






# import json

# class AmazonScraperPipeline:
#     def process_item(self, item, spider):
#         # 1. Clean Images (Keep only High-Res URL strings)
#         if item.get('images'):
#             # Extract just the 'hiRes' link or fallback to 'large' if hiRes is missing
#             clean_images = [img.get('hiRes') or img.get('large') for img in item['images']]
#             item['images'] = ", ".join(filter(None, clean_images))

#         # 2. Clean Variant Data (Make it readable)
#         if item.get('variant_data'):
#             # Convert the dict to a string: "ASIN: [Size, Net, Color] | ASIN: ..."
#             readable_variants = [f"{asin}: {', '.join(specs)}" for asin, specs in item['variant_data'].items()]
#             item['variant_data'] = " | ".join(readable_variants)

#         # 3. Clean Stars (Convert '4.5 out of 5 stars' to '4.5')
#         if item.get('price'):
#             clean_price = item['price'].replace('$', '').replace(',', '').strip()
#             # If the price is just empty or only a dot, set to 0.0
#             if clean_price == "" or clean_price == ".":
#                 item['price'] = 0.0
#             else:
#                 try:
#                     item['price'] = float(clean_price)
#                 except ValueError:
#                     item['price'] = 0.0

#         # 2. FIX THE STARS (Final Decimal Check)
#         if item.get('stars'):
#             try:
#                 # Converts "4.5 out of 5 stars" -> 4.5
#                 item['stars'] = float(item['stars'].split(' ')[0])
#             except (ValueError, IndexError):
#                 item['stars'] = 0.0

#         return item




# import json
# import re

# class AmazonScraperPipeline:
#     def process_item(self, item, spider):
#         # 1. Clean Images: Extract URLs from the chompjs list
#         if item.get('images'):
#             clean_images = [img.get('hiRes') or img.get('large') for img in item['images']]
#             item['images'] = ", ".join(filter(None, clean_images))

#         # 2. Clean Variant Data: Transform the dictionary into a readable string
#         if item.get('variant_data') and isinstance(item['variant_data'], dict):
#             readable_variants = [f"{asin}: {', '.join(specs)}" for asin, specs in item['variant_data'].items()]
#             item['variant_data'] = " | ".join(readable_variants)

#         # 3. Clean Price: Convert "$1,299.00" -> 1299.0 (Float)
#         if item.get('price'):
#             clean_price = item['price'].replace('$', '').replace(',', '').strip()
#             if clean_price in ["", "."]:
#                 item['price'] = 0.0
#             else:
#                 try:
#                     item['price'] = float(clean_price)
#                 except ValueError:
#                     item['price'] = 0.0

#         # 4. Clean Stars: Convert "4.5 out of 5 stars" -> 4.5 (Float)
#         if item.get('stars'):
#             try:
#                 item['stars'] = float(item['stars'].split(' ')[0])
#             except (ValueError, IndexError):
#                 item['stars'] = 0.0

#         # 5. Clean Rating Count: Convert "1,245 ratings" -> 1245 (Integer)
#         if item.get('rating_count'):
#             # This regex finds only the digits in the string
#             numbers_only = re.sub(r'[^\d]', '', item['rating_count'])
#             try:
#                 item['rating_count'] = int(numbers_only)
#             except ValueError:
#                 item['rating_count'] = 0
#         else:
#             item['rating_count'] = 0

#         # 6. Clean Feature Bullets: Join list into one paragraph
#         if isinstance(item.get('feature_bullets'), list):
#             item['feature_bullets'] = " ".join(item['feature_bullets'])

#         return item




import json
import re
from scrapy.exceptions import DropItem

class AmazonScraperPipeline:
    def __init__(self):
        # Initialize a set to keep track of unique product URLs during the run
        self.seen_urls = set()

    def process_item(self, item, spider):
        # 1. DUPLICATE CHECK
        # Using URL as the unique ID to ensure we don't save the same product twice
        product_url = item.get('url')
        
        if product_url in self.seen_urls:
            raise DropItem(f"Duplicate product found and dropped: {product_url}")
        
        # If unique, add it to our set so we don't process it again
        self.seen_urls.add(product_url)

        # 2. Clean Images: Extract URLs from the chompjs list
        if item.get('images'):
            # Extract just the 'hiRes' link or fallback to 'large'
            clean_images = [img.get('hiRes') or img.get('large') for img in item['images']]
            item['images'] = ", ".join(filter(None, clean_images))

        # 3. Clean Variant Data: Transform the dictionary into a readable string
        if item.get('variant_data') and isinstance(item['variant_data'], dict):
            readable_variants = [f"{asin}: {', '.join(specs)}" for asin, specs in item['variant_data'].items()]
            item['variant_data'] = " | ".join(readable_variants)

        # 4. Clean Price: Convert "$1,299.00" -> 1299.0 (Float)
        if item.get('price'):
            clean_price = item['price'].replace('$', '').replace(',', '').strip()
            if clean_price in ["", "."]:
                item['price'] = 0.0
            else:
                try:
                    item['price'] = float(clean_price)
                except ValueError:
                    item['price'] = 0.0

        # 5. Clean Stars: Convert "4.5 out of 5 stars" -> 4.5 (Float)
        if item.get('stars'):
            try:
                item['stars'] = float(item['stars'].split(' ')[0])
            except (ValueError, IndexError):
                item['stars'] = 0.0

        # 6. Clean Rating Count: Convert "1,245 ratings" -> 1245 (Integer)
        if item.get('rating_count'):
            # This regex finds only the digits in the string
            numbers_only = re.sub(r'[^\d]', '', item['rating_count'])
            try:
                item['rating_count'] = int(numbers_only)
            except ValueError:
                item['rating_count'] = 0
        else:
            item['rating_count'] = 0

        # 7. Clean Feature Bullets: Join list into one paragraph
        if isinstance(item.get('feature_bullets'), list):
            item['feature_bullets'] = " ".join(item['feature_bullets'])

        return item