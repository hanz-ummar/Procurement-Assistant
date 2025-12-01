import chromadb
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import StorageContext
from loguru import logger
from .config import Config

_vector_store_cache = None
_storage_context_cache = None

def get_vector_store():
    """
    Returns a configured LlamaIndex ChromaVectorStore and StorageContext.
    Uses caching to avoid repeated connections.
    """
    global _vector_store_cache, _storage_context_cache
    
    if _vector_store_cache and _storage_context_cache:
        return _vector_store_cache, _storage_context_cache

    try:
        # Initialize ChromaDB client
        logger.info(f"Connecting to ChromaDB at {Config.CHROMA_HOST}:{Config.CHROMA_PORT}")
        db = chromadb.HttpClient(host=Config.CHROMA_HOST, port=Config.CHROMA_PORT)
        
        # Get or create collection
        chroma_collection = db.get_or_create_collection(Config.CHROMA_COLLECTION_NAME)
        
        # Create Vector Store
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
        
        # Create Storage Context
        storage_context = StorageContext.from_defaults(vector_store=vector_store)
        
        _vector_store_cache = vector_store
        _storage_context_cache = storage_context
        
        return vector_store, storage_context
    except Exception as e:
        logger.error(f"Failed to initialize Vector Store: {e}")
        raise e

class MinioClient:
    """
    Kept for file storage (PDFs/CSVs) before processing.
    """
    def __init__(self):
        from minio import Minio
        self.client = Minio(
            Config.MINIO_ENDPOINT,
            access_key=Config.MINIO_ACCESS_KEY,
            secret_key=Config.MINIO_SECRET_KEY,
            secure=False
        )
        self.bucket = Config.MINIO_BUCKET_NAME
        self._ensure_bucket()

    def _ensure_bucket(self):
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def upload_file(self, object_name, data, length):
        self.client.put_object(self.bucket, object_name, data, length)

    def list_files(self):
        """
        Lists all files in the bucket.
        """
        try:
            objects = self.client.list_objects(self.bucket)
            return [obj.object_name for obj in objects]
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            return []

    def get_file_content(self, object_name):
        """
        Retrieves the content of a file as bytes.
        """
        try:
            response = self.client.get_object(self.bucket, object_name)
            return response.read()
        except Exception as e:
            logger.error(f"Error getting file content: {e}")
            return None
        finally:
            if 'response' in locals():
                response.close()
                
    def delete_file(self, object_name):
        """
        Deletes a file from the bucket.
        """
        try:
            self.client.remove_object(self.bucket, object_name)
            return True
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return False
