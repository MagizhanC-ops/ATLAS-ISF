from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/chat", response_class=HTMLResponse)
async def chat_interface():
    """Serve Chainlit interface"""
    return """
    <!DOCTYPE html>
    <html>
        <head>
            <title>ATLAS-ISF Chat Interface</title>
            <script>
                window.location.href = "http://localhost:8000/_chainlit/";
            </script>
        </head>
        <body>
            <p>Redirecting to chat interface...</p>
        </body>
    </html>
    """ 