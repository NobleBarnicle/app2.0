from bs4 import BeautifulSoup, Tag
from typing import Optional, List, Tuple, Dict
from datetime import datetime
import re
from .models import (
    CriminalCode, Part, Section, Subsection, 
    Definition, HistoricalNote, CrossReference,
    MarginalNote, ListItem
)

class CriminalCodeParser:
    """Parser for the Criminal Code of Canada HTML structure"""
    
    def __init__(self):
        self.section_number_pattern = re.compile(r'^\d+(\.\d+)?$')
        self.list_label_pattern = re.compile(r'^\([a-z0-9]+(?:\.\d+)?\)$')
        
    def parse_html(self, html_content: str) -> Optional[CriminalCode]:
        if not html_content or not html_content.strip():
            return None
        
        soup = BeautifulSoup(html_content, 'lxml')
        if not soup.find('head') or not soup.find('body'):
            return None
        
        # Extract basic metadata
        title = self._extract_title(soup)
        last_updated, last_amended = self._extract_dates(soup)
        
        # Parse all parts
        parts = self._parse_parts(soup)
        
        return CriminalCode(
            title=title,
            parts=parts,
            last_updated=last_updated,
            last_amended=last_amended
        )
    
    def parse_part(self, part_element: Tag) -> Optional[Part]:
        """Parse a single part element"""
        if not part_element:
            return None
            
        part_id = part_element.get('id', '')
        part_number = self._extract_part_number(part_element)
        title = self._extract_part_title(part_element)
        subheading = self._extract_part_subheading(part_element)
        
        # Get all sections within this part
        sections = self._parse_sections(part_element)
        
        return Part(
            id=part_id,
            number=part_number,
            title=title,
            subheading=subheading,
            sections=sections
        )
    
    def _parse_sections(self, container: Tag) -> List[Section]:
        """Parse all sections within a container element"""
        sections = []
        current_section = None
        
        for element in container.find_all(['p', 'div'], recursive=False):
            if 'Section' in element.get('class', []):
                if current_section:
                    sections.append(current_section)
                current_section = self._parse_section(element)
            elif current_section:
                # Add content to current section
                self._add_section_content(current_section, element)
        
        if current_section:
            sections.append(current_section)
            
        return sections
    
    def _parse_section(self, section_element: Tag) -> Optional[Section]:
        """Parse a single section element"""
        if not section_element:
            return None
        
        # Check for required elements
        section_id = section_element.get('id', '')
        section_number = self._extract_section_number(section_element)
        
        # Validate required attributes
        if not section_id or not section_number:
            return None
        
        marginal_note = self._parse_marginal_note(section_element)
        historical_notes = self._parse_historical_notes(section_element)
        
        # Create the section
        section = Section(
            id=section_id,
            number=section_number,
            text=self._extract_section_text(section_element),
            marginal_note=marginal_note,
            subsections=[],
            definitions=[],
            historical_notes=historical_notes,
            cross_references=[],
            list_items=[]
        )
        
        # Parse subsections if they exist
        subsections = []
        for subsec_elem in section_element.find_all('p', class_='Subsection'):
            subsection = self._parse_subsection(subsec_elem, section.id)
            if subsection:
                subsections.append(subsection)
        section.subsections = subsections
        
        # Add any remaining content
        for element in section_element.children:
            if isinstance(element, Tag):
                self._add_section_content(section, element)
        
        return section
    
    def _parse_subsection(self, subsection_elem: Tag, parent_section_id: str) -> Optional[Subsection]:
        """Parse a subsection element"""
        if not subsection_elem:
            return None
        
        # Extract subsection number (e.g., "(1)", "(2)", etc.)
        number = subsection_elem.find('span', class_='lawlabel')
        if not number:
            return None
        
        subsection = Subsection(
            id=subsection_elem.get('id', ''),
            number=number.get_text(strip=True),
            text=self._extract_subsection_text(subsection_elem),
            parent_section=parent_section_id,
            marginal_note=self._parse_marginal_note(subsection_elem)
        )
        
        # Parse list items within the subsection
        next_elem = subsection_elem.find_next_sibling()
        if next_elem and next_elem.name == 'ul' and 'ProvisionList' in next_elem.get('class', []):
            subsection.list_items = self._parse_nested_list(next_elem)
        
        return subsection
    
    def _extract_subsection_text(self, element: Tag) -> str:
        """Extract text content from subsection element"""
        # Remove the lawlabel and other elements we don't want in the text
        text_content = []
        for content in element.stripped_strings:
            if not self.list_label_pattern.match(content):
                text_content.append(content)
        return ' '.join(text_content).strip()
    
    def _parse_nested_list(self, list_element: Tag) -> List[ListItem]:
        """Parse a nested provision list into a hierarchical structure"""
        items = []
        
        for element in list_element.find_all('p', class_=['Paragraph', 'Subparagraph'], recursive=True):
            label = self._extract_list_label(element)
            text = self._extract_list_text(element)
            
            item = ListItem(
                id=element.get('id', ''),
                label=label,
                text=text,
                subitems=[]
            )
            
            # Check if this is a subitem
            if 'Subparagraph' in element.get('class', []):
                # Find parent paragraph
                parent_elem = element.find_parent('li').find_parent('li')
                if parent_elem:
                    parent_para = parent_elem.find('p', class_='Paragraph')
                    if parent_para:
                        item.parent_id = parent_para.get('id')
                        # Add to parent's subitems instead of main list
                        for parent_item in items:
                            if parent_item.id == item.parent_id:
                                parent_item.subitems.append(item)
                                break
                        continue
                    
            items.append(item)
        
        return items
    
    def _parse_marginal_note(self, element: Tag) -> Optional[MarginalNote]:
        """Parse marginal note from an element"""
        marginal_note_elem = element.find_previous_sibling('p', class_='MarginalNote')
        if marginal_note_elem:
            note_text = marginal_note_elem.get_text(strip=True)
            # Remove "Marginal note:" prefix if present
            note_text = re.sub(r'^Marginal note:\s*', '', note_text)
            return MarginalNote(text=note_text)
        return None
    
    def _parse_definitions(self, element: Tag) -> List[Definition]:
        """Parse definitions from a definition list element"""
        definitions = []
        for term_elem in element.find_all('dt'):
            term = term_elem.get_text(strip=True)
            definition_elem = term_elem.find_next_sibling('dd')
            if definition_elem:
                french_term = None
                french_term_elem = definition_elem.find('span', class_='DefinedTermLink', lang='fr')
                if french_term_elem:
                    french_term = french_term_elem.get_text(strip=True)
                
                definitions.append(Definition(
                    term=term,
                    definition_text=definition_elem.get_text(strip=True),
                    french_term=french_term
                ))
        return definitions
    
    def _extract_dates(self, soup: BeautifulSoup) -> Tuple[datetime, datetime]:
        """Extract last updated and amended dates"""
        # Implementation depends on exact HTML structure
        # This is a placeholder implementation
        return datetime.now(), datetime.now()
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """Extract the title of the Criminal Code"""
        title_elem = soup.find('h1', class_='HeadTitle')
        return title_elem.get_text(strip=True) if title_elem else "Criminal Code"
    
    def _extract_part_number(self, element: Tag) -> Optional[str]:
        """Extract part number from element"""
        number_match = re.search(r'Part ([IVXLCDM]+)', element.get_text())
        return number_match.group(1) if number_match else None
    
    def _extract_part_title(self, element: Tag) -> str:
        """Extract part title from element"""
        title_elem = element.find('span', class_='HTitleText1')
        return title_elem.get_text(strip=True) if title_elem else ""
    
    def _extract_part_subheading(self, element: Tag) -> Optional[str]:
        """Extract part subheading"""
        subheading_elem = element.find_next_sibling('h3', class_='Subheading')
        if subheading_elem:
            text_elem = subheading_elem.find('span', class_='HTitleText2')
            return text_elem.get_text(strip=True) if text_elem else None
        return None
    
    def _extract_section_number(self, element: Tag) -> str:
        """Extract section number from element"""
        section_label = element.find('span', class_='sectionLabel')
        return section_label.get_text(strip=True) if section_label else ""
    
    def _extract_section_text(self, element: Tag) -> str:
        """Extract main text content from section element"""
        # Remove section number and other elements we don't want in the text
        text_content = []
        for content in element.stripped_strings:
            if not self.section_number_pattern.match(content):
                text_content.append(content)
        return ' '.join(text_content).strip()
    
    def _parse_nested_list(self, list_element: Tag) -> List[Dict]:
        """
        Parse a nested provision list into a hierarchical structure.
        Returns a list of dictionaries containing the text and any nested items.
        """
        items = []
        current_item = None
        
        for element in list_element.children:
            if not isinstance(element, Tag):
                continue
                
            # Handle paragraph elements (main list items)
            if 'Paragraph' in element.get('class', []):
                if current_item:
                    items.append(current_item)
                
                label = self._extract_list_label(element)
                text = self._extract_list_text(element)
                current_item = {
                    'id': element.get('id', ''),
                    'label': label,
                    'text': text,
                    'subitems': []
                }
                
            # Handle nested lists
            elif element.name == 'ul' and 'ProvisionList' in element.get('class', []):
                if current_item:
                    nested_items = self._parse_nested_list(element)
                    current_item['subitems'].extend(nested_items)
                    
            # Handle continued paragraphs
            elif 'ContinuedParagraph' in element.get('class', []):
                if current_item:
                    current_item['text'] += ' ' + element.get_text(strip=True)
        
        if current_item:
            items.append(current_item)
            
        return items
    
    def _extract_list_label(self, element: Tag) -> str:
        """Extract the label (e.g., '(a)', '(i)') from a list item"""
        label_elem = element.find('span', class_='lawlabel')
        return label_elem.get_text(strip=True) if label_elem else ""
    
    def _extract_list_text(self, element: Tag) -> str:
        """Extract the text content from a list item, excluding the label"""
        # Remove the label element if it exists
        label_elem = element.find('span', class_='lawlabel')
        if label_elem:
            label_elem.decompose()
        
        return element.get_text(strip=True)
    
    def _add_section_content(self, section: Section, element: Tag):
        """Add content to a section based on element type"""
        # Handle definition lists
        if element.name == 'dl' and 'Definition' in element.get('class', []):
            definitions = self._parse_definitions(element)
            section.definitions.extend(definitions)
            
        # Handle historical notes
        elif 'HistoricalNote' in element.get('class', []):
            notes = self._parse_historical_notes(element)
            section.historical_notes.extend(notes)
            
        # Handle provision lists (nested lists)
        elif element.name == 'ul' and 'ProvisionList' in element.get('class', []):
            nested_items = self._parse_nested_list(element)
            # Convert nested items to subsections if appropriate
            self._convert_list_to_subsections(section, nested_items)
            
        # Handle cross references
        elif 'XRefExternal' in element.get('class', []):
            cross_ref = self._parse_cross_reference(element)
            if cross_ref:
                section.cross_references.append(cross_ref)
    
    def _parse_historical_notes(self, section_element: Tag) -> List[HistoricalNote]:
        """Parse historical notes that follow a section"""
        notes = []
        # Find the next historical note div after this section
        historical_div = section_element.find_next_sibling('div', class_='HistoricalNote')
        if historical_div:
            for note_item in historical_div.find_all('li', class_='HistoricalNoteSubItem'):
                notes.append(HistoricalNote(
                    text=note_item.get_text(strip=True)
                ))
        return notes
    
    def _parse_cross_reference(self, element: Tag) -> Optional[CrossReference]:
        """Parse a cross-reference from an element"""
        text = element.get_text(strip=True)
        
        # Check if it's an external act reference
        is_external = 'XRefExternalAct' in element.get('class', [])
        
        # Extract URL for external references
        external_url = None
        if is_external:
            link = element.find('a')
            if link and link.get('href'):
                # Convert relative URLs to absolute
                href = link['href']
                if href.startswith('/'):
                    external_url = f"https://laws-lois.justice.gc.ca{href}"
            else:
                external_url = href
    
        return CrossReference(
            text=text,
            target_section=self._extract_target_section(element),
            target_act=text if is_external else None,
            external_url=external_url,
            is_external=is_external
        )

    def _convert_list_to_subsections(self, section: Section, nested_items: List[Dict]):
        """Convert nested list items to subsections where appropriate"""
        for item in nested_items:
            # Check if this is a proper subsection (numbered like (1), (2), etc.)
            if re.match(r'^\(\d+\)$', item['label']):
                subsection = Subsection(
                    id=item['id'],
                    number=item['label'],
                    text=item['text'],
                    parent_section=section.id
                )
                
                # Handle any nested items as part of the subsection text
                if item['subitems']:
                    nested_text = self._format_nested_items(item['subitems'])
                    subsection.text += '\n' + nested_text
                
                section.subsections.append(subsection)
    
    def _format_nested_items(self, items: List[Dict], indent: int = 1) -> str:
        """Format nested items into a readable text structure"""
        text = []
        for item in items:
            prefix = '  ' * indent
            text.append(f"{prefix}{item['label']} {item['text']}")
            if item['subitems']:
                text.append(self._format_nested_items(item['subitems'], indent + 1))
        return '\n'.join(text)
    
    def _parse_parts(self, soup: BeautifulSoup) -> List[Part]:
        """Parse all parts from the document"""
        parts = []
        for part_elem in soup.find_all('div', class_='part'):
            part = self.parse_part(part_elem)
            if part:
                parts.append(part)
        return parts


