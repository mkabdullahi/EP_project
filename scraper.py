import json
import os
import re
from datetime import datetime
import requests
from playwright.sync_api import sync_playwright

def scrape_ep():
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,  # UI first for debugging
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-accelerated-2d-canvas",
                    "--no-first-run",
                    "--no-zygote",
                    "--disable-gpu"
                ]
            )
            page = browser.new_page()

            print("Navigating to the page...")
            page.goto("https://www.europarl.europa.eu/plenary/en/texts-adopted.html")
            page.wait_for_load_state("networkidle")

            # Try to accept cookies - adjust selector if needed
            try:
                page.click("text=I accept analytics cookies", timeout=5000)
                print("Accepted cookies.")
            except:
                print("Cookie button not found or already accepted.")

            page.wait_for_timeout(2000)  # Brief wait for any dynamic content

            # Try to expand "More Options" - target the visible h4
            try:
                page.wait_for_selector("h4.expand_collapse_closed:has-text('More options')", state="visible", timeout=10000)
                page.click("h4.expand_collapse_closed:has-text('More options')")
                print("Expanded More options.")
            except Exception as e:
                print(f"Could not expand More options: {e}. Proceeding without filtering.")

            # Try to fill date and search - adjust button selector
            try:
                page.fill("input[name='refSittingDateStart']", "01/07/2025")
                page.click("input#sidesButtonSubmit")
                page.wait_for_load_state("networkidle")
                print("Applied date filter and searched.")
            except Exception as e:
                print(f"Could not apply filter: {e}. Extracting default results.")

            # Extract entries - results are in div.notice
            print("Extracting data...")
            items = page.query_selector_all("div.notice")
            print(f"Found {len(items)} items.")

            parsed_date = datetime.now().strftime("%d-%b-%Y").upper()  # e.g., 01-APR-2026

            for item in items:
                # Full title from p.details
                details_elem = item.query_selector("p.details")
                full_title = details_elem.inner_text().strip() if details_elem else ""
                if not full_title:
                    continue

                # Document reference from span.reference
                ref_elem = item.query_selector("span.reference")
                doc_ref = ref_elem.inner_text().strip() if ref_elem else ""

                # Latest EP document name: full_title without bracketed code at end
                doc_name = re.sub(r'\s*\([^)]*\)\s*$', '', full_title)

                # Inter-institutional code: extract from full_title
                inter_code_match = re.search(r'(\d{4}/\d{4}\([A-Z]+\))', full_title)
                inter_code = inter_code_match.group(1) if inter_code_match else ""

                # Legal document type: between "European Parliament" and "of [Date]" or "adopted by"
                type_match = re.search(r'European Parliament (.*?)(?: of \d| adopted by)', full_title, re.IGNORECASE)
                doc_type = type_match.group(1).strip() if type_match else ""

                # PDF link from a.link_pdf
                pdf_elem = item.query_selector("a.link_pdf")
                pdf_url = pdf_elem.get_attribute("href") if pdf_elem else ""

                # Docx link from a.link_doc
                docx_elem = item.query_selector("a.link_doc")
                docx_url = docx_elem.get_attribute("href") if docx_elem else ""

                # Published Date from span.date, convert format
                date_elem = item.query_selector("span.date")
                pub_date_raw = date_elem.inner_text().replace("Date :", "").strip() if date_elem else ""
                pub_date = ""
                if pub_date_raw:
                    try:
                        # Assuming DD-MM-YYYY, convert to DD-MMM-YYYY
                        dt = datetime.strptime(pub_date_raw, "%d-%m-%Y")
                        pub_date = dt.strftime("%d-%b-%Y").upper()
                    except:
                        pub_date = pub_date_raw  # Keep as is if format fails

                results.append({
                    "Source": "Plenary",
                    "Inter-institutional code": inter_code,
                    "Document reference": doc_ref,
                    "Latest EP document name": doc_name,
                    "Legal document type": doc_type,
                    "Latest EP PDF link": pdf_url,
                    "Latest EP Docx link": docx_url,
                    "Published Date": pub_date,
                    "Date when first parsed": parsed_date,
                    # Empty fields as per instructions
                    "Note": "",
                    "New document": "",
                    "Document typology": "",
                    "Typology confidence level": "",
                    "Report summary": ""
                })

            # Handle pagination
            page_num = 1
            while True:
                next_btn = page.query_selector("a:has-text('Next'), button:has-text('Next')")
                if next_btn:
                    print(f"Loading page {page_num + 1}...")
                    next_btn.click()
                    page.wait_for_load_state("networkidle")
                    page_num += 1
                    # Extract from new page using same logic
                    items = page.query_selector_all("div.notice")
                    for item in items:
                        details_elem = item.query_selector("p.details")
                        full_title = details_elem.inner_text().strip() if details_elem else ""
                        if not full_title:
                            continue
                        ref_elem = item.query_selector("span.reference")
                        doc_ref = ref_elem.inner_text().strip() if ref_elem else ""
                        doc_name = re.sub(r'\s*\([^)]*\)\s*$', '', full_title)
                        inter_code_match = re.search(r'(\d{4}/\d{4}\([A-Z]+\))', full_title)
                        inter_code = inter_code_match.group(1) if inter_code_match else ""
                        type_match = re.search(r'European Parliament (.*?)(?: of \d| adopted by)', full_title, re.IGNORECASE)
                        doc_type = type_match.group(1).strip() if type_match else ""
                        pdf_elem = item.query_selector("a.link_pdf")
                        pdf_url = pdf_elem.get_attribute("href") if pdf_elem else ""
                        docx_elem = item.query_selector("a.link_doc")
                        docx_url = docx_elem.get_attribute("href") if docx_elem else ""
                        date_elem = item.query_selector("span.date")
                        pub_date_raw = date_elem.inner_text().replace("Date :", "").strip() if date_elem else ""
                        pub_date = ""
                        if pub_date_raw:
                            try:
                                dt = datetime.strptime(pub_date_raw, "%d-%m-%Y")
                                pub_date = dt.strftime("%d-%b-%Y").upper()
                            except:
                                pub_date = pub_date_raw
                        results.append({
                            "Source": "Plenary",
                            "Inter-institutional code": inter_code,
                            "Document reference": doc_ref,
                            "Latest EP document name": doc_name,
                            "Legal document type": doc_type,
                            "Latest EP PDF link": pdf_url,
                            "Latest EP Docx link": docx_url,
                            "Published Date": pub_date,
                            "Date when first parsed": parsed_date,
                            "Note": "",
                            "New document": "",
                            "Document typology": "",
                            "Typology confidence level": "",
                            "Report summary": ""
                        })
                else:
                    break

            browser.close()
            print(f"Extraction complete. Found {len(results)} items.")
    except Exception as e:
        print(f"Error during scraping: {e}")
        # Return whatever was extracted so far

    return results

if __name__ == "__main__":
    data = scrape_ep()
    print(json.dumps(data, indent=2))
    # 5. Push data back to n8n Webhook
    webhook_url = os.getenv("N8N_WEBHOOK_URL")
    if webhook_url and data:
         response = requests.post(webhook_url, json=data)
         print(f"Posted data to webhook, response status: {response.status_code}")
    else:
        print("No webhook URL set, skipping webhook post.")
