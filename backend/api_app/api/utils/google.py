import json
from google.cloud import pubsub_v1
from api_app.api.core.config import settings


class GooglePubSubClient:
    def __init__(self):
        try:
            self.publisher = pubsub_v1.PublisherClient()
            self.project_id = settings.GCP_PROJECT_ID
        except Exception as e:
            print(
                f"⚠️ Warning: Google Cloud Credentials not found. Pub/Sub will not work. ({e})"
            )
            self.publisher = None

    def publish_message(self, topic_name: str, data: dict) -> str:
        if not self.publisher:
            print("❌ Error: Publisher not initialized.")
            return None
        topic_path = self.publisher.topic_path(self.project_id, topic_name)
        message_json = json.dumps(data)
        message_bytes = message_json.encode("utf-8")
        future = self.publisher.publish(topic_path, data=message_bytes)
        try:
            message_id = future.result(timeout=5)
            print(f"✅ Published message to {topic_name}: {message_id}")
            return message_id
        except Exception as e:
            print(f"❌ Failed to publish message: {e}")
            raise e


pubsub_client = GooglePubSubClient()
