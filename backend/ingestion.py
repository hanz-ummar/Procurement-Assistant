import pandas as pd
import io
from loguru import logger
from llama_index.core import Document, VectorStoreIndex
from .database import MinioClient, get_vector_store
from .llm import init_llm

class DataPreprocessingAgent:
    def __init__(self):
        self.minio_client = MinioClient()
        # Ensure LLM settings are initialized
        init_llm()

    def process_csv(self, file_content, file_name, progress_callback=None):
        """
        Ingests a CSV file using LlamaIndex:
        1. Uploads raw file to MinIO.
        2. Parses CSV and creates LlamaIndex Documents.
        3. Indexes them into ChromaDB via VectorStoreIndex.
        """
        # 1. Upload to MinIO
        if progress_callback: progress_callback(0.1, "Uploading to MinIO...")
        self.minio_client.upload_file(file_name, io.BytesIO(file_content), len(file_content))

        # 2. Parse CSV
        if progress_callback: progress_callback(0.2, "Parsing CSV...")
        try:
            df = pd.read_csv(io.BytesIO(file_content))
            logger.info(f"Loaded CSV with {len(df)} rows")
        except Exception as e:
            logger.error(f"Error parsing CSV: {e}")
            return False, "Invalid CSV format"

        # 3. Create LlamaIndex Documents
        documents = []
        total_rows = len(df)
        
        for index, row in df.iterrows():
            if progress_callback and index % 10 == 0:
                progress = 0.2 + (0.5 * (index / total_rows))
                progress_callback(progress, f"Preparing Documents ({index+1}/{total_rows})...")

            # Create a rich text representation of the row
            text_chunk = (
                f"Supplier: {row.get('SupplierName', 'N/A')} (ID: {row.get('SupplierID', 'N/A')})\n"
                f"Item: {row.get('ItemName', 'N/A')} (Category: {row.get('ItemCategory', 'N/A')})\n"
                f"PO: {row.get('POID', 'N/A')} | Date: {row.get('PODate', 'N/A')}\n"
                f"Cost: {row.get('TotalAmount', '0')} {row.get('Unit', '')} | Price: {row.get('UnitPrice', '0')}\n"
                f"Performance: Delivery {row.get('OnTimeDelivery%', 'N/A')}%, Quality {row.get('QualityScore', 'N/A')}\n"
                f"Risk: {row.get('SupplierRiskLevel', 'Low')} - {row.get('RiskDescription', 'None')}\n"
                f"Contract: {row.get('ContractID', 'N/A')} (Expires: {row.get('ContractEndDate', 'N/A')})\n"
                f"Compliance: {row.get('ComplianceStatus', 'Unknown')}"
            )
            
            # Metadata for filtering
            metadata = {
                "supplier_id": str(row.get('SupplierID', '')),
                "supplier_name": str(row.get('SupplierName', '')),
                "item_category": str(row.get('ItemCategory', '')),
                "risk_level": str(row.get('SupplierRiskLevel', '')),
                "source": file_name,
                "row_index": index
            }
            
            doc = Document(text=text_chunk, metadata=metadata)
            documents.append(doc)

        # 4. Index into ChromaDB
        if progress_callback: progress_callback(0.8, "Indexing to Vector DB...")
        
        try:
            vector_store, storage_context = get_vector_store()
            
            # Create Index (this handles embedding generation automatically)
            VectorStoreIndex.from_documents(
                documents, 
                storage_context=storage_context,
                show_progress=True
            )
            
            if progress_callback: progress_callback(1.0, "Done!")
            return True, f"Successfully processed {len(documents)} records."
        except Exception as e:
            logger.error(f"Error indexing documents: {e}")
            return False, f"Error indexing documents: {str(e)}"
