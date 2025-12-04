import json
import requests

class SageRemote:
    def __init__(self, url: str ="https://sagecell.sagemath.org/service", timeout: int = 20):
        self.url: str = url
        self.timeout: int = timeout

    def run_code(self, code: str):
        payload = {"code": code}
        headers = {"Content-Type": "application/json"}

        try:
            response = requests.post(self.url, data=json.dumps(payload), headers=headers, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            return data.get("stdout", "").strip()
        except Exception as e:
            print("Помилка при виконанні коду на SageMathCell:", e)
            return None
