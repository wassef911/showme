from azure.storage.blob import BlobServiceClient, ContainerClient
from io import BytesIO
from loguru import logger


class ImageStorageService:
    container_client: ContainerClient
    container_name: str
    blob_service_client: BlobServiceClient

    def __init__(self, connection_string: str, container_name: str):
        """- connection_string: The connection string to the Azure Blob Storage account."""
        self.blob_service_client: BlobServiceClient = (
            BlobServiceClient.from_connection_string(
                connection_string,
            )
        )
        self._ensure_container_exists(container_name)

    def _ensure_container_exists(self, container_name):
        """
        Checks if the specified container exists, and creates it if not.
        """
        container_client = self.blob_service_client.get_container_client(
            container_name,
        )

        if not container_client.exists():
            container_client.create_container()
            logger.info(f"Container '{container_name}' was created.")
        else:
            logger.info(f"Container '{container_name}' already exists.")
        self.container_name = container_name
        self.container_client = container_client

    def image_exists(self, blob_name):
        """
        Check if the specified blob exists in the container.

        Parameters:
        - blob_name: The name of the blob to check.

        Returns:
        - True if the blob exists, False otherwise.
        """
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name,
            blob=blob_name,
        )
        return blob_client.exists()

    def upload_image_if_not_exists(self, blob_name, bytes_io: BytesIO):
        """
        Check if a PNG image exists in the specified Azure Blob Storage container and if not, upload it from a BytesIO object.

        Parameters:
        - blob_name: The desired name of the PNG file in the Blob Storage.
        - bytes_io: A BytesIO object containing the PNG data to be uploaded.

        Returns:
        - True if the file was uploaded successfully, False if the file already exists or an error occurred.
        """
        if self.image_exists(blob_name):
            return False
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name,
            blob=blob_name,
        )
        bytes_io.seek(0)
        blob_client.upload_blob(
            bytes_io,
            blob_type="BlockBlob",
            overwrite=True,
        )
        return True

    def delete_image(self, blob_name):
        """
        Delete the specified blob from the container.

        Parameters:
        - blob_name: The name of the blob to delete.

        Returns:
        - True if the blob was deleted successfully, False if the blob does not exist.
        """
        if not self.image_exists(blob_name):
            return False

        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name,
            blob=blob_name,
        )
        blob_client.delete_blob()
        return True

    def get_image(self, blob_name) -> BytesIO:
        """
        Get the image data from the specified blob in the container.

        Parameters:
        - blob_name: The name of the blob to retrieve.

        Returns:
        - A BytesIO object containing the image data, or None if the blob does not exist.
        """

        if not self.image_exists(blob_name):
            raise FileNotFoundError(
                f"Blob '{blob_name}' not found in container '{self.container_name}'.",
            )

        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name,
            blob=blob_name,
        )
        image_data = blob_client.download_blob().readall()
        return BytesIO(image_data)

    def get_image_url(self, blob_name) -> str:
        """
        Get the URL of the specified blob in the container.

        Parameters:
        - blob_name: The name of the blob to retrieve.

        Returns:
        - A string containing the URL of the blob.
        """
        blob_client = self.blob_service_client.get_blob_client(
            container=self.container_name,
            blob=blob_name,
        )
        return blob_client.url
