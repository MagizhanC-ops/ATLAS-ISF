from pathlib import Path
from typing import List
import logging
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import (
    PyPDFLoader,
    TextLoader,
    UnstructuredMarkdownLoader
)
from langchain.schema import Document
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import ollama
import numpy as np
import hashlib

logger = logging.getLogger(__name__)

class DocumentIngestionService:
    def __init__(self, docs_dir: str = "./docs", collection_name: str = "documents"):
        self.docs_dir = Path(docs_dir)
        self.collection_name = collection_name
        self.client = QdrantClient(host="localhost", port=6333)
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
            separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""]
        )
        
        # Initialize Qdrant collection
        self._ensure_collection()
    
    def _ensure_collection(self):
        """Ensure vector collection exists"""
        try:
            collections = self.client.get_collections().collections
            exists = any(c.name == self.collection_name for c in collections)
            
            if not exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(size=384, distance=Distance.COSINE)
                )
        except Exception as e:
            logger.error(f"Error ensuring collection: {str(e)}")
    
    def _load_document(self, file_path: Path) -> List[Document]:
        """Load document based on file type"""
        try:
            if file_path.suffix == '.pdf':
                loader = PyPDFLoader(str(file_path))
            elif file_path.suffix == '.txt':
                loader = TextLoader(str(file_path))
            elif file_path.suffix == '.md':
                loader = UnstructuredMarkdownLoader(str(file_path))
            else:
                logger.warning(f"Unsupported file type: {file_path}")
                return []
            
            return loader.load()
        except Exception as e:
            logger.error(f"Error loading document {file_path}: {str(e)}")
            return []
    
    async def _get_embeddings(self, text: str) -> List[float]:
        """Get embeddings using Ollama"""
        try:
            response = await ollama.embeddings(
                model='mistral',
                prompt=text
            )
            return response['embedding']
        except Exception as e:
            logger.error(f"Error getting embeddings: {str(e)}")
            return []
    
    def _get_document_hash(self, content: str) -> str:
        """Generate hash for document content"""
        return hashlib.md5(content.encode()).hexdigest()
    
    async def process_documents(self):
        """Process all documents in the docs directory"""
        try:
            for file_path in self.docs_dir.glob('**/*'):
                if file_path.is_file() and file_path.suffix in ['.pdf', '.txt', '.md']:
                    # Load and split document
                    docs = self._load_document(file_path)
                    chunks = self.text_splitter.split_documents(docs)
                    
                    for chunk in chunks:
                        content = chunk.page_content
                        doc_hash = self._get_document_hash(content)
                        
                        # Get embeddings
                        embeddings = await self._get_embeddings(content)
                        if not embeddings:
                            continue
                        
                        # Store in Qdrant
                        self.client.upsert(
                            collection_name=self.collection_name,
                            points=[{
                                'id': doc_hash,
                                'vector': embeddings,
                                'payload': {
                                    'text': content,
                                    'source': str(file_path),
                                    'metadata': chunk.metadata
                                }
                            }]
                        )
                        
                    logger.info(f"Processed document: {file_path}")
                    
        except Exception as e:
            logger.error(f"Error processing documents: {str(e)}") 