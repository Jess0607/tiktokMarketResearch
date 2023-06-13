from dotenv import load_dotenv
import os
from google.cloud import storage


class GoogleStorage:
    def __init__(self, project_id=None):
        load_dotenv()
        self.storage_client = storage.Client(project=project_id)
        self.bucket_name = os.getenv("GOOGLE_STORAGE_BUCKET_NAME")

    def upload_blob(self, source_file_name, destination_blob_name):
        """Uploads a file to the bucket."""
        bucket = self.storage_client.bucket(self.bucket_name)
        blob = bucket.blob(destination_blob_name)
        blob.upload_from_filename(source_file_name, timeout=300)
        print("File {} uploaded to {}.".format(source_file_name, destination_blob_name))

    def get_gs_url(self, destination_blob_name):
        return 'gs://{}/{}'.format(self.bucket_name, destination_blob_name)


if __name__ == "__main__":
    google_storage = GoogleStorage()
    google_storage.upload_blob("video.mp4", "video.mp4")