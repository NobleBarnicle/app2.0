import json
from app.scraper.scraper import CriminalCodeScraper
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # Initialize scraper
    scraper = CriminalCodeScraper()
    
    # Get the structure
    logger.info("Starting test scrape...")
    structure = scraper.extract_structure()
    
    # Save to a test JSON file
    output_file = 'test_output.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(structure, f, indent=2, ensure_ascii=False)
    
    logger.info(f"Saved test output to {output_file}")
    
    # Print first part as a sample
    if structure['parts']:
        logger.info("\nFirst part sample:")
        print(json.dumps(structure['parts'][0], indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main() 