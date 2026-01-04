# Troubleshooting & Development History

This scraper was developed iteratively, addressing various challenges. Here's a summary of the end-to-end conversation and fixes:

## Initial Issues
- **Playwright Launch Failure**: SIGSEGV on macOS due to browser installation issues. Fixed by updating Playwright, reinstalling browsers, and adding launch arguments (`--no-sandbox`, etc.).
- **Browser Installation**: Chromium failed initially; resolved by specific `playwright install chromium`.
- **Element Visibility**: "More options" not clickable due to hidden elements. Updated selector to target visible `h4.expand_collapse_closed`.
- **Cookie Banner**: Blocked interactions; added code to accept cookies.
- **Search Button**: Incorrect selector; updated to `input# sidesButtonSubmit`.
- **Data Extraction**: Initially 0 results; fixed selectors to target `div.notice` containers and specific child elements (`p.details`, `span.reference`, etc.).

## Key Fixes Applied
1. **Launch Args**: Added macOS-stable arguments to prevent crashes.
2. **Selectors**: Corrected for "More options" (h4), search button (input# sidesButtonSubmit), and result items (div.notice).
3. **Dynamic Content**: Added waits and try-except for robustness.
4. **Field Parsing**: Implemented regex extraction for codes, types, and date formatting (DD-MM-YYYY to DD-MMM-YYYY).
5. **Pagination**: Added loop to click "Next" and extract from subsequent pages.
6. **Error Handling**: Wrapped operations in try-except to ensure JSON output even on partial failures.

## Testing Tips
- Run with `headless=False` for visual debugging.
- Check browser console for errors.
- Inspect page elements to verify selectors.
- Use `page.wait_for_timeout(5000)` for manual inspection.

If issues persist, inspect the page and update selectors accordingly.
