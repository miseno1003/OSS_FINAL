from fastapi import FastAPI
from pydantic import BaseModel
import random

app = FastAPI(title="치킨 추천 API")


KEYWORD_MAP = {
    "후라이드": "후라이드",
    "양념": "양념",
    "달달": "달달",
    "달콤": "달달",
    "간장": "간장",
    "매콤": "매콤",
    "매운": "매콤",
    "스파이시": "매콤",
}

RULES = {
    "후라이드": [
        {"name": "BBQ 황금 올리브 치킨", "brand": "BBQ", "description": "겉은 바삭 육즙 가득한 부드러운 속살이 환상적인 건강한 치킨 비비큐의 시그니처 메뉴 후라이드의 대명사 황금올리브치킨 [땅콩 알러지 주의]"},
        {"name": "후라이드 치킨", "brand": "처갓집양념치킨", "description": "국내산 신선육에 독특한 맛의 파우더를 입혀 바삭하고 고소하게 튀겨낸 처갓집양념치킨의 인기메뉴"},
        {"name": "60계 치킨 크크크치킨", "brand": "60계 치킨", "description": "크럼블!크런치! 크리스피! 바삭하고 맛있어서 ㅋㅋㅋ 웃음이 터지는 치킨"},
        {"name": "콰삭킹", "brand": "BHC", "description": "콰삭한 식감과 고소한 맛이 일품인 후라이드 치킨"},
    ],
    "양념": [
        {"name": "슈프림 양념치킨", "brand": "처갓집양념치킨", "description": "바삭한 후라이드 치킨 위에 허니올리고당 야채 양념과 신비의 하얀 소스가 뿌려진 이색적인 양념치킨"},
        {"name": "양념치킨", "brand": "호치킨", "description": "호치킨만의 소스로 맛을 낸 매콤 달콤한 치킨"},
    ],
    "달달": [
        {"name": "BHC 뿌링클", "brand": "BHC", "description": "뿌링 시즈닝의 원조, 치즈 파우더 듬뿍"},
        {"name": "허니콤보", "brand": "교촌치킨", "description": "달콤한 허니 소스와 간장 소스의 조화"},
    ],
    "간장": [
        {"name": "교촌 오리지날", "brand": "교촌치킨", "description": "달콤한 허니간장 소스"},
        {"name": "소이갈릭", "brand": "네네치킨", "description": "간장과 마늘의 완벽한 조화"},
        {"name": "단짠치킨", "brand": "또래오래", "description": "단짠한 맛의 대표 메뉴"}
    ],
    "매콤": [
        {"name": "자메이카 통다리구이 양념", "brand": "BBQ", "description": "치킨 부위 중 가장 맛있는 엉치살이 붙은 통다리만을 골라, 카리브해 서인도제도의 신비의 나라인 자메이카의 300년 전통 저크 소스를 바른 뒤, 2번 구워내어 매콤 달콤한 맛과 깊은 신비를 느낄 수 있는 치킨, 바비큐의 절정 통다리구이"},
        {"name": "맛초킹", "brand": "BHC", "description": "매콤한 양념이 중독적인 인기 메뉴"},
        {"name": "알싸한 마늘치킨", "brand": "노랑통닭", "description": "알싸한 마늘 양념이 매력적인 메뉴"},
    ],
}


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