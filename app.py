from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.llms import Ollama
from langchain.prompts import PromptTemplate
import uvicorn

app = FastAPI()

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_credentials=True,
    allow_headers=["*"],
)

# Request Model
class WizardRequest(BaseModel):
    topic: str
    level: str

# Initialize Ollama (cached)
llm = Ollama(model="deepseek-r1:1.5b")

@app.post("/summon-wizard")
async def summon_wizard(request: WizardRequest):
    try:
        prompt_template = PromptTemplate(
            input_variables=["topic", "level"],
            template="""
            You are a wise wizard in a fantasy realm helping a young coding apprentice.
            Use simple, magical analogies and whimsical language to teach about: {topic}.
            Explain at the level of: {level}.
            Include a Python code example.
            Always be encouraging and fun.
            """
        )
        prompt = prompt_template.format(topic=request.topic, level=request.level)
        response = llm(prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 80)))
