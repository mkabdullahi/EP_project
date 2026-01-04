# EP Scraper

A Python-based scraper for European Parliament texts adopted, using Playwright for browser automation.

## Description

This project automates the scraping of the European Parliament's "Texts Adopted" page (https://www.europarl.europa.eu/plenary/en/texts-adopted.html). It extracts detailed metadata for each document, including titles, references, links to PDFs and Docx files, publication dates, and more. The scraper handles pagination to collect all available results and outputs structured JSON data.

## Features

- **Comprehensive Data Extraction**: Scrapes plenary documents with fields like source, inter-institutional code, document reference, latest EP document name, legal document type, PDF/Docx links, published date, and parsed date.
- **Pagination Support**: Automatically navigates through multiple pages of results.
- **Dynamic Content Handling**: Manages cookies, expandable sections, and date filters.
- **JSON Output**: Produces clean JSON for further processing.
- **Webhook Integration**: Posts data to an n8n webhook if configured.
- **CI/CD Ready**: Includes GitHub Actions workflow for automated runs.
- **Error Handling**: Graceful fallbacks and debug logging.

## Installation

1. Clone the repository:
   ```
   git clone <repo-url>
   cd EP_project
   ```

2. Install Python dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```
   playwright install
   ```

## Usage

Run the scraper locally:
```
python3 scraper.py
```

The script will:
- Launch a browser (headless by default in CI)
- Navigate to the EP texts adopted page
- Accept cookies
- Expand "More options"
- Apply a date filter (default: 01/07/2025)
- Search and extract data
- Handle pagination
- Output JSON to console
- Post to webhook if `N8N_WEBHOOK_URL` is set

### Configuration

- **Date Filter**: Edit the date in `scraper.py`: `page.fill("input[name='refSittingDateStart']", "01/07/2025")`
- **Webhook**: Set environment variable `N8N_WEBHOOK_URL` to your n8n endpoint URL.
- **Headless Mode**: Change `headless=False` to `True` for production runs.

### Output Example

```json
[
  {
    "Source": "Plenary",
    "Inter-institutional code": "2025/3025(RSP)",
    "Document reference": "P10_TA(2025)0345",
    "Latest EP document name": "European Parliament resolution of 18 December 2025 on the continuous Belarusian hybrid attacks against Lithuania",
    "Legal document type": "resolution",
    "Latest EP PDF link": "https://www.europarl.europa.eu/doceo/document/TA-10-2025-0345_EN.pdf",
    "Latest EP Docx link": "https://www.europarl.europa.eu/doceo/document/TA-10-2025-0345_EN.docx",
    "Published Date": "18-DEC-2025",
    "Date when first parsed": "01-APR-2026",
    "Note": "",
    "New document": "",
    "Document typology": "",
    "Typology confidence level": "",
    "Report summary": ""
  }
]
```

## CI/CD

The project includes a GitHub Actions workflow (`.github/workflows/scrape.yml`) that runs the scraper on Ubuntu with Playwright. It can be triggered manually or on a schedule.

To trigger manually:
- Go to GitHub Actions tab
- Select "EP Scraper" workflow
- Click "Run workflow"

## Dependencies

- Python 3.8+
- Playwright
- Requests

## License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License. You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the specific language governing permissions and limitations under the License.
