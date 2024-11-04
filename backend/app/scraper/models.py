from typing import List, Optional, Dict
from dataclasses import dataclass
from datetime import datetime

@dataclass
class HistoricalNote:
    """Represents a historical note/amendment for a section"""
    text: str
    date: Optional[datetime] = None
    citation: Optional[str] = None

@dataclass 
class CrossReference:
    """Represents a cross-reference to another section or act"""
    text: str
    target_section: Optional[str] = None
    target_act: Optional[str] = None
    is_external: bool = False

@dataclass
class ListItem:
    """Represents an item in a nested list structure"""
    id: str
    label: str  # e.g., "(a)", "(i)", "(1)"
    text: str
    subitems: List['ListItem'] = None
    parent_id: Optional[str] = None
    
    def __post_init__(self):
        if self.subitems is None:
            self.subitems = []

@dataclass
class Definition:
    """Represents a legal definition within a section"""
    term: str
    definition_text: str
    french_term: Optional[str] = None
    subsection_id: Optional[str] = None
    nested_items: List[ListItem] = None  # For definitions with nested lists
    
    def __post_init__(self):
        if self.nested_items is None:
            self.nested_items = []

@dataclass
class MarginalNote:
    """Represents a marginal note for a section or subsection"""
    text: str
    language: str = "en"
    definition_marker: bool = False  # True for "Definition of" marginal notes

@dataclass
class Subsection:
    """Represents a subsection within a section"""
    id: str
    number: str  # e.g. "(1)", "(2)", etc.
    text: str
    marginal_note: Optional[MarginalNote] = None
    parent_section: Optional[str] = None
    definitions: List[Definition] = None
    cross_references: List[CrossReference] = None
    list_items: List[ListItem] = None  # For nested lists within subsections
    continued_text: Optional[str] = None  # For ContinuedSectionSubsection content
    
    def __post_init__(self):
        if self.definitions is None:
            self.definitions = []
        if self.cross_references is None:
            self.cross_references = []
        if self.list_items is None:
            self.list_items = []

@dataclass
class Section:
    """Represents a section of the Criminal Code"""
    id: str
    number: str  # e.g. "2", "2.1", etc.
    marginal_note: Optional[MarginalNote]
    text: str
    subsections: List[Subsection]
    definitions: List[Definition]
    historical_notes: List[HistoricalNote]
    cross_references: List[CrossReference]
    list_items: List[ListItem]  # For nested lists directly under section
    parent_part: Optional[str] = None
    
    def __post_init__(self):
        if self.subsections is None:
            self.subsections = []
        if self.definitions is None:
            self.definitions = []
        if self.historical_notes is None:
            self.historical_notes = []
        if self.cross_references is None:
            self.cross_references = []
        if self.list_items is None:
            self.list_items = []

@dataclass
class Part:
    """Represents a part of the Criminal Code"""
    id: str
    number: Optional[str]  # e.g. "I", "II", etc.
    title: str
    subheading: Optional[str]
    sections: List[Section]
    
    def __post_init__(self):
        if self.sections is None:
            self.sections = []

@dataclass
class CriminalCode:
    """Root object representing the entire Criminal Code"""
    title: str
    parts: List[Part]
    last_updated: datetime
    last_amended: datetime
    
    def __post_init__(self):
        if self.parts is None:
            self.parts = []
    
    def get_section_by_number(self, section_number: str) -> Optional[Section]:
        """Helper method to find a section by its number"""
        for part in self.parts:
            for section in part.sections:
                if section.number == section_number:
                    return section
        return None
