import requests
from bs4 import BeautifulSoup
import urllib.parse
from .base import BaseCrawler

class MercadoLivreCrawler(BaseCrawler):
    def search(self, query: str):
        q = urllib.parse.quote(query)
        url = f"https://lista.mercadolivre.com.br/{q}"

        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept-Language": "pt-BR,pt;q=0.9"
        }

        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.text, "html.parser")

        selector = "li.ui-search-layout__item"
        products = soup.select(selector)[:10]

        results = [{"html": str(p)} for p in products]
        self.save_json(results, "mercado_livre")
        return results
