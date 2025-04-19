import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from src.utils.user_agents import get_random_user_agent
from src.utils.logger import setup_logger
from src.utils.file_utils import save_to_csv
from typing import List, Dict, Set

logger = setup_logger("company_scraper")

class CompanyScraper:
    def __init__(self, headless: bool = False):
        self.driver = self._setup_driver(headless)
        self.collected_links: Set[str] = set()
        self.code_postal_idf = ["75", "77", "78", "91", "92", "93", "94", "95"]
        
    def _setup_driver(self, headless: bool) -> webdriver.Chrome:
        """Configure Chrome driver with anti-detection measures"""
        chrome_options = Options()
        
        if headless:
            chrome_options.add_argument("--headless=new")
            
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument(f"user-agent={get_random_user_agent()}")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Use webdriver-manager to handle driver automatically
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service, options=chrome_options)
    
    def extract_company_info(self, row) -> Dict[str, str]:
        """Extract company information from a table row"""
        company_info = {}
        
        try:
            link = row.find_element(By.CSS_SELECTOR, "a[href]").get_attribute("href")
            if link in self.collected_links:
                return None
            self.collected_links.add(link)
            company_info['link'] = link
        except Exception as e:
            logger.warning(f"Failed to extract link: {e}")
            company_info['link'] = None
            
        # Other extraction logic (similar to your original code)
        fields = {
            "company_name": (By.CLASS_NAME, "cse-company-name"),
            "director": (By.CLASS_NAME, "cse-officer-name"),
            "phone": (By.CLASS_NAME, "phone-copy"),
            "email": (By.CLASS_NAME, "email-copy"),
            "postal_code": (By.TAG_NAME, "span", 7),
            "revenue": (By.CLASS_NAME, "text-nowrap.font-weight-semibold"),
            "creation_date": (By.TAG_NAME, "span", 6),
            "staff_count": (By.TAG_NAME, "span", 10)
        }
        
        for field, locator in fields.items():
            try:
                if len(locator) == 3:  # Special case for postal code, date, etc.
                    cell = row.find_elements(By.TAG_NAME, "td")[locator[2]]
                    company_info[field] = cell.find_element(locator[0], locator[1]).text.strip()
                else:
                    company_info[field] = row.find_element(*locator).text.strip()
            except Exception as e:
                logger.debug(f"Failed to extract {field}: {e}")
                company_info[field] = None
                
        return company_info
    
    def scrape_page(self, page_num: int) -> List[Dict]:
        """Scrape a single page of results"""
        url = f'https://infonet.fr/recherche-entreprises/{page_num}/P2FwZUNvZGVzPTg3MTBBJTJDODcxMEIlMkM4NzEwQyUyQzg3MjBBJTJDODczMEIlMkM4NzkwQSUyQzg3OTBCJTJDODcyMEIlMkM4NzMwQSZzaXJlbnM9Jm1pbkNyZWF0aW9uRGF0ZT0yMDAwJm1heENyZWF0aW9uRGF0ZT0yMDI1JmluY2x1ZGVGb3JlaWduZXJzPTAmaXNBY3RpdmU9MSZzb3J0Qnk9c2FsZXMmc29ydE9yZGVyPWRlc2MmY3VzdG9tQ29sdW1uTmFtZT1zdGFmZiZsaW1pdD0yNQ=='
        self.driver.get(url)
        time.sleep(2)  # Consider using WebDriverWait instead
        
        page_data = []
        rows = self.driver.find_elements(By.CSS_SELECTOR, "tr.toggle-add-to-list-button")
        
        for row in rows:
            try:
                postal_code_cell = row.find_elements(By.TAG_NAME, "td")[7]
                code_postal = postal_code_cell.find_element(By.TAG_NAME, "span").text.strip()
                
                if code_postal in self.code_postal_idf:
                    company_info = self.extract_company_info(row)
                    if company_info:
                        page_data.append(company_info)
            except Exception as e:
                logger.error(f"Error processing row: {e}")
                
        return page_data
    
    def scrape(self, max_pages: int = 100) -> pd.DataFrame:
        """Main scraping function"""
        all_data = []
        
        for page_num in range(1, max_pages + 1):
            logger.info(f"Scraping page {page_num}/{max_pages}")
            try:
                page_data = self.scrape_page(page_num)
                all_data.extend(page_data)
            except Exception as e:
                logger.error(f"Error scraping page {page_num}: {e}")
                continue
                
        return pd.DataFrame(all_data)
    
    def enrich_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add additional information by visiting each company page"""
        # Your additional data collection logic here
        return df
    
    # In company_scraper.py
from src.utils.logger import setup_logger
from src.utils.file_utils import save_to_csv

logger = setup_logger("company_scraper")

def scrape(self):
    try:
        data = [...]  # Your scraping logic
        save_to_csv(data, "data/scraped/companies.csv")
        logger.info("Scraping completed successfully")
    except Exception as e:
        logger.critical(f"Scraping failed: {e}")
        raise
    def close(self):
        """Clean up resources"""
        self.driver.quit()