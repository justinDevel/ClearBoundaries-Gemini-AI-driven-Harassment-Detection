import asyncio
from http.client import HTTPException
from typing import Any, Dict, List, Optional, Union
import os
from models.message import AnalyzeMessagesRequest, FlaggedPhrase, MessageAnalysisResult, Report
from services.task_manager import task_manager
from utils.prompt_util import generate_prompt
from fastapi import  HTTPException, status, Request
import logging
from dotenv import load_dotenv
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import json
from functools import lru_cache


load_dotenv()

logger = logging.getLogger(__name__)
#gemini-1.5-pro"
#gemini-1.5-flash-latest
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", '') 
GEMINI_API_MODEL_NAME: str = os.getenv("GEMINI_API_MODEL_NAME", 'gemini-1.5-flash-latest') 
MODEL_PATH = "models/"
MODEL_NAME = GEMINI_API_MODEL_NAME
MODEL_FILE_PATH = f"{MODEL_PATH}{MODEL_NAME}"

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

GENERATION_CONFIG = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "application/json",
}


@lru_cache()
def get_gemini_model():
    """
    Retrieves and caches the Gemini model for efficient use.
    """
    logger.error(f"Api for Gemini: {GEMINI_API_KEY}")
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(
        model_name=MODEL_FILE_PATH,
        generation_config=GENERATION_CONFIG,
    )
    return model

async def get_gemini_model_info():
    

    modelInfo = genai.get_model(MODEL_FILE_PATH)

    return modelInfo

async def get_gemini_models_list():
    

    models = genai.list_models()

    return models


async def analyze_message(request: AnalyzeMessagesRequest) -> List[MessageAnalysisResult]:
    results = []

    context = request.data.get("context", "")

    for message in request.messages:
        if not message.body:
            logger.error("Received empty message body.")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message body must not be empty.")

        try:
            prompt_data = {
                "subject": message.subject,
                "body": message.body,
                "sender": message.sender,
                "recipient": message.recipient,
                "created_at": message.created_at.isoformat() if message.created_at else None,
                "modified_at": message.modified_at.isoformat() if message.modified_at else None,
                "email_thread_id": message.email_thread_id,
                "language": message.language,
                "context": context
            }

            logger.info(f"prompt_data: {prompt_data}")
            prompt = await generate_prompt(prompt_data)

        except (AttributeError, TypeError, ValueError) as e:
            logger.error(f"Invalid message format or data error: {e}")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Message format or data is invalid.")

        logger.info(f"Generated prompt for message analysis: {prompt}")

        try:
            model = get_gemini_model()
        
            safety_settings = [
                {
                    "category": "HARM_CATEGORY_HARASSMENT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_HATE_SPEECH",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                    "threshold": "BLOCK_NONE",
                },
                {
                    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                    "threshold": "BLOCK_NONE",
                },
            ]
            
            # response = await task_manager.add_task(model.generate_content, prompt)
            response = model.generate_content(prompt, safety_settings=safety_settings)
            if not response:
                logger.error("No response received from Gemini API.")
                raise ValueError("Received None from Gemini API.")

            if not hasattr(response, 'text') or not response.text:
                logger.error("Invalid response structure: missing 'text' field.")
                raise ValueError("Response does not contain a valid 'text' field.")

         
            if hasattr(response, 'safety_ratings') and any(rating.probability > 'LOW' for rating in response.safety_ratings):
                logger.warning(f"Content flagged by safety filters: {response.safety_ratings}")
                raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Content flagged by AI safety filters.")

            try:
                gemini_response = json.loads(response.text) if isinstance(response.text, str) else response.text
            except json.JSONDecodeError as decode_err:
                logger.error(f"Failed to parse Gemini response as JSON: {decode_err}")
                raise ValueError("Invalid JSON structure in Gemini response.")
            logger.info(f"Gemini response: {gemini_response}")
            parsed_response = gemini_response


            modelInfo = await get_gemini_model_info()
            input_tokens = model.count_tokens(prompt)
            max_model_tokens = modelInfo.input_token_limit
            limit = response.usage_metadata

            return {"status": "success", "modelData": modelInfo, "data": parsed_response, "model_max_tokens": format_number(max_model_tokens), "model_max_tokens_raw": max_model_tokens, "input_Tokens": input_tokens.total_tokens, "limit": limit.candidates_token_count}

        except Exception as e:
            logger.error(f"Error during message analysis: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error during analysis.")

    return results


def format_number(num):
    """
    Convert a token count to a short format with SI units (K, M, B) with accurate representation.
    
    Parameters:
    - num: The number of tokens (int).
    
    Returns:
    - A string representing the formatted token count with the appropriate unit.
    """
    if num >= 1_000_000_000_000:
        return f"{num / 1_000_000_000_000:.1f}T"  # Terabytes
    elif num >= 1_000_000_000:
        return f"{num / 1_000_000_000:.1f}G"   # Gigabytes
    elif num >= 1_000_000:
        return f"{num / 1_000_000:.1f}M"      # Megabytes
    elif num >= 1_000:
        return f"{num / 1_000:.1f}K"          # Kilobytes
    else:
        return str(num)                       

