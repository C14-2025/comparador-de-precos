from playwright.sync_api import sync_playwright
from .base import BaseCrawler
import urllib.parse

class AmazonCrawler(BaseCrawler):
    def search(self, query: str):
        q = urllib.parse.quote(query)
        url = f"https://www.amazon.com.br/s?k={q}"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            page.wait_for_selector("div.s-result-item[data-component-type='s-search-result']")

            products = page.query_selector_all("div.s-result-item[data-component-type='s-search-result']")[:10]

            results = [{"html": p.inner_html()} for p in products]
            browser.close()

        self.save_json(results, "amazon")
        return results
