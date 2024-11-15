import asyncio
import json
from pathlib import Path
import secrets
import uuid
from models.message import AnalysisResults, AnalyzeMessagesRequest, MessageAnalysisResult
import aiofiles
from pydantic import BaseModel, Field, ValidationError
from typing import Any, Dict, List, Optional, Union
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status, Query, UploadFile, File, Request, Body
from fastapi.responses import JSONResponse
from services.analysis_service import  analyze_message
from services.app_service import  get_current_datetime
from fastapi import FastAPI, APIRouter, Response, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from fastapi.responses import HTMLResponse, RedirectResponse
from google_auth_oauthlib.flow import Flow
import requests
import jwt
import logging
import redis.asyncio as redis
import shutil
import httpx
import os


load_dotenv()

logger = logging.getLogger(__name__)

router = APIRouter()

def get_redis_client() -> redis.Redis:
   
    return redis.from_url(os.getenv("REDIS_URL", "redis://localhost:6379"), decode_responses=True)



@router.post("/analyze-messages", response_model=AnalysisResults)
async def analyze_messages(request: AnalyzeMessagesRequest):
    """
    Analyze workplace communication for potential harassment.

    This endpoint processes a batch of messages and evaluates them for any 
    harmful content based on predefined criteria. The results include a 
    harassment score, flagged phrases, and other relevant information to 
    help determine the tone and sentiment of the messages.

    **Parameters:**
    - `messages`: List of messages to analyze, each with a subject, body, sender, and recipient.
    - `data`: Additional data or context, such as analysis context (e.g., workplace communication).

    **Returns:**
    - Harassment score, flagged phrases, harassment type, and other metrics.
    """
    try:
        analysis_results = await analyze_message(request)
        return {"analysis_results": analysis_results}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))