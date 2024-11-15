from services.app_service import get_current_datetime
from services.prompt_generator import create_prompt
from fastapi import APIRouter, Request, HTTPException, status
import logging
from typing import Dict, Any, Optional


logger = logging.getLogger(__name__)


async def generate_prompt(data: Optional[Dict[str, Any]]) -> str:
    """
    Generate a prompt based on the provided data. This function ensures that all required data
    fields are populated, and provides default values when necessary to avoid errors.
    """

    if data is None:
        data = {}

    logger = logging.getLogger(__name__)
    logger.info(f"Received data: {data}")

    email_data = {
        "subject": data.get("subject", "No subject provided"),
        "body": data.get("body", "No body content provided"),
        "sender": data.get("sender", "No sender provided"),
        "recipient": data.get("recipient", "No recipient provided"),
        "created_at": data.get("created_at", "Unknown creation time"),
        "modified_at": data.get("modified_at", "Unknown modification time"),
        "email_thread_id": data.get("email_thread_id", "Unknown thread ID"),
        "language": data.get("language", "English"),
        "context": data.get("context", "General workplace communication"),
    }

    logger.info(f"email_data {email_data}")

    try:
        prompt = await create_prompt(**email_data)
    except Exception as e:
        logger.error(f"Error while generating prompt: {e}")
        raise RuntimeError(f"Failed to generate prompt: {e}")

    logger.info(f"Generated prompt: {prompt}")
    return prompt