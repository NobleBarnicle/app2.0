from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class CriminalCodeParser:
    def __init__(self):
        self.current_part = None
        self.current_section = None
    
    def parse_part(self, element: BeautifulSoup) -> Dict:
        """Parse a part of the Criminal Code."""
        try:
            part_num = element.get('id', '').replace('part-', '')
            title = element.find('h2').text.strip() if element.find('h2') else ''
            
            return {
                'part_number': part_num,
                'title': title,
                'sections': self.parse_sections(element)
            }
        except Exception as e:
            logger.error(f"Error parsing part: {str(e)}")
            return {}
    
    def parse_sections(self, part_element: BeautifulSoup) -> List[Dict]:
        """Parse all sections within a part."""
        sections = []
        section_elements = part_element.find_all('div', class_='section')
        
        for section in section_elements:
            parsed_section = self.parse_section(section)
            if parsed_section:
                sections.append(parsed_section)
        
        return sections
    
    def parse_section(self, element: BeautifulSoup) -> Optional[Dict]:
        """Parse a single section of the Criminal Code."""
        try:
            section_num = element.get('id', '').replace('section-', '')
            title = element.find('h3').text.strip() if element.find('h3') else ''
            content = element.find('div', class_='provision').text.strip()
            
            return {
                'section_number': section_num,
                'title': title,
                'content': content,
                'subsections': self.parse_subsections(element)
            }
        except Exception as e:
            logger.error(f"Error parsing section: {str(e)}")
            return None
    
    def parse_subsections(self, section_element: BeautifulSoup) -> List[Dict]:
        """Parse all subsections within a section."""
        subsections = []
        subsection_elements = section_element.find_all('div', class_='subsection')
        
        for subsection in subsection_elements:
            parsed_subsection = self.parse_subsection(subsection)
            if parsed_subsection:
                subsections.append(parsed_subsection)
        
        return subsections
    
    def parse_subsection(self, element: BeautifulSoup) -> Optional[Dict]:
        """Parse a single subsection."""
        try:
            subsection_num = element.get('id', '').replace('subsection-', '')
            content = element.text.strip()
            
            return {
                'subsection_number': subsection_num,
                'content': content
            }
        except Exception as e:
            logger.error(f"Error parsing subsection: {str(e)}")
            return None 