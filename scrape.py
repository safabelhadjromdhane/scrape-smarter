from src.company_scraper import CompanyScraper
from src.utils.file_utils import save_to_csv
import pandas as pd

def main():
    scraper = CompanyScraper(headless=False)
    
    try:
        # Scrape main data
        df = scraper.scrape(max_pages=5)  # Reduced for testing
        
        # Enrich with additional data
        df = scraper.enrich_data(df)
        
        # Save results
        save_to_csv(df, "data/scraped_data/companies.csv")
        print(f"Successfully scraped {len(df)} companies!")
        
    except Exception as e:
        print(f"Error during scraping: {e}")
    finally:
        scraper.close()

if __name__ == "__main__":
    main()