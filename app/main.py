import asyncio
import os
import uvicorn
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from api.routes import router as analysis_router

# Initialize FastAPI app
app = FastAPI(title="Email Analysis API - ClearBoundaries")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(analysis_router, prefix="/api/analyze")


load_dotenv()


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)



app.add_middleware(SessionMiddleware, secret_key=os.getenv("SECRET_KEY"))


@app.middleware("http")
async def timeout_middleware(request: Request, call_next):
    timeout = 15

    try:
       
        logger.info(f"Request sent by the client to : {request.url.path}")
        response = await asyncio.wait_for(call_next(request), timeout=timeout)
        return response

    except asyncio.TimeoutError:

        logger.warning(f"Request timed out after {timeout} seconds: {request.url.path}")
        return JSONResponse(
            status_code=504,
            content={"error": "Request timed out", "detail": f"Processing time exceeded {timeout} seconds"}
        )
    

    
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
