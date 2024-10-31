from dataclasses import dataclass
from typing import List, Optional

@dataclass
class Subsection:
    subsection_number: str
    content: str

@dataclass
class Section:
    section_number: str
    title: str
    content: str
    subsections: List[Subsection]

@dataclass
class Part:
    part_number: str
    title: str
    sections: List[Section]

@dataclass
class CriminalCode:
    title: str
    parts: List[Part]
    last_updated: Optional[str] = None 