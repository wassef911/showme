from azure.storage.blob import BlobServiceClient
from io import BytesIO
from loguru import logger


class BlobStorageService:
    def __init__(self, connection_string: str, container_name: str):
        """- connection_string: The connection string to the Azure Blob Storage account."""
        self.blob_client: BlobServiceClient = BlobServiceClient.from_connection_string(
            connection_string,
        )
        self.ensure_container_exists(container_name)

    def ensure_container_exists(self, container_name):
        """
        Checks if the specified container exists, and creates it if not.
        """
        container_client = self.blob_client.get_container_client(
            container_name,
        )

        if not container_client.exists():
            container_client.create_container()
            logger.info(f"Container '{self.container_name}' was created.")
        else:
            logger.info(f"Container '{self.container_name}' already exists.")
        self.container_name = container_name

    def upload_png_if_not_exists(self, container_name, blob_name, bytes_io: BytesIO):
        """
        Check if a PNG image exists in the specified Azure Blob Storage container and if not, upload it from a BytesIO object.

        Parameters:
        - container_name: The name of the container where the PNG is to be uploaded.
        - blob_name: The desired name of the PNG file in the Blob Storage.
        - bytes_io: A BytesIO object containing the PNG data to be uploaded.

        Returns:
        - True if the file was uploaded successfully, False if the file already exists or an error occurred.
        """
        # Create a blob client using the container and blob name
        self.blob_client.get_blob_client(container=container_name, blob=blob_name)
        if not self.blob_client.exists():
            bytes_io.seek(0)
            self.blob_client.upload_blob(
                bytes_io,
                blob_type="BlockBlob",
                overwrite=True,
            )
            return True
        return False
