import requests

class SegAIChat(object):
    def __init__(self, db_name):
        self.db_name = db_name


    def get_sample_prompts(self):
        try:
            url = 'http://ds.moeinternal.com/v1/ds/seg-ai-chat/prompts/sample'
            headers = {
                'MOE-DBNAME': self.db_name
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            data = response.json()  # Parse the JSON response
            processed_data = {"sample-prompts": data.get("sample_prompts", {})}
            return processed_data
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return {}

    def generate_filter(self, prompt,regenerate = False):
        try:
            url = 'http://ds.moeinternal.com/v1/ds/seg-ai-chat/generate-segment'
            headers = {
                'MOE-DBNAME': self.db_name,
                'Content-Type': 'application/json'
            }
            data = {
                "prompt": prompt,
                "regenerate": regenerate
            }
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()  # Raise an exception for bad status codes
            return response.json()  # Parse the JSON response
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")
            return {}
