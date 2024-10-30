# app2.0

### Notes for Self

## Terminal Commands

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install requirements.txt
pip3 install -r requirements.txt

# Git - check current remote repo
git remote -v

# Git 

# app2.0

# Criminal Code Web Application Project Outline
Version: 0.1.0
Last Updated: 2024-03-XX

## Vision
The vision for the web-app is a version of the Criminal Code of Canada built for busy criminal lawyers. The current government website has significant limitations in navigation, aesthetics, UI/UX, scrolling behavior, and mobile responsiveness. This project aims to create a superior alternative while serving as a learning experience in modern web development and LLM integration.

URL of GOV Site: https://laws-lois.justice.gc.ca/eng/acts/c-46/FullText.html

## Backend Architecture

### Flask App
- Python-based RESTful API
- Modular blueprint structure
- CORS handling for frontend integration
- Request validation middleware
- Error handling and logging

### Data Processing
1. **Web Scraping**
   - BeautifulSoup4 for HTML parsing
   - Automated data extraction pipeline
   - Version control for scraped content
   - Data cleaning and normalization
   - Validation against schema

2. **Database Design**
   - PostgreSQL for primary storage
   - Hierarchical data structure
   - JSON support for flexibility
   - Tables:
     - Parts
     - Sections
     - Subsections (recursive)
     - Notes (marginal/historical)

3. **Search Engine**
   - Elasticsearch integration
   - Full-text search capabilities
   - Synchronized with PostgreSQL

### API Design
- RESTful architecture
- Key endpoints:
  - GET /parts
  - GET /sections/:id
  - GET /search
  - POST /notes (future)

### Infrastructure
1. **Caching**
   - Redis implementation
   - In-memory data storage
   - Performance optimization

2. **Load Balancing**
   - Nginx/HAProxy
   - High availability
   - Scalability support

### Security
1. **API Security**
   - Input validation
   - Rate limiting
   - HTTPS implementation

2. **Authentication (Future)**
   - JWT implementation
   - User account management


## Frontend Architecture

### Framework
- Next.js
- TypeScript for type safety
- React Server Components for optimal performance

### Core Layout Components
1. **Main Reading Pane**
   - Vertical scrolling view
   - Continuous page presentation
   - Infinite scroll with lazy loading

2. **Top Bar**
   - Persistent search bar
   - Search results overlay
   - Additional tools (TBD)

3. **Left Sidebar**
   - Expandable, nested table of contents
   - Default view: Parts of Criminal Code
   - Floating behavior during scroll
   - Critical for navigation and user experience

### User Experience Features
1. **Search Functionality**
   - Always-visible search bar
   - Section/subsection result targeting
   - Smooth zoom animation to results
   - Visual feedback for scroll direction
   - Highlight of found terms

2. **Visual Design**
   - Modern, sleek aesthetic
   - Light/dark mode toggle
   - Sans-serif fonts for readability
   - Adjustable font sizing
   - Optimized whitespace and line spacing

3. **Responsive Design**
   - Mobile-first approach
   - Adaptive layouts for all screen sizes
   - Collapsible navigation for mobile
   - Floating UI elements

### Technical Implementation
1. **Performance Optimizations**
   - Infinite scroll implementation
   - Lazy loading of content
   - Async data fetching
   - Content pre-loading
   - Server-side rendering (SSR) for initial load
   - Static site generation (SSG) for static content

2. **Suggested Libraries**
   - Next.js App Router
   - TanStack Query for data fetching
   - Tailwind CSS for styling
   - Framer Motion for animations
   - Zod for schema validation

## Next Steps

### Phase 1: Project Setup and Basic Infrastructure
1. 

### Current Priority


## Version History
- 
