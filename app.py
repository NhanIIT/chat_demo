from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline
from db import init_db, query_db
from redis_cache import cache_get, cache_set, make_cache_key


app = FastAPI()

# Khởi tạo CSDL nhân sự mẫu khi app khởi động
init_db()

# Khởi tạo pipeline Gemma-2B-IT (text-generation)
llm = pipeline(
    "text-generation",
    model="google/gemma-2b-it",
    device_map="auto"
)


def sinh_sql(question: str) -> str:
    prompt = f"Viết câu truy vấn SQL cho câu hỏi: '{question}'\nSQL:"
    result = llm(prompt, max_new_tokens=128, do_sample=True, temperature=0.2)
    sql = result[0]['generated_text'].split('SQL:')[-1].strip()
    return sql


class ChatRequest(BaseModel):
    question: str


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    sql = sinh_sql(request.question)
    cache_key = make_cache_key(sql)
    cached = cache_get(cache_key)
    if cached:
        return {
            "sql": sql,
            "result": cached,
            "note": "Kết quả từ cache (Redis)"
        }
    try:
        result = query_db(sql)
        cache_set(cache_key, result)
        return {
            "sql": sql,
            "result": result,
            "note": "Kết quả từ CSDL và đã cache"
        }
    except Exception as e:
        return {
            "sql": sql,
            "error": str(e),
            "note": "Lỗi khi truy vấn CSDL"
        } 