import os
from groq import AsyncGroq
from dotenv import load_dotenv
from typing import AsyncIterable, List, Dict


# Load environment variables
load_dotenv()
api_key = os.environ.get("GROQ_API_KEY")

# Initialize the Groq client with the API key
client = AsyncGroq(api_key=api_key)

async def get_answer_from_model(system_prompt: str, message: str, chat_history: List[Dict[str, str]])-> AsyncIterable[str]:

    # Create a chat completion with streaming enabled

    chat_completion = await client.chat.completions.create(
        # Required parameters
        messages=chat_history +[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": message,
            }
        ],
        
        # The language model which will generate the completion
        model="llama3-groq-70b-8192-tool-use-preview",

        # Optional parameters
        temperature=0.5,
        # Uncomment the following if needed
        # max_tokens=1024,
        # top_p=1,
        # stop=None,
        stream=True,
    )
    
    async def stream_response() -> AsyncIterable[str]:
        async for chunk in chat_completion:
            if chunk.choices[0].delta.content is not None:
                yield chunk.choices[0].delta.content
    
    return stream_response()