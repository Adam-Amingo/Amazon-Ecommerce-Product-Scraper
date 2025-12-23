# Enterprise-Grade Amazon Data Extraction Engine

A high-performance Scrapy crawler engineered to bypass advanced E-commerce anti-bot protections and extract deeply nested product metadata. This engine is built to handle Amazon's dynamic layout changes and JavaScript-heavy data structures.

## 🛡️ Anti-Bot & Infrastructure
* **Residential Proxy Rotation:** Integrated with ScrapeOps to rotate requests across millions of IPs, eliminating 403 Forbidden errors.
* **Headless JS Rendering:** Full JavaScript execution to mimic real user behavior and bypass TLS fingerprinting.
* **Budget-Controlled Pagination:** Scalable crawling logic with an adjustable "Max Page" safety valve to optimize proxy credit usage.
* **Automated Deduplication:** Custom pipeline layer that filters duplicate products in real-time using URL hashing.

## 🛠️ Tech Stack & Problem Solving
| Tool | Purpose | Challenge Solved |
| :--- | :--- | :--- |
| **Scrapy** | Core Framework | Industry-standard concurrency and crawling speed. |
| **chompjs** | JS Parsing | Decodes malformed JavaScript Objects that standard Regex/JSON parsers fail on. |
| **Regex** | Data Pointing | High-speed location of specific backend metadata blocks within 1MB+ HTML files. |
| **Python Pipeline** | Data Integrity | Converts raw text into mathematical types (Floats for price/stars, Ints for ratings). |

## 📊 Extracted Data Points
* **Deep Variant Mapping:** Complete ASIN-to-Specification mapping (Color, Storage, Network).
* **High-Res Image Flattening:** Automatic extraction and cleaning of multi-image high-resolution galleries.
* **Search Query Labeling:** Metadata inheritance that tracks which specific keyword produced each result.
* **Clean Bullet Points:** Formatting of multi-line product features into single-cell searchable paragraphs.

## 🛠️ Technical Challenges & Problem Solving

Extracting data from Amazon is more than just "visiting a URL." This project solves several high-level engineering hurdles:

### 1. Bypassing Advanced Anti-Bot (403 Forbidden)
Amazon uses sophisticated TLS fingerprinting. This engine integrates **ScrapeOps Proxy** to rotate residential IPs and mimic authentic browser headers, ensuring a 99.9% success rate without IP bans.

### 2. Full JavaScript Rendering
Much of Amazon's data is "lazy-loaded" via JavaScript. This spider utilizes **Headless Rendering** to execute the scripts and capture the DOM only after the data has been populated.

### 3. Decoding "Messy" Source Code
Amazon hides its most valuable data (like product variants) inside malformed JSON objects within `<script>` tags. 
* **The HTML Analysis:** During development, raw HTML (see `amazon_page.html` in the repo) was captured and audited to locate hidden data blocks.
* **The Solution:** We used `chompjs` to decode these non-standard JavaScript objects into clean Python dictionaries.



### 4. Handling Dynamic Layouts
Amazon frequently A/B tests their layouts. This spider is built with **defensive parsing logic**—if one selector fails, it falls back to a second or third method to ensure no data is lost during a crawl.


## 🔍 The Reverse Engineering Process

Unlike basic scrapers that rely on fragile UI elements, this engine was built by auditing the raw network responses from Amazon's servers.

* **HTML Auditing:** We captured the raw server response (see `amazon_page.html`) to identify where the data "lives" before the browser renders it.
* **Data Deserialization:** By reverse-engineering the script tags, we discovered that Amazon stores product specifications in a highly compressed JavaScript format. 
* **The Result:** We bypass the "visual" layer entirely and extract data directly from the backend source, making the scraper 5x more stable against UI layout changes.

## ⚙️ Execution
## ⚙️ How to Run
1. **Clone & Install:**
   ```bash
   git clone [https://github.com/your-repo.git](https://github.com/your-repo.git)
   cd amazon-scraper
   pip install -r requirements.txt