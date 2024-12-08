import chainlit as cl
from services.rag_inference import RAGInferenceService
from services.doc_ingestion import DocumentIngestionService
import asyncio
import logging

logger = logging.getLogger(__name__)

rag_service = RAGInferenceService()
doc_service = DocumentIngestionService()

@cl.on_chat_start
async def start():
    """Initialize chat session"""
    # Process documents on startup
    await doc_service.process_documents()
    
    cl.Message(content="�� Welcome to ATLAS-ISF Assistant! I'm here to help you with ISF manufacturing processes. How can I assist you today?").send()

@cl.on_message
async def main(message: cl.Message):
    """Handle incoming messages"""
    try:
        # Show thinking message
        thinking_msg = cl.Message(content="Thinking...")
        await thinking_msg.send()
        
        # Get response from RAG service
        response = await rag_service.get_answer(message.content)
        
        # Update message with response
        await thinking_msg.update(content=response)
        
    except Exception as e:
        logger.error(f"Error in chat interface: {str(e)}")
        await thinking_msg.update(content="I apologize, but I encountered an error. Please try again.")

if __name__ == "__main__":
    cl.run() 