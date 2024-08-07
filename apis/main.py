import sys
sys.path.append('../')
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field, field_validator
from fastapi.responses import JSONResponse, StreamingResponse
from functions.groq_api_response import get_answer_from_model
from functions.chat_history import read_chat_history, format_chat_history

app = FastAPI()

class api_response(BaseModel):
    system_prompt: str = Field(..., min_length=1, description="System prompt cannot be empty and must be a non-null string.")
    user_prompt: str = Field(..., min_length=1, description="User prompt cannot be empty and must be a non-null string.")
    
    @field_validator('system_prompt', 'user_prompt')
    def check_max_words(cls, value):
        # Check if the string contains fewer than 100 words
        if len(value.split()) >= 100:
            raise ValueError('The string must contain fewer than 100 words')
        return value

@app.get('/', response_model=str)
async def root():
    return JSONResponse(status_code=200, content="Welcome to Groq API ChatBot API's")

@app.post('/groq_api_generator_response')
async def get_groq_api_response(input: api_response):
    try:
        chat_history = await read_chat_history(limit=5)
        format_history = await format_chat_history(chat_history)

        response_stream = await get_answer_from_model(input.system_prompt, input.user_prompt, format_history)

        return StreamingResponse(response_stream, media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))