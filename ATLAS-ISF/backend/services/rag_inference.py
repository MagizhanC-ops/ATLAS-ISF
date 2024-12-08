from qdrant_client import QdrantClient
import ollama
import logging
from typing import List, Dict, Any
import asyncio

logger = logging.getLogger(__name__)

class RAGInferenceService:
    def __init__(self, collection_name: str = "documents"):
        self.collection_name = collection_name
        self.client = QdrantClient(host="localhost", port=6333)
        self.context_size = 2000
        self.manufacturing_prompt = """You are an expert manufacturing consultant specializing in ISF (Incremental Sheet Forming) processes. 
        Use the following context to answer the question. If you cannot find relevant information in the context, 
        clearly state that you don't have enough information to provide a reliable answer.
        
        Context: {context}
        
        Question: {question}
        """
    
    async def _get_embeddings(self, text: str) -> List[float]:
        """Get embeddings for query text"""
        try:
            response = await ollama.embeddings(
                model='mistral',
                prompt=text
            )
            return response['embedding']
        except Exception as e:
            logger.error(f"Error getting embeddings: {str(e)}")
            return []
    
    def _format_context(self, results: List[Dict[str, Any]]) -> str:
        """Format search results into context string"""
        context_parts = []
        current_length = 0
        
        for result in results:
            text = result['payload']['text']
            if current_length + len(text) <= self.context_size:
                context_parts.append(text)
                current_length += len(text)
            else:
                break
        
        return "\n\n".join(context_parts)
    
    async def get_answer(self, question: str) -> str:
        """Get answer using RAG approach"""
        try:
            # Get question embeddings
            query_vector = await self._get_embeddings(question)
            if not query_vector:
                return "I apologize, but I'm having trouble processing your question. Please try again."
            
            # Search similar contexts
            search_results = self.client.search(
                collection_name=self.collection_name,
                query_vector=query_vector,
                limit=5
            )
            
            if not search_results:
                return "I don't have enough information in my knowledge base to answer this question reliably."
            
            # Format context
            context = self._format_context(search_results)
            
            # Generate answer using Ollama
            prompt = self.manufacturing_prompt.format(
                context=context,
                question=question
            )
            
            response = await ollama.chat(
                model='mistral',
                messages=[{
                    'role': 'user',
                    'content': prompt
                }]
            )
            
            return response['message']['content']
            
        except Exception as e:
            logger.error(f"Error in RAG inference: {str(e)}")
            return "I apologize, but I encountered an error while processing your question. Please try again." 