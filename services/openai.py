import requests
import time


class ChatAPI:
    def __init__(self, api_url, api_key):
        self.api_url = api_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        }

    def send_message(self, model, messages):
        data = {"model": model, "messages": messages, "stream": False}
        response = requests.post(self.api_url, headers=self.headers, json=data)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def retry_on_failure(self, func, retries=3, delay=10):
        for attempt in range(1, retries + 1):
            try:
                return func()
            except requests.exceptions.RequestException as e:
                print(f"\nError: {e}. Retrying in {delay} seconds ({attempt}/{retries})...")
            except KeyError as e:
                print(f"\nUnexpected response format: {e}. Retrying in {delay} seconds ({attempt}/{retries})...")

            for sec in range(delay, 0, -1):
                print(f"\rRetrying in {sec} seconds...", end="", flush=True)
                time.sleep(1)

        print("\nAll retries exhausted. Skipping.")
        return None