import os
import json
import requests
import urllib.parse
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


class BaseCrawler:
    def save_json(self, data, json_path: str, filename: str):

        os.makedirs(json_path, exist_ok=True)
        caminho_completo = os.path.join(json_path, f"{filename}.json")
        
        with open(caminho_completo, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"Arquivo salvo em: {caminho_completo}")


class AmazonCrawler(BaseCrawler):
    def search(self, query: str, json_path: str):
        
        q = urllib.parse.quote(query)
        url = f"https://www.amazon.com.br/s?k={q}"

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url)

            try:
                page.wait_for_selector("div.s-result-item[data-component-type='s-search-result']", timeout=10000)
                products = page.query_selector_all("div.s-result-item[data-component-type='s-search-result']")[:10]
                results = [{"html": p.inner_html()} for p in products]
            except Exception as e:
                print(f"Erro ao buscar na Amazon: {e}")
                results = []
            finally:
                browser.close()

        self.save_json(data=results, json_path=json_path, filename="amazon")
        return results


class MercadoLivreCrawler(BaseCrawler):
    def search(self, query: str, json_path: str):

        q = urllib.parse.quote(query)
        url = f"https://lista.mercadolivre.com.br/{q}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "pt-BR,pt;q=0.9"
        }

        try:
            r = requests.get(url, headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")

            selector = "li.ui-search-layout__item"
            products = soup.select(selector)[:10]
            results = [{"html": str(p)} for p in products]
        except Exception as e:
            print(f"Erro ao buscar no Mercado Livre: {e}")
            results = []

        self.save_json(data=results, json_path=json_path, filename="mercado_livre")
        return results