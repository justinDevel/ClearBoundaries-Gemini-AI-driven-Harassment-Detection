from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class FlaggedPhrase(BaseModel):
    phrase: str
    suggested_replacement: str
    severity: str
    context: str

class Report(BaseModel):
    ai_analysis_is_harassment: bool
    is_harassment: bool
    harassment_type: Optional[str] = None
    recommendations: List[str] = []

class Message(BaseModel):
    subject: str
    body: str
    sender: str
    recipient: str
    created_at: Optional[datetime]
    modified_at: Optional[datetime]
    email_thread_id: str
    language: str

class Data(BaseModel):
    context: Optional[str] = "General workplace communication"

class MessageAnalysisResult(BaseModel):
    message: str
    tone: str
    sentiment: str
    flagged_phrases: List[FlaggedPhrase]
    revised_email: str
    report: Optional[Report] = None
    score: float

class AnalyzeMessagesRequest(BaseModel):
    messages: List[Message]
    data: dict


class Suggestion(BaseModel):
    original: str
    suggestion: str

class ModelData(BaseModel):
    name: str
    base_model_id: Optional[str] = None
    version: str
    display_name: str
    description: str
    input_token_limit: int
    output_token_limit: int
    supported_generation_methods: List[str]
    temperature: float
    max_temperature: float
    top_p: float
    top_k: int

class DataAnalysis(BaseModel):
    harmful: bool
    inappropriate: bool
    offensive: bool
    suggestions: List[Suggestion]

class AnalysisResults(BaseModel):
    analysis_results: dict

