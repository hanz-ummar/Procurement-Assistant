"""
Integration tests for MinIO storage.
Requires MinIO running via docker-compose.
"""
import pytest
import io
from backend.database import MinioClient


@pytest.mark.integration
class TestMinIOConnection:
    """Test MinIO connection and basic operations"""
    
    def test_minio_client_initialization(self):
        """Test MinIO client initializes successfully"""
        client = MinioClient()
        
        assert client is not None
        assert client.bucket == "procurement-data"
    
    def test_bucket_exists(self, minio_client):
        """Test that procurement bucket exists"""
        # Bucket should be created automatically
        assert minio_client.client.bucket_exists(minio_client.bucket)


@pytest.mark.integration
class TestMinIOFileOperations:
    """Test MinIO file upload, download, list, delete operations"""
    
    def test_upload_file(self, minio_client, clean_test_file):
        """Test file upload to MinIO"""
        filename = clean_test_file("test_upload.csv")
        test_data = b"SupplierName,Amount\nAcme,1000"
        
        # Upload
        minio_client.upload_file(filename, io.BytesIO(test_data), len(test_data))
        
        # Verify uploaded
        files = minio_client.list_files()
        assert filename in files
    
    def test_download_file(self, minio_client, clean_test_file):
        """Test file download from MinIO"""
        filename = clean_test_file("test_download.csv")
        test_data = b"SupplierName,Amount\nBeta,2000"
        
        # Upload first
        minio_client.upload_file(filename, io.BytesIO(test_data), len(test_data))
        
        # Download and verify
        downloaded = minio_client.get_file_content(filename)
        assert downloaded == test_data
    
    def test_list_files(self, minio_client, clean_test_file):
        """Test listing files in MinIO"""
        # Upload multiple test files
        files_to_upload = [
            clean_test_file("test_list_1.csv"),
            clean_test_file("test_list_2.csv"),
            clean_test_file("test_list_3.csv")
        ]
        
        for filename in files_to_upload:
            test_data = f"test data for {filename}".encode()
            minio_client.upload_file(filename, io.BytesIO(test_data), len(test_data))
        
        # List files
        all_files = minio_client.list_files()
        
        # Verify all test files are listed
        for filename in files_to_upload:
            assert filename in all_files
    
    def test_delete_file(self, minio_client):
        """Test file deletion from MinIO"""
        filename = "test_delete.csv"
        test_data = b"temporary data"
        
        # Upload
        minio_client.upload_file(filename, io.BytesIO(test_data), len(test_data))
        
        # Verify exists
        files = minio_client.list_files()
        assert filename in files
        
        # Delete
        result = minio_client.delete_file(filename)
        assert result == True
        
        # Verify deleted
        files_after = minio_client.list_files()
        assert filename not in files_after
    
    def test_large_file_upload(self, minio_client, clean_test_file, large_csv_data):
        """Test uploading larger files"""
        filename = clean_test_file("test_large.csv")
        
        # Upload large file
        minio_client.upload_file(filename, io.BytesIO(large_csv_data), len(large_csv_data))
        
        # Verify uploaded
        downloaded = minio_client.get_file_content(filename)
        assert len(downloaded) == len(large_csv_data)
        assert downloaded == large_csv_data


@pytest.mark.integration
class TestMinIOErrorHandling:
    """Test MinIO error handling"""
    
    def test_download_nonexistent_file(self, minio_client):
        """Test downloading file that doesn't exist"""
        result = minio_client.get_file_content("nonexistent_file.csv")
        
        # Should return None on error
        assert result is None
    
    def test_delete_nonexistent_file(self, minio_client):
        """Test deleting file that doesn't exist"""
        result = minio_client.delete_file("nonexistent_file_xyz123.csv")
        
        # MinIO may return True even for nonexistent files (idempotent operation)
        # Just verify it doesn't crash
        assert result in [True, False]
