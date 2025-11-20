import os
import json

class BaseCrawler:
    def save_json(self, data, filename):
        os.makedirs("app/json_temp", exist_ok=True)
        with open(f"app/json_temp/{filename}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
