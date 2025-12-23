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

## ⚙️ Execution
## ⚙️ How to Run
1. **Clone & Install:**
   ```bash
   git clone [https://github.com/your-repo.git](https://github.com/your-repo.git)
   cd amazon-scraper
   pip install -r requirements.txt