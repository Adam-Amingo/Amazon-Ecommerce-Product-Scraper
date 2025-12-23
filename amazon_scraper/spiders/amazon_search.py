# import json
# import scrapy
# from urllib.parse import urljoin
# import re


# class AmazonSearchSpider(scrapy.Spider):
#     name = "amazon_search"
#     allowed_domains = ["amazon.com" , "proxy.scrapeops.io"]
    

#     def start_requests(self):
#         keyword_list = ['ipad']
#         for keyword in keyword_list:
#             amazon_search_url = f"https://www.amazon.com/s?k={keyword}&page=1"
#             yield scrapy.Request(url = amazon_search_url , callback = self.discover_product_urls , meta = {'keyword' : keyword , 'page' : 1}, dont_filter=True)

#     def discover_product_urls(self , response):
#         page = response.meta['page']
#         keyword = response.meta['keyword']

#         ##Get all pages 
#         if page == 1 :
#             available_pages = response.xpath(
#                  '//*[contains(@class, "s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
#             ).getall()
            
#             last_page = available_pages[-1]

#             for page_num in range(2, int(last_page) + 1):
#                 amazon_search_url = f"https://www.amazon.com/s?k={keyword}&page={page_num}"
#                 yield scrapy.Request(url = amazon_search_url , callback = self.parse_product_data , meta = {'keyword' : keyword , 'page':page_num})
        

#     def parse_product_data(self, response):
#         # 1. Robust Image Extraction
#         image_data = []
#         try:
#             # We search for the image block without relying on the exact newline at the end
#             raw_image_data = re.findall(r"colorImages':.*'initial':\s*(\[.+?\])}", response.text)
#             if raw_image_data:
#                 image_data = json.loads(raw_image_data[0])
#         except Exception as e:
#             self.logger.warning(f"Could not extract images for {response.url}: {e}")

#         # 2. Robust Variant Extraction
#         variant_data = []
#         try:
#             raw_variants = re.findall(r'dimensionValuesDisplayData"\s*:\s*({.+?}),', response.text)
#             if raw_variants:
#                 variant_data = json.loads(raw_variants[0])
#         except:
#             pass

#         # 3. Clean CSS selectors
#         feature_bullets = [bullet.strip() for bullet in response.css("#feature-bullets li ::text").getall() if bullet.strip()]
        
#         price = response.css('.a-price span[aria-hidden="true"] ::text').get("")
#         if not price:
#             price = response.css('.a-price .a-offscreen ::text').get("")

#         product_data = {
#             "name": response.css("#productTitle::text").get("").strip(),
#             "price": price,
#             "stars": response.css("i[data-hook=average-star-rating] ::text").get("").strip(),
#             "feature_bullets": feature_bullets,
#             "images": image_data,
#             "variant_data": variant_data,
#             "url": response.url
#         }
    
#         yield product_data
    # def parse_product_data(self, response):
    #     image_data = json.loads(re.findall(r"colorImages':.*'initial':\s*(\[.+?\])},\n", response.text)[0])
    #     variant_data = re.findall(r'dimensionValuesDisplayData"\s*:\s* ({.+?}),\n', response.text)
    #     feature_bullets = [bullet.strip() for bullet in response.css("#feature-bullets li ::text").getall()]
    #     price = response.css('.a-price span[aria-hidden="true"] ::text').get("")
    #     if not price:
    #         price = response.css('.a-price .a-offscreen ::text').get("")

    #     product_data = {
    #         "name": response.css("#productTitle::text").get("").strip(),
    #         "price": price,
    #         "stars": response.css("i[data-hook=average-star-rating] ::text").get("").strip(),
    #         "rating_count": response.css("div[data-hook=total-review-count] ::text").get("").strip(),
    #         "feature_bullets": feature_bullets,
    #         "images": image_data,
    #         "variant_data": variant_data,
    #     }
    
    #     # Print the data before yielding
    #     self.logger.info(f"Scraped Data: {product_data}")
    #     print(product_data)
    #     yield product_data



# curl https://proxy.scrapeops.io/v1/?api_key=088af6a6-6911-4481-aa7b-5e7a7b102453&url=https://amazon.com
# curl "https://proxy.scrapeops.io/v1/?api_key=088af6a6-6911-4481-aa7b-5e7a7b102453&url=https://www.amazon.com/dp/B08264XDKC" > amazon_page.html

# import json
# import scrapy
# from urllib.parse import urljoin
# import re

# class AmazonSearchSpider(scrapy.Spider):
#     name = "amazon_search"
#     allowed_domains = ["amazon.com", "proxy.scrapeops.io"]

#     def start_requests(self):
#         keyword_list = ['ipad']
#         for keyword in keyword_list:
#             amazon_search_url = f"https://www.amazon.com/s?k={keyword}&page=1"
#             yield scrapy.Request(
#                 url=amazon_search_url, 
#                 callback=self.discover_product_urls, 
#                 meta={'keyword': keyword, 'page': 1},
#                 dont_filter=True
#             )

#     def discover_product_urls(self, response):
#         # FIND THE PRODUCTS
#         # This selector targets the actual product containers on the search page
#         products = response.css("div.s-result-item[data-component-type=s-search-result]")
        
#         self.logger.info(f"FOUND {len(products)} PRODUCTS ON PAGE {response.meta['page']}")

#         for product in products:
#             relative_url = product.css("h2 a::attr(href)").get()
#             if relative_url:
#                 # BUILD THE BRIDGE: Move from search results to the actual product page
#                 product_url = urljoin('https://www.amazon.com/', relative_url)
#                 yield scrapy.Request(
#                     url=product_url, 
#                     callback=self.parse_product_data
#                 )

#         # PAGINATION
#         page = response.meta['page']
#         if page == 1:
#             # Look for the last page number in the pagination bar
#             available_pages = response.css('span.s-pagination-item.s-pagination-disabled::text').getall()
#             if available_pages:
#                 last_page = int(available_pages[-1])
#                 for page_num in range(2, last_page + 1):
#                     next_url = f"https://www.amazon.com/s?k={response.meta['keyword']}&page={page_num}"
#                     yield scrapy.Request(
#                         url=next_url, 
#                         callback=self.discover_product_urls, 
#                         meta={'keyword': response.meta['keyword'], 'page': page_num}
#                     )
#     def parse_product_data(self, response):
#         # IMAGE EXTRACTION
#         raw_images = re.findall(r"colorImages':.*'initial':\s*(\[.+?\])}", response.text)
#         image_json = json.loads(raw_images[0]) if raw_images else []

#         # PRICE EXTRACTION (Better way to handle fractional prices)
#         whole = response.css('.a-price-whole::text').get("")
#         fraction = response.css('.a-price-fraction::text').get("")
        
#         full_price = f"${whole.replace('.', '')}.{fraction}" if whole else "N/A"

#         yield {
#             "name": response.css("#productTitle::text").get("").strip(),
#             "price": full_price,
#             "url": response.url,
#             "image_count": len(image_json)
#         }

    # def parse_product_data(self, response):
    #     # We are now on a SINGLE product page. No try-except here. 
    #     # If these fail, we want to see the error.
        
    #     # IMAGE EXTRACTION
    #     # This Regex looks for the initial image set inside the script tag
    #     raw_images = re.findall(r"colorImages':.*'initial':\s*(\[.+?\])}", response.text)
    #     image_json = json.loads(raw_images[0]) if raw_images else []

    #     # PRICE EXTRACTION
    #     # Amazon is tricky; we try the most common selector
    #     price = response.css('.a-price-whole::text').get("") + response.css('.a-price-fraction::text').get("")

    #     yield {
    #         "name": response.css("#productTitle::text").get("").strip(),
    #         "price": f"${price}" if price else "N/A",
    #         "url": response.url,
    #         "image_count": len(image_json)
    #     }



# import json
# import scrapy
# from urllib.parse import urljoin
# import re

# class AmazonSearchSpider(scrapy.Spider):
#     name = "amazon_search"
    
#     # We leave this empty because we disabled the middleware in settings
#     allowed_domains = [] 

#     def start_requests(self):
#         keyword = 'ipad'
#         url = f"https://www.amazon.com/s?k={keyword}&page=1"
#         # dont_filter=True is the key to bypassing internal Scrapy deduplication
#         yield scrapy.Request(
#             url=url, 
#             callback=self.discover_product_urls, 
#             meta={'keyword': keyword, 'page': 1},
#             dont_filter=True
#         )

#     def discover_product_urls(self, response):
#         # This will show up in your terminal if the proxy is working
#         self.logger.info(f"DEBUG: Processing Search Page {response.url}")
        
#         products = response.css("div.s-result-item[data-component-type=s-search-result]")
        
#         if not products:
#             self.logger.error("CRITICAL: No products found on page! The selectors might be wrong or Amazon sent a captcha.")
#             return

#         for product in products:
#             relative_url = product.css("h2 a::attr(href)").get()
#             if relative_url:
#                 product_url = urljoin('https://www.amazon.com/', relative_url)
#                 yield scrapy.Request(
#                     url=product_url, 
#                     callback=self.parse_product_data,
#                     dont_filter=True # Force Scrapy to follow the link
#                 )

#         # Pagination (Let's just test page 1 and 2 for now to be sure)
#         current_page = response.meta['page']
#         if current_page == 1:
#             next_url = f"https://www.amazon.com/s?k={response.meta['keyword']}&page=2"
#             yield scrapy.Request(
#                 url=next_url, 
#                 callback=self.discover_product_urls, 
#                 meta={'keyword': response.meta['keyword'], 'page': 2},
#                 dont_filter=True
#             )

#     def parse_product_data(self, response):
#         self.logger.info(f"DEBUG: Scraping Product: {response.url}")
        
#         # We use simple selectors first to prove it works
#         name = response.css("#productTitle::text").get("").strip()
#         price_whole = response.css('.a-price-whole::text').get("")
        
#         # Regex for images (The unfiltered version)
#         raw_images = re.findall(r"colorImages':.*'initial':\s*(\[.+?\])}", response.text)
        
#         item = {
#             "name": name,
#             "price": price_whole,
#             "url": response.url,
#             "has_images": bool(raw_images)
#         }
        
#         yield item



# import json
# import scrapy
# from urllib.parse import urljoin
# import re

# class AmazonSearchSpider(scrapy.Spider):
#     name = "amazon_search"
    
#     # We keep this empty because we disabled the OffsiteMiddleware in settings.py
#     allowed_domains = [] 

#     def start_requests(self):
#         # We start with a search for 'ipad'
#         url = "https://www.amazon.com/s?k=ipad&page=1"
        
#         # LAYER 3 SOLUTION: We tell ScrapeOps to render the JS so the page is 'fully baked'
#         yield scrapy.Request(
#             url=url, 
#             callback=self.discover_product_urls, 
#             meta={'render_js': True}, 
#             dont_filter=True
#         )

#     def discover_product_urls(self, response):
#         # LAYER 1 SOLUTION: Use a broad selector for links
#         # This finds every product 'front door' on the search page
#         links = response.css('a[href*="/dp/"]::attr(href)').getall()
#         product_urls = list(set([urljoin("https://www.amazon.com/", l.split("?")[0]) for l in links if "/dp/" in l]))
        
#         self.logger.info(f"SOP: Found {len(product_urls)} products to scrape.")

#         for url in product_urls:
#             # We follow each link and render the JS for the detail page too
#             yield scrapy.Request(
#                 url=url, 
#                 callback=self.parse_product_data,
#                 meta={'render_js': True},
#                 dont_filter=True
#             )

#     def parse_product_data(self, response):
#         # LAYER 1: CSS for the easy stuff (Title and Price)
#         # Using fallbacks in case Amazon is A/B testing layouts
#         name = response.css("#productTitle::text").get() or response.css(".a-size-large::text").get()
        
#         # We look for the 'hidden' offscreen price which is usually the most stable
#         price = response.css('.a-price .a-offscreen::text').get() or response.css('.a-price-whole::text').get()

#         # LAYER 2 SOLUTION: Regex for the 'Embedded JSON' (Images)
#         # We reach into the <script> tags to find the high-res image list
#         image_data = []
#         try:
#             # This regex captures the JSON array inside the JavaScript 'colorImages' block
#             raw_image_json = re.findall(r"colorImages':.*'initial':\s*(\[.+?\])}", response.text)
#             if raw_image_json:
#                 image_data = json.loads(raw_image_json[0])
#         except Exception as e:
#             self.logger.warning(f"Regex failed for images on {response.url}: {e}")

#         # CLEANUP: Prepare the final item
#         yield {
#             "name": name.strip() if name else "N/A",
#             "price": price if price else "N/A",
#             "images": image_data,
#             "url": response.url
#         }



















# import scrapy
# from urllib.parse import urljoin
# import re
# import chompjs # Make sure to pip install chompjs

# class AmazonSearchSpider(scrapy.Spider):
#     name = "amazon_search"
#     allowed_domains = [] 

#     keyword_list = ["ipad" , "laptop" , "gaming mouse"]

#     def start_requests(self):
#         url = "https://www.amazon.com/s?k=ipad&page=1"
#         yield scrapy.Request(
#             url=url, 
#             callback=self.discover_product_urls, 
#             meta={'render_js': True}, 
#             dont_filter=True
#         )

#     def discover_product_urls(self, response):
#         links = response.css('a[href*="/dp/"]::attr(href)').getall()
#         # Clean URLs to avoid duplicate tracking parameters
#         product_urls = list(set([urljoin("https://www.amazon.com/", l.split("?")[0]) for l in links if "/dp/" in l]))
        
#         self.logger.info(f"SOP: Found {len(product_urls)} products to scrape.")

#         for url in product_urls:
#             yield scrapy.Request(
#                 url=url, 
#                 callback=self.parse_product_data,
#                 meta={'render_js': True},
#                 dont_filter=True
#             )
#     def parse_product_data(self, response):
#         # --- 1. EXTRACT IMAGES (Using chompjs) ---
#         image_data = []
#         img_script = response.xpath("//script[contains(., 'colorImages')]/text()").get()
#         if img_script:
#             # We find the start of 'initial' and let chompjs find the end
#             img_match = re.search(r"'initial':\s*(\[.*)", img_script)
#             if img_match:
#                 try:
#                     image_data = chompjs.parse_js_object(img_match.group(1))
#                 except Exception:
#                     pass

#         # --- 2. EXTRACT VARIANTS (Using chompjs) ---
#         variant_data = {}
#         var_script = response.xpath("//script[contains(., 'dimensionValuesDisplayData')]/text()").get()
#         if var_script:
#             # We find the start of the object and let chompjs parse the nested structure
#             var_match = re.search(r'dimensionValuesDisplayData"\s*:\s*({.*)', var_script)
#             if var_match:
#                 try:
#                     variant_data = chompjs.parse_js_object(var_match.group(1))
#                 except Exception:
#                     pass

#         # --- 3. SCRAPE TEXT DATA (CSS Selectors) ---
#         feature_bullets = [bullet.strip() for bullet in response.css("#feature-bullets li ::text").getall() if bullet.strip()]
        
#         rating_count = response.css("span#acrCustomerReviewText::text").get() or \
#                    response.css("div[data-hook='total-review-count'] span::text").get() or \
#                    response.xpath("//span[contains(@class, 'a-size-base') and contains(text(), 'ratings')]/text()").get("")

#         # Price logic with your specific aria-hidden preference
#         price = response.css('.a-price span[aria-hidden="true"] ::text').get("")
        
#         # Premium Fallback: If price is missing, look in the 'twister' data (Variations)
#         if not price or price == "$":
#             # We look for the price embedded in the variation script
#             script_text = response.xpath("//script[contains(., 'dimensionValuesDisplayData')]/text()").get()
#             if script_text:
#                 # We search for any dollar amount pattern in the metadata
#                 found_price = re.search(r'"priceAmount":\s*(\d+\.\d+)', script_text)
#                 if found_price:
#                     price = found_price.group(1)

#         # --- 4. ASSEMBLE PRODUCT DATA ---
#         product_data = {
#             "name": response.css("#productTitle::text").get("").strip(),
#             "price": price,
#             "stars": response.css("i[data-hook=average-star-rating] ::text").get("").strip(),
#             "rating_count": rating_count,
#             "feature_bullets": feature_bullets,
#             "images": image_data,
#             "variant_data": variant_data,
#             "url": response.url
#         }

#         yield product_data





# import chompjs
# import re
# import json

# def parse_product_data(self, response):
#     # --- 1. EXTRACT IMAGES (Using chompjs) ---
#     image_data = []
#     img_script = response.xpath("//script[contains(., 'colorImages')]/text()").get()
#     if img_script:
#         # We find the start of 'initial' and let chompjs find the end
#         img_match = re.search(r"'initial':\s*(\[.*)", img_script)
#         if img_match:
#             try:
#                 image_data = chompjs.parse_js_object(img_match.group(1))
#             except Exception:
#                 pass

#     # --- 2. EXTRACT VARIANTS (Using chompjs) ---
#     variant_data = {}
#     var_script = response.xpath("//script[contains(., 'dimensionValuesDisplayData')]/text()").get()
#     if var_script:
#         # We find the start of the object and let chompjs parse the nested structure
#         var_match = re.search(r'dimensionValuesDisplayData"\s*:\s*({.*)', var_script)
#         if var_match:
#             try:
#                 variant_data = chompjs.parse_js_object(var_match.group(1))
#             except Exception:
#                 pass

#     # --- 3. SCRAPE TEXT DATA (CSS Selectors) ---
#     feature_bullets = [bullet.strip() for bullet in response.css("#feature-bullets li ::text").getall() if bullet.strip()]
    
#     # Price logic with your specific aria-hidden preference
#     price = response.css('.a-price span[aria-hidden="true"] ::text').get("")
#     if not price:
#         price = response.css('.a-price .a-offscreen ::text').get("")

#     # --- 4. ASSEMBLE PRODUCT DATA ---
#     product_data = {
#         "name": response.css("#productTitle::text").get("").strip(),
#         "price": price,
#         "stars": response.css("i[data-hook=average-star-rating] ::text").get("").strip(),
#         "rating_count": response.css("div[data-hook=total-review-count] ::text").get("").strip(),
#         "feature_bullets": feature_bullets,
#         "images": image_data,
#         "variant_data": variant_data,
#         "url": response.url
#     }

#     yield product_data



















import scrapy
from urllib.parse import urljoin, urlencode
import re
import chompjs

class AmazonSearchSpider(scrapy.Spider):
    name = "amazon_search"
    allowed_domains = [] 

    # 1. Your Keyword List
    keyword_list = ["ipad", "macbook pro M1", "gaming mouse"]

    def start_requests(self):
        for keyword in self.keyword_list:
            # 2. Build the URL dynamically for each keyword
            params = {'k': keyword, 'page': '1'}
            base_url = "https://www.amazon.com/s?"
            search_url = base_url + urlencode(params)
            
            yield scrapy.Request(
                url=search_url, 
                callback=self.discover_product_urls, 
                # 3. Use 'meta' to pass the keyword like a 'sticky note'
                meta={'render_js': True, 'keyword': keyword}, 
                dont_filter=False
            )

    def discover_product_urls(self, response):
        keyword = response.meta.get('keyword')
        # Get the current page number from meta, default to 1 if it's the first page
        current_page = response.meta.get('page', 1)
        # SET YOUR LIMIT HERE
        max_pages = 3 
        
        # 1. Extract organic product links
        links = response.css('h2 a.a-link-normal::attr(href)').getall()
        if not links:
            links = response.css('a[href*="/dp/"]::attr(href)').getall()

        product_urls = list(set([urljoin("https://www.amazon.com/", l.split("?")[0]) for l in links if "/dp/" in l]))
        
        self.logger.info(f"PAGE {current_page}: Found {len(product_urls)} products for '{keyword}'")

        # 2. Yield requests for product data
        for url in product_urls:
            yield scrapy.Request(
                url=url, 
                callback=self.parse_product_data,
                meta={'render_js': True, 'keyword': keyword},
                dont_filter=False
            )

        # 3. PAGINATION WITH LIMIT
        if current_page < max_pages:
            next_page = response.css('a.s-pagination-next::attr(href)').get()
            
            if next_page:
                next_url = urljoin("https://www.amazon.com/", next_page)
                self.logger.info(f"SCRAPING NEXT PAGE ({current_page + 1}/{max_pages})")
                
                yield scrapy.Request(
                    url=next_url,
                    callback=self.discover_product_urls,
                    meta={
                        'render_js': True, 
                        'keyword': keyword, 
                        'page': current_page + 1  # Increment the page counter
                    }
                )
        else:
            self.logger.info(f"LIMIT REACHED: Finished {max_pages} pages for '{keyword}'")

    # def discover_product_urls(self, response):
    #     # Retrieve the keyword from the sticky note
    #     keyword = response.meta.get('keyword')
        
    #     links = response.css('a[href*="/dp/"]::attr(href)').getall()
    #     product_urls = list(set([urljoin("https://www.amazon.com/", l.split("?")[0]) for l in links if "/dp/" in l]))
        
    #     self.logger.info(f"SOP: Found {len(product_urls)} products for keyword: {keyword}")

    #     for url in product_urls:
    #         yield scrapy.Request(
    #             url=url, 
    #             callback=self.parse_product_data,
    #             # Pass the keyword forward to the final parser
    #             meta={'render_js': True, 'keyword': keyword},
    #             dont_filter=False
    #         )

    def parse_product_data(self, response):
        # Retrieve the original search query
        search_query = response.meta.get('keyword')

        # --- 1. EXTRACT IMAGES (Using chompjs) ---
        image_data = []
        img_script = response.xpath("//script[contains(., 'colorImages')]/text()").get()
        if img_script:
            img_match = re.search(r"'initial':\s*(\[.*)", img_script)
            if img_match:
                try:
                    image_data = chompjs.parse_js_object(img_match.group(1))
                except Exception:
                    pass

        # --- 2. EXTRACT VARIANTS (Using chompjs) ---
        variant_data = {}
        var_script = response.xpath("//script[contains(., 'dimensionValuesDisplayData')]/text()").get()
        if var_script:
            var_match = re.search(r'dimensionValuesDisplayData"\s*:\s*({.*)', var_script)
            if var_match:
                try:
                    variant_data = chompjs.parse_js_object(var_match.group(1))
                except Exception:
                    pass

        # --- 3. SCRAPE TEXT DATA (CSS Selectors) ---
        feature_bullets = [bullet.strip() for bullet in response.css("#feature-bullets li ::text").getall() if bullet.strip()]
        
        rating_count = response.css("span#acrCustomerReviewText::text").get() or \
                   response.css("div[data-hook='total-review-count'] span::text").get() or \
                   response.xpath("//span[contains(@class, 'a-size-base') and contains(text(), 'ratings')]/text()").get("")

        price = response.css('.a-price span[aria-hidden="true"] ::text').get("")
        
        if not price or price == "$":
            script_text = response.xpath("//script[contains(., 'dimensionValuesDisplayData')]/text()").get()
            if script_text:
                found_price = re.search(r'"priceAmount":\s*(\d+\.\d+)', script_text)
                if found_price:
                    price = found_price.group(1)

        # --- 4. ASSEMBLE PRODUCT DATA ---
        yield {
            "search_query": search_query, # ADDED THIS FIELD
            "name": response.css("#productTitle::text").get("").strip(),
            "price": price,
            "stars": response.css("i[data-hook=average-star-rating] ::text").get("").strip(),
            "rating_count": rating_count,
            "feature_bullets": feature_bullets,
            "images": image_data,
            "variant_data": variant_data,
            "url": response.url
        }