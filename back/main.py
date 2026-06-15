from fastapi import FastAPI
from pydantic import BaseModel
import random
import json

app = FastAPI(title="치킨 추천 API")

with open("chickens.json", encoding="utf-8") as f:
    _data = json.load(f)

KEYWORD_MAP: dict = _data["keyword_map"]
RULES: dict = _data["rules"]


class RecommendRequest(BaseModel):
    text: str


class ChickenItem(BaseModel):
    name: str
    brand: str
    description: str


class RecommendResponse(BaseModel):
    status: str
    keyword: str
    message: str
    recommendations: list[ChickenItem]


@app.get("/")
def root():
    return {"message": "치킨 추천 API 서버 정상 동작 중 🍗"}


@app.post("/recommend", response_model=RecommendResponse)
def recommend(req: RecommendRequest):
    text = req.text.strip()

    for keyword, category in KEYWORD_MAP.items():
        if keyword in text:
            return RecommendResponse(
                status="ok",
                keyword=keyword,
                message=f"'{keyword}' 치킨을 원하시는군요! 딱 맞는 추천입니다 🍗",
                recommendations=RULES[category],
            )

    if "치킨" in text:
        all_items = [item for items in RULES.values() for item in items]
        chosen = random.sample(all_items, k=min(3, len(all_items)))
        return RecommendResponse(
            status="random",
            keyword="랜덤",
            message="음… 고민해볼 필요가 있겠네요….. 오늘의 랜덤 추천입니다! 🎲",
            recommendations=chosen,
        )

    return RecommendResponse(
        status="error",
        keyword="",
        message="잘못 입력하셨습니다 😥 '치킨🍗'이 맞나요?",
        recommendations=[],
    )