# Criminal Code HTML Structure Guide

## Root Level
The Criminal Code is hierarchically structured, with Parts as top-level containers.

## 1. Parts
- Parts are the highest-level divisions of the Criminal Code.
- Parts may contain subheadings. 
### Example 1: Basic Part
<h2 class="Part" id="h-115006"><span class="HTitleText1">Short Title</span></h2>

#### Components:
- Title: "Short Title" (exact text from HTitleText1)
- ID: "h-115006" (unique identifier)
- HTML Classes: ["Part"] (for element selection)
- Element Type: h2

### Example 2: Numbered Part w/ subheadings
<h2 class="Part" id="h-115244"><span class="HTitleText1">Part I</span></h2>
<h3 class="Subheading" id="h-115245"><span class="HTitleText2">General</span></h3>

#### Components:
- Title: "Part I" (text from HTitleText1)
- Subheading: "General" (text from HTitleText2)
- IDs:
  - Part ID: "h-115244" (unique identifier)
  - Subheading ID: "h-115245" (unique identifier)
- HTML Classes: 
  - Part: ["Part"]
  - Subheading: ["Subheading"]
- Element Types:
  - Part: h2
  - Subheading: h3
- Special Features:
  - Contains subheading element
  - Numbered part format

## 2. Sections
Sections come in multiple configurations:

### 2.1 Base Case Section
A simple section with marginal note, content, and historical note.

#### Example:
<p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Where one party cannot be convicted</p>
<p class="Section" id="115611"><strong><a class="sectionLabel" id="s-23.1"><span class="sectionLabel">23.1</span></a></strong>&nbsp;For greater certainty, sections 21 to 23 apply in respect of an accused notwithstanding the fact that the person whom the accused aids or abets, counsels or procures or receives, comforts or assists cannot be convicted of the offence.</p>
<div class="HistoricalNote"><ul class="HistoricalNote"><li class="HistoricalNoteSubItem">R.S., 1985, c. 24 (2nd Supp.), s. 45</li></ul></div>

#### Components:
- Marginal Note: "Where one party cannot be convicted" (text from MarginalNote > span)
- Section ID: "115611" (unique identifier)
- Section Number: "23.1" (from sectionLabel span)
- Content: "For greater certainty, sections 21 to 23 apply in respect of an accused notwithstanding the fact that the person whom the accused aids or abets, counsels or procures or receives, comforts or assists cannot be convicted of the offence."
- Historical Note: "R.S., 1985, c. 24 (2nd Supp.), s. 45"
- HTML Classes: ["MarginalNote", "Section", "HistoricalNote"]

### 2.2 Section with List
Sections may contain enumerated lists that are not true subsections (i.e. they are not preceded by a subsection number, (a), (b), etc.). Some sections with lists have a ContinuedSectionSubsection, while others may not.

#### Example:       #note how the list can be nested, we must recursively check for not only the next list item but also the potential nested sub-nodes (a)(i), (a)(ii), (b)(i), (b)(ii), etc.
<p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Offences of negligence — organizations</p>
<p class="Section" id="115590"><strong><a class="sectionLabel" id="s-22.1"><span class="sectionLabel">22.1</span></a></strong>&nbsp;In respect of an offence that requires the prosecution to prove negligence, an organization is a party to the offence if</p>
<ul class="ProvisionList"><li><p class="Paragraph" id="115592"><span class="lawlabel">(a)</span>&nbsp;acting within the scope of their authority</p><ul class="ProvisionList"><li><p class="Subparagraph" id="115593"><span class="lawlabel">(i)</span>&nbsp;one of its representatives is a party to the offence, or</p></li><li><p class="Subparagraph" id="115594"><span class="lawlabel">(ii)</span>&nbsp;two or more of its representatives engage in conduct, whether by act or omission, such that, if it had been the conduct of only one representative, that representative would have been a party to the offence; and</p></li></ul></li><li><p class="Paragraph" id="115595"><span class="lawlabel">(b)</span>&nbsp;the senior officer who is responsible for the aspect of the organization’s activities that is relevant to the offence departs — or the senior officers, collectively, depart — markedly from the standard of care that, in the circumstances, could reasonably be expected to prevent a representative of the organization from being a party to the offence.</p></li></ul>
<div class="HistoricalNote"><ul class="HistoricalNote"><li class="HistoricalNoteSubItem">2003, c. 21, s. 2</li></ul></div>
#### Components:
- Marginal Note: "Offences of negligence — organizations" (text from MarginalNote > span)
- Section ID: "115590" (unique identifier)
- Section Number: "22.1" (from sectionLabel span)
- Initial Content: "In respect of an offence that requires the prosecution to prove negligence, an organization is a party to the offence if"
- Provision List Structure:
  - Item A (ID: "115592"): "acting within the scope of their authority"
    - Sub-item i (ID: "115593"): "one of its representatives is a party to the offence, or"
    - Sub-item ii (ID: "115594"): "two or more of its representatives engage in conduct, whether by act or omission, such that, if it had been the conduct of only one representative, that representative would have been a party to the offence; and"
  - Item B (ID: "115595"): "the senior officer who is responsible for the aspect of the organization's activities that is relevant to the offence departs — or the senior officers, collectively, depart — markedly from the standard of care that, in the circumstances, could reasonably be expected to prevent a representative of the organization from being a party to the offence."
- Historical Note: "2003, c. 21, s. 2"
- HTML Classes: ["MarginalNote", "Section", "ProvisionList", "Paragraph", "Subparagraph", "HistoricalNote", "HistoricalNoteSubItem"]
- Special Features:
  - Nested provision list structure with two levels (a/b and i/ii)
  - Lawlabel elements for list markers

### 2.3 Section with Definitions
Stand-alone sections may have dictionaries. Dictionaries can have in-line definitions and indented definitions.

#### 2.3.1 Section with Inline Definitions
A section containing inline definitions with multiple historical notes and amendment details.

##### Example:
<p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Further definitions — firearms</p>
<p class="Section" id="1487945"><strong><a class="sectionLabel" id="s-2.1"><span class="sectionLabel">2.1</span></a></strong>&nbsp;In this Act, <span class="DefinedTerm"><dfn>ammunition</dfn></span>, <span class="DefinedTerm"><dfn>antique firearm</dfn></span>, <span class="DefinedTerm"><dfn>automatic firearm</dfn></span>, <span class="DefinedTerm"><dfn>cartridge magazine</dfn></span>, <span class="DefinedTerm"><dfn>cross-bow</dfn></span>, <span class="DefinedTerm"><dfn>firearm part</dfn></span>, <span class="DefinedTerm"><dfn>handgun</dfn></span>, <span class="DefinedTerm"><dfn>imitation firearm</dfn></span>, <span class="DefinedTerm"><dfn>prohibited ammunition</dfn></span>, <span class="DefinedTerm"><dfn>prohibited device</dfn></span>, <span class="DefinedTerm"><dfn>prohibited firearm</dfn></span>, <span class="DefinedTerm"><dfn>prohibited weapon</dfn></span>, <span class="DefinedTerm"><dfn>replica firearm</dfn></span>, <span class="DefinedTerm"><dfn>restricted firearm</dfn></span> and <span class="DefinedTerm"><dfn>restricted weapon</dfn></span>, as well as <span class="DefinedTerm"><dfn>authorization</dfn></span>, <span class="DefinedTerm"><dfn>licence</dfn></span> and <span class="DefinedTerm"><dfn>registration certificate</dfn></span> when used in relation to those words and expressions, have the same meaning as in subsection 84(1).</p>
<div class="HistoricalNote"><ul class="HistoricalNote"><li class="HistoricalNoteSubItem">2009, c. 22, s. 1</li><li class="HistoricalNoteSubItem"><a href="#1432858-1487947" aria-controls="centred-popup" class="wb-lbx wb-init wb-data-ajax-after-inited wb-lbx-inited" role="button" data-ajax-after="1432858-1487947.html" id="wb-auto-5">2023, c. 32, s. 0.1</a><section id="1432858-1487947" class="mfp-hide modal-dialog modal-content overlay-def"><header class="modal-header"><h2 class="modal-title">2023, c. 32, s. 0.1</h2></header><div class="modal-body"><ul class="Section ProvisionList" id="1432858"><li><p class="Subsection amending" id="1432859"><strong><a class="sectionLabel" id="s-0.1"><span class="sectionLabel">0.1</span></a></strong>&nbsp;<span class="lawlabel">(1)</span>&nbsp;Section 2.1 of the <cite class="XRefExternalAct">Criminal Code</cite> is replaced by the following:</p><section><div class="AmendedText"><p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Further definitions — firearms</p><p class="Section"><strong>2.1</strong>&nbsp;In this Act, <span class="DefinedTerm"><dfn>ammunition</dfn></span>, <span class="DefinedTerm"><dfn>antique firearm</dfn></span>, <span class="DefinedTerm"><dfn>automatic firearm</dfn></span>, <span class="DefinedTerm"><dfn>cartridge magazine</dfn></span>, <span class="DefinedTerm"><dfn>cross-bow</dfn></span>, <span class="DefinedTerm"><dfn>firearm part</dfn></span>, <span class="DefinedTerm"><dfn>handgun</dfn></span>, <span class="DefinedTerm"><dfn>imitation firearm</dfn></span>, <span class="DefinedTerm"><dfn>prohibited ammunition</dfn></span>, <span class="DefinedTerm"><dfn>prohibited device</dfn></span>, <span class="DefinedTerm"><dfn>prohibited firearm</dfn></span>, <span class="DefinedTerm"><dfn>prohibited weapon</dfn></span>, <span class="DefinedTerm"><dfn>replica firearm</dfn></span>, <span class="DefinedTerm"><dfn>restricted firearm</dfn></span> and <span class="DefinedTerm"><dfn>restricted weapon</dfn></span>, as well as <span class="DefinedTerm"><dfn>authorization</dfn></span>, <span class="DefinedTerm"><dfn>licence</dfn></span> and <span class="DefinedTerm"><dfn>registration certificate</dfn></span> when used in relation to those words and expressions, have the same meaning as in subsection 84(1).</p></div></section></li><li><p class="Subsection CIF" id="1432861"><span class="lawlabel">(2)</span>&nbsp;Subsection (1) comes into force on a day to be fixed by order of the Governor in Council.</p></li></ul></div></section></li></ul></div>

##### Components:
- Marginal Note: "Further definitions — firearms" (text from MarginalNote > span)
- Section ID: "1487945" (unique identifier)
- Section Number: "2.1" (from sectionLabel span)
- Content: "In this Act, [defined terms] have the same meaning as in subsection 84(1)."
- Defined Terms (class="DefinedTerm"):
  - ammunition
  - antique firearm
  - automatic firearm
  - cartridge magazine
  - cross-bow
  - firearm part
  - handgun
  - imitation firearm
  - prohibited ammunition
  - prohibited device
  - prohibited firearm
  - prohibited weapon
  - replica firearm
  - restricted firearm
  - restricted weapon
  - authorization
  - licence
  - registration certificate
- Historical Notes:
  - Primary: "2009, c. 22, s. 1"
  - Amendment: "2023, c. 32, s. 0.1" (with modal popup containing amendment details)
- HTML Classes: ["MarginalNote", "Section", "DefinedTerm", "HistoricalNote", "HistoricalNoteSubItem"]
- Special Features:
  - Multiple historical notes (unlike base case)
  - Interactive amendment link with modal
  - Inline dfn tags for term definitions

#### 2.3.2 Stand-alone Section with Indented Definitions
Note that this example contains french terms
##### Example:
<p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Definitions</p>
<p class="Section" id="117789"><strong><a class="sectionLabel" id="s-118"><span class="sectionLabel">118</span></a></strong>&nbsp;In this Part,</p>
<dl class="Definition"><dt id="117791"><span class="DefinedTerm"><dfn>evidence</dfn></span></dt><dd><p class="Definition"><span class="DefinedTerm"><dfn>evidence</dfn></span> or <span class="DefinedTerm"><dfn>statement</dfn></span> means an assertion of fact, opinion, belief or knowledge, whether material or not and whether admissible or not; (<span class="DefinedTermLink" lang="fr">témoignage</span>, <span class="DefinedTermLink" lang="fr">déposition</span> ou <span class="DefinedTermLink" lang="fr">déclaration</span>)</p></dd><dt id="117792"><span class="DefinedTerm"><dfn>government</dfn></span></dt><dd><p class="Definition"><span class="DefinedTerm"><dfn>government</dfn></span> means</p><ul class="ProvisionList"><li><p class="Paragraph" id="117793"><span class="lawlabel">(a)</span>&nbsp;the Government of Canada,</p></li><li><p class="Paragraph" id="117794"><span class="lawlabel">(b)</span>&nbsp;the government of a province, or</p></li><li><p class="Paragraph" id="117795"><span class="lawlabel">(c)</span>&nbsp;Her Majesty in right of Canada or a province; (<span class="DefinedTermLink" lang="fr">gouvernement</span>)</p></li></ul></dd><dt id="117796"><span class="DefinedTerm"><dfn>judicial proceeding</dfn></span></dt><dd><p class="Definition"><span class="DefinedTerm"><dfn>judicial proceeding</dfn></span> means a proceeding</p><ul class="ProvisionList"><li><p class="Paragraph" id="117797"><span class="lawlabel">(a)</span>&nbsp;in or under the authority of a court of justice,</p></li><li><p class="Paragraph" id="117798"><span class="lawlabel">(b)</span>&nbsp;before the Senate or House of Commons or a committee of the Senate or House of Commons, or before a legislative council, legislative assembly or house of assembly or a committee thereof that is authorized by law to administer an oath,</p></li><li><p class="Paragraph" id="117799"><span class="lawlabel">(c)</span>&nbsp;before a court, judge, justice, provincial court judge or coroner,</p></li><li><p class="Paragraph" id="117800"><span class="lawlabel">(d)</span>&nbsp;before an arbitrator or umpire, or a person or body of persons authorized by law to make an inquiry and take evidence therein under oath, or</p></li><li><p class="Paragraph" id="117801"><span class="lawlabel">(e)</span>&nbsp;before a tribunal by which a legal right or legal liability may be established,</p></li></ul><p class="ContinuedDefinition" id="117802">whether or not the proceeding is invalid for want of jurisdiction or for any other reason; (<span class="DefinedTermLink" lang="fr">procédure judiciaire</span>)</p></dd><dt id="117803"><span class="DefinedTerm"><dfn>office</dfn></span></dt><dd><p class="Definition"><span class="DefinedTerm"><dfn>office</dfn></span> includes</p><ul class="ProvisionList"><li><p class="Paragraph" id="117804"><span class="lawlabel">(a)</span>&nbsp;an office or appointment under the government,</p></li><li><p class="Paragraph" id="117805"><span class="lawlabel">(b)</span>&nbsp;a civil or military commission, and</p></li><li><p class="Paragraph" id="117806"><span class="lawlabel">(c)</span>&nbsp;a position or an employment in a public department; (<span class="DefinedTermLink" lang="fr">charge</span> ou <span class="DefinedTermLink" lang="fr">emploi</span>)</p></li></ul></dd><dt id="117807"><span class="DefinedTerm"><dfn>official</dfn></span></dt><dd><p class="Definition"><span class="DefinedTerm"><dfn>official</dfn></span> means a person who</p><ul class="ProvisionList"><li><p class="Paragraph" id="117808"><span class="lawlabel">(a)</span>&nbsp;holds an office, or</p></li><li><p class="Paragraph" id="117809"><span class="lawlabel">(b)</span>&nbsp;is appointed or elected to discharge a public duty; (<span class="DefinedTermLink" lang="fr">fonctionnaire</span>)</p></li></ul></dd><dt id="117810"><span class="DefinedTerm"><dfn>witness</dfn></span></dt><dd><p class="Definition"><span class="DefinedTerm"><dfn>witness</dfn></span> means a person who gives evidence orally under oath or by affidavit in a judicial proceeding, whether or not he is competent to be a witness, and includes a child of tender years who gives evidence but does not give it under oath, because, in the opinion of the person presiding, the child does not understand the nature of an oath. (<span class="DefinedTermLink" lang="fr">témoin</span>)</p></dd></dl>
<div class="HistoricalNote"><ul class="HistoricalNote"><li class="HistoricalNoteSubItem">R.S., 1985, c. C-46, s. 118</li><li class="HistoricalNoteSubItem"> R.S., 1985, c. 27 (1st Supp.), ss. 15, 203</li><li class="HistoricalNoteSubItem"> 2007, c. 13, s. 2</li></ul></div>

##### Components:
- Marginal Note: "Definitions" (text from MarginalNote > span)
- Section ID: "117789" (unique identifier)
- Section Number: "118" (from sectionLabel span)
- Initial Content: "In this Part," (text after section number)
- Definitions List (class="Definition"):
  1. evidence/statement:
     - Term ID: "117791"
     - Term: "evidence" or "statement"
     - Definition: "means an assertion of fact, opinion, belief or knowledge, whether material or not and whether admissible or not"
     - French Terms: Found in elements with class="DefinedTermLink" and lang="fr":
     - "témoignage"
     - "déposition"
     - "déclaration"

  2. government:
     - Term ID: "117792"
     - Term: "government"
     - Definition: "means" + list items:
       - Item A (ID: "117793"): "the Government of Canada"
       - Item B (ID: "117794"): "the government of a province"
       - Item C (ID: "117795"): "Her Majesty in right of Canada or a province"
     - French Term: Found in element with class="DefinedTermLink" and lang="fr": "gouvernement"

  3. judicial proceeding:
     - Term ID: "117796"
     - Term: "judicial proceeding"
     - Definition: "means a proceeding" + list items:
       - Item A (ID: "117797"): "in or under the authority of a court of justice"
       - Item B (ID: "117798"): "before the Senate or House of Commons or a committee of the Senate or House of Commons, or before a legislative council, legislative assembly or house of assembly or a committee thereof that is authorized by law to administer an oath"
       - Item C (ID: "117799"): "before a court, judge, justice, provincial court judge or coroner"
       - Item D (ID: "117800"): "before an arbitrator or umpire, or a person or body of persons authorized by law to make an inquiry and take evidence therein under oath"
       - Item E (ID: "117801"): "before a tribunal by which a legal right or legal liability may be established"
     - Continued Definition (ID: "117802"): "whether or not the proceeding is invalid for want of jurisdiction or for any other reason"
     - French Term: Found in element with class="DefinedTermLink" and lang="fr": "procédure judiciaire"

  4. office:
     - Term ID: "117803"
     - Term: "office"
     - Definition: "includes" + list items:
       - Item A (ID: "117804"): "an office or appointment under the government"
       - Item B (ID: "117805"): "a civil or military commission"
       - Item C (ID: "117806"): "a position or an employment in a public department"
     - French Terms: Found in elements with class="DefinedTermLink" and lang="fr":
       - "charge"
       - "emploi"

  5. official:
     - Term ID: "117807"
     - Term: "official"
     - Definition: "means a person who" + list items:
       - Item A (ID: "117808"): "holds an office"
       - Item B (ID: "117809"): "is appointed or elected to discharge a public duty"
     - French Term: Found in element with class="DefinedTermLink" and lang="fr": "fonctionnaire"

  6. witness:
     - Term ID: "117810"
     - Term: "witness"
     - Definition: "means a person who gives evidence orally under oath or by affidavit in a judicial proceeding, whether or not he is competent to be a witness, and includes a child of tender years who gives evidence but does not give it under oath, because, in the opinion of the person presiding, the child does not understand the nature of an oath"
     - French Term: Found in element with class="DefinedTermLink" and lang="fr": "témoin"

- Historical Notes:
  - "R.S., 1985, c. C-46, s. 118"
  - "R.S., 1985, c. 27 (1st Supp.), ss. 15, 203"
  - "2007, c. 13, s. 2"

- HTML Classes: ["MarginalNote", "Section", "Definition", "DefinedTerm", "ProvisionList", "Paragraph", "ContinuedDefinition", "DefinedTermLink", "HistoricalNote"]

- Special Features:
  - Definition list (dl) structure
  - Nested provision lists within definitions
  - Bilingual term links. *These can be found in any other section types with class="DefinedTermLink" and lang="fr"*
  - Multiple historical notes
  - ContinuedDefinition for extended definitions

### 2.4 Section with Subsections
- A very important and common section type. They have many variations, and can themselves contain yet further subsections. We must check recursively for subsections.
- Like Sections (2.3) they have marginal notes, section numbers, and historical notes. Also like sections (2.3) they can contain lists and definitions.

#### 2.4.1 Section with Subsections - Base Case
##### Example: 
<p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Effect of judicial acts</p>
<ul class="Section ProvisionList" id="115246"><li><p class="Subsection" id="1201744"><strong><a class="sectionLabel" id="s-3.1"><span class="sectionLabel">3.1</span></a></strong>&nbsp;<span class="lawlabel">(1)</span>&nbsp;Unless otherwise provided or ordered, anything done by a court, justice or judge is effective from the moment it is done, whether or not it is reduced to writing.</p></li><li><p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Clerk of the court</p><p class="Subsection" id="1201745"><span class="lawlabel">(2)</span>&nbsp;Unless otherwise provided or ordered, if anything is done from the bench by a court, justice or judge and it is reduced to writing, the clerk of the court may sign the writing.</p></li></ul>
<div class="HistoricalNote"><ul class="HistoricalNote"><li class="HistoricalNoteSubItem">2002, c. 13, s. 2</li><li class="HistoricalNoteSubItem"><a href="#1146298-1201747" aria-controls="centred-popup" class="wb-lbx wb-init wb-data-ajax-after-inited wb-lbx-inited" role="button" data-ajax-after="1146298-1201747.html" id="wb-auto-10">2019, c. 25, s. 3</a><section id="1146298-1201747" class="mfp-hide modal-dialog modal-content overlay-def"><header class="modal-header"><h2 class="modal-title">2019, c. 25, s. 3</h2></header><div class="modal-body"><p class="MarginalNote"><span class="wb-invisible">Marginal note:</span><span class="HistoricalNote">2002, c. 13, s. 2</span></p><p class="Section amending" id="1146298"><strong><a class="sectionLabel" id="s-3"><span class="sectionLabel">3</span></a></strong>&nbsp;Section 3.1 of the Act is renumbered as subsection 3.1(1) and is amended by adding the following:</p><section><div class="AmendedText"><ul class="Section ProvisionList" id=""><li><p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Clerk of the court</p><p class="Subsection"><span class="lawlabel">(2)</span>&nbsp;Unless otherwise provided or ordered, if anything is done from the bench by a court, justice or judge and it is reduced to writing, the clerk of the court may sign the writing.</p></li></ul></div></section></div></section></li></ul></div>

##### Components:
- Marginal Note: "Effect of judicial acts" (text from MarginalNote > span)
- Section ID: "115246" (unique identifier)
- Section Number: "3.1" (from sectionLabel span)
- Subsections:
  1. First Subsection (ID: "1201744"):
     - Number: "(1)" (from lawlabel span)
     - Content: "Unless otherwise provided or ordered, anything done by a court, justice or judge is effective from the moment it is done, whether or not it is reduced to writing."
  
  2. Second Subsection (ID: "1201745"):
     - Marginal Note: "Clerk of the court"
     - Number: "(2)" (from lawlabel span)
     - Content: "Unless otherwise provided or ordered, if anything is done from the bench by a court, justice or judge and it is reduced to writing, the clerk of the court may sign the writing."

- Historical Notes:
  - Primary: "2002, c. 13, s. 2"
  - Amendment: "2019, c. 25, s. 3" (with modal popup containing amendment details)
    - Modal Content:
      - Title: "2019, c. 25, s. 3"
      - Amendment Description: "Section 3.1 of the Act is renumbered as subsection 3.1(1) and is amended by adding the following:"
      - Amended Text: Contains subsection (2) addition

- HTML Classes: ["MarginalNote", "Section", "ProvisionList", "Subsection", "HistoricalNote", "HistoricalNoteSubItem"]
- Special Features:
  - Multiple historical notes with interactive amendment link
  - Modal popup for amendment details
  - Subsection-specific marginal note for subsection (2)
#### 2.4.2 Section with Subsections - Lists
##### Example:
<p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Fraud</p>
<ul class="Section ProvisionList" id="122425"><li><p class="Subsection" id="122427"><strong><a class="sectionLabel" id="s-380"><span class="sectionLabel">380</span></a></strong>&nbsp;<span class="lawlabel">(1)</span>&nbsp;Every one who, by deceit, falsehood or other fraudulent means, whether or not it is a false pretence within the meaning of this Act, defrauds the public or any person, whether ascertained or not, of any property, money or valuable security or any service,</p><ul class="ProvisionList"><li><p class="Paragraph" id="122428"><span class="lawlabel">(a)</span>&nbsp;is guilty of an indictable offence and liable to a term of imprisonment not exceeding fourteen years, where the subject-matter of the offence is a testamentary instrument or the value of the subject-matter of the offence exceeds five thousand dollars; or</p></li><li><p class="Paragraph" id="122429"><span class="lawlabel">(b)</span>&nbsp;is guilty</p><ul class="ProvisionList"><li><p class="Subparagraph" id="122430"><span class="lawlabel">(i)</span>&nbsp;of an indictable offence and is liable to imprisonment for a term not exceeding two years, or</p></li><li><p class="Subparagraph" id="122431"><span class="lawlabel">(ii)</span>&nbsp;of an offence punishable on summary conviction,</p></li></ul><p class="ContinuedParagraph" id="122432">where the value of the subject-matter of the offence does not exceed five thousand dollars.</p></li></ul></li><li><p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Minimum punishment</p><p class="Subsection" id="122433"><span class="lawlabel">(1.1)</span>&nbsp;When a person is prosecuted on indictment and convicted of one or more offences referred to in subsection (1), the court that imposes the sentence shall impose a minimum punishment of imprisonment for a term of two years if the total value of the subject-matter of the offences exceeds one million dollars.</p></li><li><p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Affecting public market</p><p class="Subsection" id="122435"><span class="lawlabel">(2)</span>&nbsp;Every one who, by deceit, falsehood or other fraudulent means, whether or not it is a false pretence within the meaning of this Act, with intent to defraud, affects the public market price of stocks, shares, merchandise or anything that is offered for sale to the public is guilty of an indictable offence and liable to imprisonment for a term not exceeding fourteen years.</p></li></ul>
<div class="HistoricalNote"><ul class="HistoricalNote"><li class="HistoricalNoteSubItem">R.S., 1985, c. C-46, s. 380</li><li class="HistoricalNoteSubItem"> R.S., 1985, c. 27 (1st Supp.), s. 54</li><li class="HistoricalNoteSubItem"> 1994, c. 44, s. 25</li><li class="HistoricalNoteSubItem"> 1997, c. 18, s. 26</li><li class="HistoricalNoteSubItem"> 2004, c. 3, s. 2</li><li class="HistoricalNoteSubItem"> 2011, c. 6, s. 2</li></ul></div>


##### Components:
- Marginal Note: "Fraud" (text from MarginalNote > span)
- Section ID: "122425" (unique identifier)
- Section Number: "380" (from sectionLabel span)
- Subsections:
  1. First Subsection (ID: "122427"):
     - Number: "(1)" (from lawlabel span)
     - Content: "Every one who, by deceit, falsehood or other fraudulent means, whether or not it is a false pretence within the meaning of this Act, defrauds the public or any person, whether ascertained or not, of any property, money or valuable security or any service,"
     - Provision List:
       - Item A (ID: "122428"): "is guilty of an indictable offence and liable to a term of imprisonment not exceeding fourteen years, where the subject-matter of the offence is a testamentary instrument or the value of the subject-matter of the offence exceeds five thousand dollars; or"
       - Item B (ID: "122429"): "is guilty"
         - Sub-item i (ID: "122430"): "of an indictable offence and is liable to imprisonment for a term not exceeding two years, or"
         - Sub-item ii (ID: "122431"): "of an offence punishable on summary conviction,"
         - Continued Paragraph (ID: "122432"): "where the value of the subject-matter of the offence does not exceed five thousand dollars."

  2. Second Subsection (ID: "122433"):
     - Marginal Note: "Minimum punishment"
     - Number: "(1.1)" (from lawlabel span)
     - Content: "When a person is prosecuted on indictment and convicted of one or more offences referred to in subsection (1), the court that imposes the sentence shall impose a minimum punishment of imprisonment for a term of two years if the total value of the subject-matter of the offences exceeds one million dollars."

  3. Third Subsection (ID: "122435"):
     - Marginal Note: "Affecting public market"
     - Number: "(2)" (from lawlabel span)
     - Content: "Every one who, by deceit, falsehood or other fraudulent means, whether or not it is a false pretence within the meaning of this Act, with intent to defraud, affects the public market price of stocks, shares, merchandise or anything that is offered for sale to the public is guilty of an indictable offence and liable to imprisonment for a term not exceeding fourteen years."

- Historical Notes:
  - "R.S., 1985, c. C-46, s. 380"
  - "R.S., 1985, c. 27 (1st Supp.), s. 54"
  - "1994, c. 44, s. 25"
  - "1997, c. 18, s. 26"
  - "2004, c. 3, s. 2"
  - "2011, c. 6, s. 2"

- HTML Classes: ["MarginalNote", "Section", "ProvisionList", "Subsection", "Paragraph", "Subparagraph", "ContinuedParagraph", "HistoricalNote", "HistoricalNoteSubItem"]
- Special Features:
  - Nested provision list structure with two levels (a/b and i/ii)
  - ContinuedParagraph for extended paragraph content
  - Multiple subsection-specific marginal notes
  - Multiple historical notes
  - Lawlabel elements for list markers

#### 2.4.3 Section with Subsections - In-line Definitions

##### Example:
<p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Sabotage</p>
<ul class="Section ProvisionList" id="115955"><li><p class="Subsection" id="115957"><strong><a class="sectionLabel" id="s-52"><span class="sectionLabel">52</span></a></strong>&nbsp;<span class="lawlabel">(1)</span>&nbsp;Every person is guilty of an indictable offence and liable to imprisonment for a term of not more than 10 years or is guilty of an offence punishable on summary conviction who does a prohibited act with the intent to endanger</p><ul class="ProvisionList"><li><p class="Paragraph" id="115958"><span class="lawlabel">(a)</span>&nbsp;the safety, security or defence of Canada, or</p></li><li><p class="Paragraph" id="1201751"><span class="lawlabel">(b)</span>&nbsp;the safety or security of the naval, army or air forces of any state other than Canada that are lawfully present in Canada.</p></li></ul></li><li><p class="MarginalNoteDefinedTerm">Definition of <span class="DefinedTerm"><dfn>prohibited act</dfn></span></p><p class="Subsection" id="115961"><span class="lawlabel">(2)</span>&nbsp;In this section, <span class="DefinedTerm"><dfn>prohibited act</dfn></span> means an act or omission that</p><ul class="ProvisionList"><li><p class="Paragraph" id="115963"><span class="lawlabel">(a)</span>&nbsp;impairs the efficiency or impedes the working of any vessel, vehicle, aircraft, machinery, apparatus or other thing; or</p></li><li><p class="Paragraph" id="115964"><span class="lawlabel">(b)</span>&nbsp;causes property, by whomever it may be owned, to be lost, damaged or destroyed.</p></li></ul></li><li><p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Saving</p><p class="Subsection" id="115965"><span class="lawlabel">(3)</span>&nbsp;No person does a prohibited act within the meaning of this section by reason only that</p><ul class="ProvisionList"><li><p class="Paragraph" id="115967"><span class="lawlabel">(a)</span>&nbsp;he stops work as a result of the failure of his employer and himself to agree on any matter relating to his employment;</p></li><li><p class="Paragraph" id="115968"><span class="lawlabel">(b)</span>&nbsp;he stops work as a result of the failure of his employer and a bargaining agent acting on his behalf to agree on any matter relating to his employment; or</p></li><li><p class="Paragraph" id="115969"><span class="lawlabel">(c)</span>&nbsp;he stops work as a result of his taking part in a combination of workmen or employees for their own reasonable protection as workmen or employees.</p></li></ul></li><li><p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Idem</p><p class="Subsection" id="115970"><span class="lawlabel">(4)</span>&nbsp;No person does a prohibited act within the meaning of this section by reason only that he attends at or near or approaches a dwelling-house or place for the purpose only of obtaining or communicating information.</p></li><li><p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>For greater certainty</p><p class="Subsection" id="1486981"><span class="lawlabel">(5)</span>&nbsp;For greater certainty, no person commits an offence under subsection (1) if they do a prohibited act while participating in advocacy, protest or dissent but they do not intend to cause any of the harms referred to in paragraphs (1)(a) and (b).</p></li></ul>
<div class="HistoricalNote"><ul class="HistoricalNote"><li class="HistoricalNoteSubItem">R.S., 1985, c. C-46, s. 52</li><li class="HistoricalNoteSubItem"><a href="#1146312-1201753" aria-controls="centred-popup" class="wb-lbx wb-init wb-data-ajax-after-inited wb-lbx-inited" role="button" data-ajax-after="1146312-1201753.html" id="wb-auto-16">2019, c. 25, s. 6</a><section id="1146312-1201753" class="mfp-hide modal-dialog modal-content overlay-def"><header class="modal-header"><h2 class="modal-title">2019, c. 25, s. 6</h2></header><div class="modal-body"><ul class="Section ProvisionList" id="1146312"><li><p class="Subsection amending" id="1146313"><strong><a class="sectionLabel" id="s-6"><span class="sectionLabel">6</span></a></strong>&nbsp;<span class="lawlabel">(1)</span>&nbsp;The portion of subsection 52(1) of the Act before paragraph (a) is replaced by the following:</p><section><div class="AmendedText"><p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Sabotage</p><ul class="Section ProvisionList" id=""><li><p class="Subsection"><strong>52</strong>&nbsp;<span class="lawlabel">(1)</span>&nbsp;Every person is guilty of an indictable offence and liable to imprisonment for a term of not more than 10 years or is guilty of an offence punishable on summary conviction who does a prohibited act for a purpose prejudicial to</p></li></ul></div></section></li><li><p class="Subsection amending" id="1146315"><span class="lawlabel">(2)</span>&nbsp;The portion of subsection 52(1) of the English version of the Act after paragraph (b) is repealed.</p></li></ul></div></section></li><li class="HistoricalNoteSubItem"><a href="#1460944-1486983" aria-controls="centred-popup" class="wb-lbx wb-init wb-data-ajax-after-inited wb-lbx-inited" role="button" data-ajax-after="1460944-1486983.html" id="wb-auto-17">2024, c. 16, s. 60</a><section id="1460944-1486983" class="mfp-hide modal-dialog modal-content overlay-def"><header class="modal-header"><h2 class="modal-title">2024, c. 16, s. 60</h2></header><div class="modal-body"><ul class="Section ProvisionList" id="1460944"><li><p class="Subsection amending" id="1460945"><strong><a class="sectionLabel" id="s-60"><span class="sectionLabel">60</span></a></strong>&nbsp;<span class="lawlabel">(1)</span>&nbsp;The portion of subsection 52(1) of the <cite class="XRefExternalAct">Criminal Code</cite> before paragraph (a) is replaced by the following:</p><section><div class="AmendedText"><p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Sabotage</p><ul class="Section ProvisionList" id=""><li><p class="Subsection"><strong>52</strong>&nbsp;<span class="lawlabel">(1)</span>&nbsp;Every person is guilty of an indictable offence and liable to imprisonment for a term of not more than 10 years or is guilty of an offence punishable on summary conviction who does a prohibited act with the intent to endanger</p></li></ul></div></section></li><li><p class="Subsection amending" id="1460947"><span class="lawlabel">(2)</span>&nbsp;Section 52 of the Act is amended by adding the following after subsection (4):</p><section><div class="AmendedText"><ul class="Section ProvisionList" id=""><li><p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>For greater certainty</p><p class="Subsection"><span class="lawlabel">(5)</span>&nbsp;For greater certainty, no person commits an offence under subsection (1) if they do a prohibited act while participating in advocacy, protest or dissent but they do not intend to cause any of the harms referred to in paragraphs (1)(a) and (b).</p></li></ul></div></section></li></ul></div></section></li></ul></div>

##### Components:
- Marginal Note: "Sabotage" (text from MarginalNote > span)
- Section ID: "115955" (unique identifier)
- Section Number: "52" (from sectionLabel span)
- Subsections:
  1. First Subsection (ID: "115957"):
     - Number: "(1)" (from lawlabel span)
     - Content: "Every person is guilty of an indictable offence and liable to imprisonment for a term of not more than 10 years or is guilty of an offence punishable on summary conviction who does a prohibited act with the intent to endanger"
     - Provision List:
       - Item A (ID: "115958"): "the safety, security or defence of Canada, or"
       - Item B (ID: "1201751"): "the safety or security of the naval, army or air forces of any state other than Canada that are lawfully present in Canada."

  2. Second Subsection (ID: "115961"):
     - Marginal Note: "Definition of prohibited act"
     - Number: "(2)" (from lawlabel span)
     - Defined Term: "prohibited act"
     - Definition: "means an act or omission that"
     - Provision List:
       - Item A (ID: "115963"): "impairs the efficiency or impedes the working of any vessel, vehicle, aircraft, machinery, apparatus or other thing; or"
       - Item B (ID: "115964"): "causes property, by whomever it may be owned, to be lost, damaged or destroyed."

  3. Third Subsection (ID: "115965"):
     - Marginal Note: "Saving"
     - Number: "(3)" (from lawlabel span)
     - Content: "No person does a prohibited act within the meaning of this section by reason only that"
     - Provision List:
       - Item A (ID: "115967"): "he stops work as a result of the failure of his employer and himself to agree on any matter relating to his employment;"
       - Item B (ID: "115968"): "he stops work as a result of the failure of his employer and a bargaining agent acting on his behalf to agree on any matter relating to his employment; or"
       - Item C (ID: "115969"): "he stops work as a result of his taking part in a combination of workmen or employees for their own reasonable protection as workmen or employees."

  4. Fourth Subsection (ID: "115970"):
     - Marginal Note: "Idem"
     - Number: "(4)" (from lawlabel span)
     - Content: "No person does a prohibited act within the meaning of this section by reason only that he attends at or near or approaches a dwelling-house or place for the purpose only of obtaining or communicating information."

  5. Fifth Subsection (ID: "1486981"):
     - Marginal Note: "For greater certainty"
     - Number: "(5)" (from lawlabel span)
     - Content: "For greater certainty, no person commits an offence under subsection (1) if they do a prohibited act while participating in advocacy, protest or dissent but they do not intend to cause any of the harms referred to in paragraphs (1)(a) and (b)."

- Historical Notes:
  - Primary: "R.S., 1985, c. C-46, s. 52"
  - Amendments:
    1. "2019, c. 25, s. 6" (with modal popup containing amendment details)
    2. "2024, c. 16, s. 60" (with modal popup containing amendment details)

- HTML Classes: ["MarginalNote", "Section", "ProvisionList", "Subsection", "Paragraph", "DefinedTerm", "MarginalNoteDefinedTerm", "HistoricalNote", "HistoricalNoteSubItem"]
- Special Features:
  - In-line definition in subsection (2)
  - Multiple historical notes with interactive amendment links
  - Modal popups for amendment details
  - Multiple subsection-specific marginal notes



#### 2.4.4 Section with Subsections - Indented Definitions  
- This example does not have continued section content after the definition list, but it could, similar to 
##### Example:  
<p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Counterfeiting stamp, etc.</p>
<ul class="Section ProvisionList" id="122374"><li><p class="Subsection" id="122376"><strong><a class="sectionLabel" id="s-376"><span class="sectionLabel">376</span></a></strong>&nbsp;<span class="lawlabel">(1)</span>&nbsp;Every person is guilty of an indictable offence and liable to imprisonment for a term of not more than 14 years who</p><ul class="ProvisionList"><li><p class="Paragraph" id="122377"><span class="lawlabel">(a)</span>&nbsp;fraudulently uses, mutilates, affixes, removes or counterfeits a stamp or part thereof,</p></li><li><p class="Paragraph" id="122378"><span class="lawlabel">(b)</span>&nbsp;knowingly and without lawful excuse has in their possession</p><ul class="ProvisionList"><li><p class="Subparagraph" id="122379"><span class="lawlabel">(i)</span>&nbsp;a counterfeit stamp or a stamp that has been fraudulently mutilated, or</p></li><li><p class="Subparagraph" id="122380"><span class="lawlabel">(ii)</span>&nbsp;anything bearing a stamp of which a part has been fraudulently erased, removed or concealed, or</p></li></ul></li><li><p class="Paragraph" id="122381"><span class="lawlabel">(c)</span>&nbsp;without lawful excuse makes or knowingly has in their possession a die or instrument that is capable of making the impression of a stamp or part of a stamp.</p></li></ul></li><li><p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Counterfeiting mark</p><p class="Subsection" id="122382"><span class="lawlabel">(2)</span>&nbsp;Every one who, without lawful authority,</p><ul class="ProvisionList"><li><p class="Paragraph" id="122384"><span class="lawlabel">(a)</span>&nbsp;makes a mark,</p></li><li><p class="Paragraph" id="122385"><span class="lawlabel">(b)</span>&nbsp;sells, or exposes for sale, or has in his possession a counterfeit mark,</p></li><li><p class="Paragraph" id="122386"><span class="lawlabel">(c)</span>&nbsp;affixes a mark to anything that is required by law to be marked, branded, sealed or wrapped other than the thing to which the mark was originally affixed or was intended to be affixed, or</p></li><li><p class="Paragraph" id="122387"><span class="lawlabel">(d)</span>&nbsp;affixes a counterfeit mark to anything that is required by law to be marked, branded, sealed or wrapped,</p></li></ul><p class="ContinuedSectionSubsection" id="122388">is guilty of an indictable offence and liable to imprisonment for a term not exceeding fourteen years.</p></li><li><p class="MarginalNote"><span class="wb-invisible">Marginal note:</span>Definitions</p><p class="Subsection" id="122389"><span class="lawlabel">(3)</span>&nbsp;In this section,</p><dl class="Definition"><dt id="122391"><span class="DefinedTerm"><dfn>mark</dfn></span></dt><dd><p class="Definition"><span class="DefinedTerm"><dfn>mark</dfn></span> means a mark, brand, seal, wrapper or design used by or on behalf of</p><ul class="ProvisionList"><li><p class="Paragraph" id="122392"><span class="lawlabel">(a)</span>&nbsp;the government of Canada or a province,</p></li><li><p class="Paragraph" id="122393"><span class="lawlabel">(b)</span>&nbsp;the government of a state other than Canada, or</p></li><li><p class="Paragraph" id="122394"><span class="lawlabel">(c)</span>&nbsp;any department, board, commission or agent established by a government mentioned in paragraph (a) or (b) in connection with the service or business of that government; (<span class="DefinedTermLink" lang="fr">marque</span>)</p></li></ul></dd><dt id="122395"><span class="DefinedTerm"><dfn>stamp</dfn></span></dt><dd><p class="Definition"><span class="DefinedTerm"><dfn>stamp</dfn></span> means an impressed or adhesive stamp used for the purpose of revenue by the government of Canada or a province or by the government of a state other than Canada. (<span class="DefinedTermLink" lang="fr">timbre</span>)</p></dd></dl></li></ul>
<div class="HistoricalNote"><ul class="HistoricalNote"><li class="HistoricalNoteSubItem">R.S., 1985, c. C-46, s. 376</li><li class="HistoricalNoteSubItem"> 2018, c. 29, s. 43</li></ul></div>

##### Components:
- Marginal Note: "Counterfeiting stamp, etc." (text from MarginalNote > span)
- Section ID: "122374" (unique identifier)
- Section Number: "376" (from sectionLabel span)
- Subsections:
  1. First Subsection (ID: "122376"):
     - Number: "(1)" (from lawlabel span)
     - Content: "Every person is guilty of an indictable offence and liable to imprisonment for a term of not more than 14 years who"
     - Provision List:
       - Item A (ID: "122377"): "fraudulently uses, mutilates, affixes, removes or counterfeits a stamp or part thereof,"
       - Item B (ID: "122378"): "knowingly and without lawful excuse has in their possession"
         - Sub-item i (ID: "122379"): "a counterfeit stamp or a stamp that has been fraudulently mutilated, or"
         - Sub-item ii (ID: "122380"): "anything bearing a stamp of which a part has been fraudulently erased, removed or concealed, or"
       - Item C (ID: "122381"): "without lawful excuse makes or knowingly has in their possession a die or instrument that is capable of making the impression of a stamp or part of a stamp."

  2. Second Subsection (ID: "122382"):
     - Marginal Note: "Counterfeiting mark"
     - Number: "(2)" (from lawlabel span)
     - Content: "Every one who, without lawful authority,"
     - Provision List:
       - Item A (ID: "122384"): "makes a mark,"
       - Item B (ID: "122385"): "sells, or exposes for sale, or has in his possession a counterfeit mark,"
       - Item C (ID: "122386"): "affixes a mark to anything that is required by law to be marked, branded, sealed or wrapped other than the thing to which the mark was originally affixed or was intended to be affixed, or"
       - Item D (ID: "122387"): "affixes a counterfeit mark to anything that is required by law to be marked, branded, sealed or wrapped,"
     - Continued Content (ID: "122388"): "is guilty of an indictable offence and liable to imprisonment for a term not exceeding fourteen years."

  3. Third Subsection (ID: "122389"):
     - Marginal Note: "Definitions"
     - Number: "(3)" (from lawlabel span)
     - Content: "In this section,"
     - Definitions:
       1. First Term (ID: "122391"):
          - Term: "mark"
          - Definition: "means a mark, brand, seal, wrapper or design used by or on behalf of"
          - Provision List:
            - Item A (ID: "122392"): "the government of Canada or a province,"
            - Item B (ID: "122393"): "the government of a state other than Canada, or"
            - Item C (ID: "122394"): "any department, board, commission or agent established by a government mentioned in paragraph (a) or (b) in connection with the service or business of that government;"
          - French Term: "marque"

       2. Second Term (ID: "122395"):
          - Term: "stamp"
          - Definition: "means an impressed or adhesive stamp used for the purpose of revenue by the government of Canada or a province or by the government of a state other than Canada."
          - French Term: "timbre"

- Historical Notes:
  - "R.S., 1985, c. C-46, s. 376"
  - "2018, c. 29, s. 43"

- HTML Classes: ["MarginalNote", "Section", "ProvisionList", "Subsection", "Paragraph", "Subparagraph", "ContinuedSectionSubsection", "Definition", "DefinedTerm", "DefinedTermLink", "HistoricalNote", "HistoricalNoteSubItem"]
- Special Features:
  - Nested provision list structure with two levels
  - Definition list with bilingual terms
  - Multiple subsection-specific marginal notes
  - ContinuedSectionSubsection for extended content
  - Lawlabel elements for list markers

## 3. Metadata
- The Criminal Code HTML contains important metadata both at the document level and within specific sections.

### 3.1 Document Metadata
Key metadata elements that should be present and validated:

#### Required Meta Tags
<meta name="dcterms.title" content="Consolidated federal laws of Canada, Criminal Code" />
<meta name="dcterms.creator" title="Department of Justice" content="Legislative Services Branch" />
<meta name="dcterms.issued" title="W3CDTF" content="2024-01-14" />
<meta name="dcterms.modified" title="W3CDTF" content="2024-01-14" />
<meta name="dcterms.language" title="ISO639-2" content="eng" />

### 3.2 Section Cross-References

Section labels are clickable links that allow navigation between related sections. They follow a consistent pattern:

#### Example:
<strong><a class="sectionLabel" id="s-23.1"><span class="sectionLabel">23.1</span></a></strong>

##### Components:
- Link Element:
  - Class: "sectionLabel"
  - ID Format: "s-{section_number}" (e.g., "s-23.1")
  - Contains: span element with section number text
- HTML Structure:
  - Wrapped in <strong> tags
  - Uses non-breaking space (&nbsp;) after the link
- Special Features:
  - Consistent across all section types (base, lists, definitions, subsections)
  - Always precedes the main section content
  - Can be referenced in other sections' content via same ID format


  