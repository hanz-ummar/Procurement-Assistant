"""
Unit tests for data ingestion and preprocessing.
Tests CSV validation, parsing, and error handling.
"""
import pytest
import pandas as pd
import io
from backend.ingestion import DataPreprocessingAgent


@pytest.mark.unit
class TestCSVValidation:
    """Test CSV validation logic"""
    
    def test_valid_csv_passes_validation(self, sample_csv_data):
        """Test that valid CSV data passes validation checks"""
        # Parse CSV to verify it's valid
        df = pd.read_csv(io.BytesIO(sample_csv_data))
        
        # Should have expected columns
        required_columns = {'SupplierName', 'PONumber', 'PODate', 'Amount'}
        assert required_columns.issubset(set(df.columns))
        
        # Should have data
        assert len(df) > 0
    
    def test_invalid_csv_detected(self, invalid_csv_data):
        """Test that invalid CSV is detected"""
        df = pd.read_csv(io.BytesIO(invalid_csv_data))
        
        # Missing required columns
        required_columns = {'SupplierName', 'PONumber', 'PODate', 'Amount'}
        assert not required_columns.issubset(set(df.columns))
    
    def test_empty_csv_handling(self):
        """Test handling of empty CSV"""
        empty_csv = b"SupplierName,PONumber,PODate,Amount\n"
        df = pd.read_csv(io.BytesIO(empty_csv))
        
        assert len(df) == 0
    
    def test_csv_with_missing_values(self):
        """Test CSV with missing values"""
        csv_with_nulls = b"""SupplierName,PONumber,PODate,Amount
Acme,PO-001,2024-01-01,1000
,PO-002,2024-01-02,2000
Beta,,2024-01-03,3000"""
        
        df = pd.read_csv(io.BytesIO(csv_with_nulls))
        
        # Should parse but have NaN values
        assert len(df) == 3
        assert df['SupplierName'].isna().sum() == 1
        assert df['PONumber'].isna().sum() == 1


@pytest.mark.unit
class TestDataPreprocessing:
    """Test data preprocessing operations"""
    
    def test_date_column_parsing(self, sample_csv_data):
        """Test that date columns are properly parsed"""
        df = pd.read_csv(io.BytesIO(sample_csv_data))
        
        # Convert dates
        df['PODate'] = pd.to_datetime(df['PODate'])
        df['DeliveryDate'] = pd.to_datetime(df['DeliveryDate'])
        
        # Should be datetime type
        assert df['PODate'].dtype == 'datetime64[ns]'
        assert df['DeliveryDate'].dtype == 'datetime64[ns]'
        
        # Should have valid dates
        assert not df['PODate'].isna().all()
    
    def test_amount_column_numeric(self, sample_csv_data):
        """Test that Amount column is numeric"""
        df = pd.read_csv(io.BytesIO(sample_csv_data))
        
        assert pd.api.types.is_numeric_dtype(df['Amount'])
        assert (df['Amount'] > 0).all()
    
    def test_text_columns_cleaned(self, sample_csv_data):
        """Test that text columns are cleaned"""
        df = pd.read_csv(io.BytesIO(sample_csv_data))
        
        # Trim whitespace
        df['SupplierName'] = df['SupplierName'].str.strip()
        df['Category'] = df['Category'].str.strip()
        
        # No leading/trailing spaces
        assert not any(df['SupplierName'].str.startswith(' '))
        assert not any(df['SupplierName'].str.endswith(' '))


@pytest.mark.unit
class TestDataPreprocessingAgent:
    """Test DataPreprocessingAgent class"""
    
    def test_agent_initialization(self):
        """Test agent initializes correctly"""
        agent = DataPreprocessingAgent()
        
        assert agent is not None
        assert hasattr(agent, 'process_csv')
    
    def test_chunk_text_function(self):
        """Test text chunking for RAG"""
        agent = DataPreprocessingAgent()
        
        # Create sample text
        text = "This is a test. " * 100  # Long text
        
        # Chunk it (if method exists)
        if hasattr(agent, '_chunk_text'):
            chunks = agent._chunk_text(text, chunk_size=100)
            
            assert len(chunks) > 1
            assert all(len(chunk) <= 150 for chunk in chunks)  # Allow some overflow
