import requests
import data


class APIClient:
    BASE_URL = data.api_url

    def create_post(self, title, body, user_id):
        payload = {
            "title": title,
            "body": body,
            "userId": user_id
        }

        return requests.post(f"{self.BASE_URL}/posts", json=payload)

    def get_post(self, post_id):
        return requests.get(f"{self.BASE_URL}/posts/{post_id}")