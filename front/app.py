import streamlit as st
import requests
import os

FASTAPI_URL = os.getenv("FASTAPI_URL", "http://localhost:8000")

st.set_page_config(page_title="오늘 뭐 시킬까? 🍗", page_icon="🍗", layout="centered")


def render_results(items: list):
    st.subheader("추천 치킨 메뉴")
    for item in items:
        with st.container(border=True):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {item['name']}")
                st.caption(item["description"])
            with col2:
                st.markdown(f"**{item['brand']}**")


st.title("🍗 오늘 야식은 치킨 🍗")
st.markdown("##### 오늘 먹고 싶은 치킨 스타일을 자유롭게 입력하면 딱 맞는 메뉴를 추천해드려요!")
st.markdown(
    "> **입력 예시:** `후라이드가 먹고 싶어요`, `달달한 게 땡겨요`, `아무 치킨이나 추천해줘`"
)
st.divider()

user_input = st.text_input(
    "오늘 어떤 치킨이 먹고 싶으세요?",
    placeholder="예: 후라이드 추천해주세요!",
    max_chars=100,
)

clicked = st.button("🔍 추천받기", use_container_width=True, type="primary")

if clicked:
    if not user_input.strip():
        st.warning("먹고 싶은 치킨을 입력해주세요!")
    else:
        with st.spinner("맛있는 치킨을 찾는 중..."):
            try:
                response = requests.post(
                    f"{FASTAPI_URL}/recommend",
                    json={"text": user_input},
                    timeout=10,
                )
                response.raise_for_status()
                result = response.json()

                st.divider()

                if result["status"] == "error":
                    st.error(result["message"])
                elif result["status"] == "random":
                    st.info(result["message"])
                    render_results(result["recommendations"])
                else:
                    st.success(result["message"])
                    render_results(result["recommendations"])

            except requests.exceptions.ConnectionError:
                st.error("FastAPI 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인해주세요.")
            except Exception as e:
                st.error(f"오류가 발생했습니다: {e}")
