from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import json
import os
from typing import Optional, List
from dotenv import load_dotenv
from groq import Groq
from huggingface_hub import InferenceClient
import re
from datetime import datetime

# Load environment variables
load_dotenv()

app = FastAPI(title="Cambridge History Examiner Bot - Simple Mode")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Knowledge Datasets
BASE_DIR = os.path.dirname(__file__)
HIST_DATA_PATH = os.path.join(BASE_DIR, "..", "data", "history_data.json")

def load_json(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

history_data = load_json(HIST_DATA_PATH)

# Initialize LLM clients
groq_client = Groq(api_key=os.getenv("GROQ_API_KEY")) if os.getenv("GROQ_API_KEY") else None
hf_client = InferenceClient(token=os.getenv("HF_API_KEY")) if os.getenv("HF_API_KEY") else None

def get_subject_context(query):
    """Focused RAG logic for Cambridge History"""
    context = ""
    query_lower = query.lower()
    data = history_data
    matches = []
    marking_examples = []
        
    specific_topics = data.get("specific_topics", {})
    topic_lower_words = set(re.findall(r'\w+', query_lower))
    
    for key, topic_data in specific_topics.items():
        key_words = set(key.split('_'))
        common = topic_lower_words.intersection(key_words)
        match = False
        if len(key_words) == 1 and len(common) == 1: match = True
        elif len(common) >= 2: match = True
        elif any(date in query_lower for date in re.findall(r'\d{4}', key)): match = True
            
        if match:
            context += f"\n### TEXTBOOK CONTEXT: {topic_data.get('title', key)} (Nigel Kelly Standards)\n"
            if "factors" in topic_data:
                for factor, points in topic_data["factors"].items():
                    context += f"**{factor}**:\n"
                    for p in points: context += f"- {p}\n"
            if "qa_pairs" in topic_data:
                context += "\n**Relevant Past Questions & Answers:**\n"
                for qa in topic_data["qa_pairs"][:3]:
                    context += f"Q: {qa['question']}\nA: {qa['answer']}\n\n"
            if "raw_text" in topic_data:
                 context += f"{topic_data['raw_text'][:1000]}...\n"
            context += "\n"
    
    for section in ["section_1", "section_2", "section_3"]:
        for item in data.get(section, []):
            topic = item.get("topic", "").lower()
            if topic in query_lower or any(kw in query_lower for kw in topic.split() if len(kw) > 3):
                matches.append(json.dumps(item, indent=2))
        
    past_papers = data.get("past_papers", {})
    for year, seasons in past_papers.items():
        for season, papers in seasons.items():
            for paper, content in papers.items():
                mark_schemes = content.get("mark_scheme", [])
                for scheme in mark_schemes:
                    question = scheme.get("question", "")
                    points = scheme.get("points", [])
                    if any(word in question.lower() for word in query_lower.split() if len(word) > 4):
                        marking_examples.append({"year": year, "question": question, "points": points[:5]})
        
    if matches:
        context += "\n### O-LEVEL HISTORY ARCHIVE:\n" + "\n---\n".join(matches[:2])
    
    if marking_examples:
        context += "\n\n### CAMBRIDGE EXAMINER MARKING SCHEMES:\n"
        for example in marking_examples[:2]:
            context += f"\n**Question: {example['question']}**\n"
            for point in example['points']: context += f"  • {point}\n"
            
    return context

async def get_llm_response(prompt: str, marks: int = 4, mode: str = "chat"):
    context = get_subject_context(prompt)
    system_prompt = f"""
You are the Cambridge History Examiner Simulation Engine (Syllabus 2059/01).
Strictly follow the 10-step protocol:
1. Detect Command Word/Topic.
2. Enforce Length: 4m(110-150w), 7m(220-260w), 14m(450-550w).
3. If personality mentioned, start with Bio details.
4. Structure: 4m(2 PEEL), 7m(3 PEEL), 14m(Intro, Agree, Disagree, Judgement).
5. Use Nigel Kelly evidence exclusively from context.
6. Append [EXAMINER AUDIT] footer with predictive mark and reasoning.
7. Student Answer Analysis when appropriate.
8. Depth Analysis for evaluation questions.
9. Tone: Clinical, formal examiner.
10. Failsafe: Default to 4m logic.

CONTEXT:
{context}
"""
    # Try Groq first (Primary)
    if groq_client:
        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Answer for {marks} marks: {prompt}"}
                ],
                temperature=0.3,
                max_tokens=2500
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Groq Error: {str(e)}. Falling back to secondary engine...")

    # Fallback to Hugging Face (Secondary)
    if hf_client:
        try:
            return hf_client.text_generation(
                f"<|system|>\n{system_prompt}\n<|user|>\nAnswer for {marks} marks: {prompt}\n<|assistant|>",
                model="Qwen/Qwen2.5-72B-Instruct",
                max_new_tokens=2000
            )
        except Exception as e:
            return f"Error with all intelligence engines: {str(e)}"
    
    return "Intelligence engines offline. Please check API keys."

@app.post("/ask-ai")
async def ask_ai(
    query: str = Form(...),
    marks: int = Form(4)
):
    answer = await get_llm_response(query, marks)
    return {"answer": answer, "marks": marks}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
