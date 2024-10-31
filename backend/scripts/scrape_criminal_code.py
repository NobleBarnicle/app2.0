from app.scraper import CriminalCodeScraper, CriminalCodeParser, CriminalCode, Part, Section, Subsection
import logging
from datetime import datetime
import json

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def main():
    logger.info("Starting Criminal Code scraping process")
    
    # Initialize our scraper and parser
    scraper = CriminalCodeScraper()
    parser = CriminalCodeParser()
    
    # Fetch the main page
    soup = scraper.fetch_page()
    if not soup:
        logger.error("Failed to fetch the Criminal Code page")
        return
    
    # Find all part elements
    part_elements = soup.find_all('div', class_='part')
    if not part_elements:
        logger.error("No parts found in the Criminal Code")
        return
    
    # Parse each part
    parts = []
    for part_element in part_elements:
        part_data = parser.parse_part(part_element)
        if part_data:
            # Convert dictionary to Part object
            sections = [
                Section(
                    section_number=section['section_number'],
                    title=section['title'],
                    content=section['content'],
                    subsections=[
                        Subsection(**subsection)
                        for subsection in section['subsections']
                    ]
                )
                for section in part_data['sections']
            ]
            
            part = Part(
                part_number=part_data['part_number'],
                title=part_data['title'],
                sections=sections
            )
            parts.append(part)
    
    # Create the final CriminalCode object
    criminal_code = CriminalCode(
        title="Criminal Code",
        parts=parts,
        last_updated=datetime.now().isoformat()
    )
    
    # Save to JSON file
    output_file = 'data/criminal_code.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(criminal_code.__dict__, f, indent=2, default=lambda x: x.__dict__)
    
    logger.info(f"Scraping completed. Data saved to {output_file}")

if __name__ == "__main__":
    main() 