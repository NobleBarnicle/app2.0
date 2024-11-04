# Criminal Code Web Application Project Outline
Version: 0.1.0
Last Updated: 2024-03-XX

## Vision
The vision for the web-app is a version of the Criminal Code of Canada built for busy criminal lawyers. The current government website has significant limitations in navigation, aesthetics, UI/UX, scrolling behavior, and mobile responsiveness. This project aims to create a superior alternative while serving as a learning experience in modern web development and LLM integration.

URL of GOV Site: https://laws-lois.justice.gc.ca/eng/acts/c-46/FullText.html

Link to Git Repo App2.0: https://github.com/NobleBarnicle/app2.0.git

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

### Phase 1: Data Foundation & Backend Infrastructure
1. **Web Scraping Development**
   - Create Python scraping script using BeautifulSoup4
   - Implement data extraction pipeline
   - Build validation schemas using Zod
   - Set up version control for scraped content
   - Create data cleaning procedures

2. **Database Implementation**
   - Design and implement PostgreSQL schema
   - Create tables for Parts, Sections, Subsections
   - Implement hierarchical relationships
   - Set up data migration scripts
   - Add indexing strategy

3. **Core Flask API**
   - Set up Flask project structure with blueprints
   - Implement database connections
   - Create basic CRUD endpoints
   - Add error handling middleware
   - Set up logging system

4. **Search Infrastructure**
   - Configure Elasticsearch
   - Implement data synchronization with PostgreSQL
   - Create search API endpoints
   - Set up results ranking system

### Phase 2: Frontend Development
1. **Project Setup**
   - Initialize Next.js with TypeScript
   - Configure Tailwind CSS
   - Set up development environment
   - Establish component architecture

2. **Core Components**
   - Implement main reading pane
   - Create navigation sidebar
   - Build persistent top bar
   - Add search interface

3. **User Experience**
   - Implement infinite scroll
   - Add responsive design
   - Create dark mode toggle
   - Set up animations with Framer Motion

### Phase 3: Integration & Optimization
1. **Performance**
   - Implement Redis caching
   - Optimize API responses
   - Add load balancing
   - Set up monitoring

2. **Final Features**
   - Complete search functionality
   - Add font controls
   - Implement mobile optimizations
   - Fine-tune animations

### Current Priority
1. **Development Environment**
   - Configure version control
   - Set up Python virtual environment
   - Install and configure PostgreSQL locally
   - Create documentation structure
   - Establish coding standards
   - Set up linting and formatting tools

2. **Data Collection Infrastructure**
   - Create initial scraping script
   - Design database schema
   - Implement data validation
   - Test scraping on sample pages

## Version History
- 0.1.0 (2024-03-XX): Initial project architecture and backend-first approach defined

## Development Setup

### Environment Configuration
1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Update `.env` with your local configuration values:
   - Generate a secure SECRET_KEY
   - Update POSTGRES_URI with your database credentials
   - Adjust other values as needed

### Database Setup
1. Install PostgreSQL if not already installed:
   ```bash
   # macOS (using Homebrew)
   brew install postgresql
   brew services start postgresql

   # Ubuntu/Debian
   sudo apt-get update
   sudo apt-get install postgresql postgresql-contrib
   ```

2. Create the database:
   ```bash
   createdb criminalcode
   createdb criminalcode_test  # for running tests
   ```

### Running the Application
1. Create and activate virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Unix/macOS
   # or
   .\venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   flask run
   ```

4. Run tests:
   ```bash
   pytest
   ```


# Criminal Code Parser & Database Implementation
### Objective
Create a robust parser and database schema to accurately capture the hierarchical structure of the Criminal Code of Canada, preserving all relationships and metadata while enabling efficient querying.
## Key Requirements
### Parser Requirements
1. Parse HTML structure as documented in parsing_examples.md
2. Handle all component types:
   - Parts with optional subheadings
   - Base sections with marginal notes
   - Sections with nested lists
   - Sections with definitions (both inline and indented)
   - Historical notes and amendments
   - Cross-references
3. Maintain document ordering using section numbers (e.g., 23.1, 23.2) for proper sequencing
### Database Schema Requirements
1. Implement hierarchical relationships:
   - Parts contain sections
   - Sections contain subsections/lists/definitions
   - Support for nested elements (e.g., (a)(i), (a)(ii))
2. Store metadata:
   - Marginal notes
   - Cross-references
   - Bilingual terms for definitions
   - Amendment histories
3. Enable efficient queries for:
   - Full text search
   - Navigation by section number
   - Hierarchical traversal
   - Cross-reference resolution
### Special Considerations
1. Handle malformed HTML gracefully
2. Preserve all relationships between components
3. Support future updates/amendments
4. Enable efficient retrieval for frontend display
5. Maintain bilingual support where applicable
## Deliverables 
1. Python parser using BeautifulSoup4
2. PostgreSQL schema with proper indexing
3. Data validation functions
4. Database population scripts
5. Query optimization strategies