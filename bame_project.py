# -*- coding: utf-8 -*-
import streamlit as st
import random
from PIL import Image
import numpy as np
import openai
st.cache_data.clear()
st.cache_resource.clear()
# ---------------- 기본 설정 ----------------
st.set_page_config(
    page_title="BAME - Bamti Escape",
    page_icon="💜",
    layout="wide",
)

st.sidebar.title("BAME")


openai.api_key = st.secrets["openai"]["api_key"]

page = st.sidebar.radio(
    "메뉴를 선택해 주세요",
    [
        "HOME 🏠",
        "대화 코치 💬",
        "패션 & 퍼스널 컬러 👗",
        "SNS 브랜딩 📸",
        "요즘 밈 설명 😂",
        "오늘의 밤티 점수 🔮",
    ],
)

def line():
    st.markdown("---")

if page == "HOME 🏠":
    st.markdown("## BAME")
    line()
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 🧾 앱 소개")
        st.write(
            "BAME는 대화, 패션, SNS 브랜딩을 한 번에 도와주는 통합 자기관리 앱입니다.\n"
            "- 카톡/DM 대화 코칭\n"
            "- 퍼스널 컬러 기반 코디 추천\n"
            "- 피드/스토리 브랜딩 가이드\n"
            "를 통해 사용자가 자연스럽게 성장하도록 돕는 것을 목표로 합니다."
        )
        st.markdown("### 🎯 개발 목표")
        st.write(
            "- 현대인의 소통 부담, 패션 고민, SNS 경쟁력 부족을 한 번에 해결\n"
            "- 사용자의 매력을 자연스럽고 입체적으로 성장시키는 것을 목표\n"
            "- 대화 추천, 코디 분석, 스토리 추천 기능 제공"
        )
    with col2:
        st.markdown("### 👥 팀 정보")
        st.write("**팀원 1:** 강민서")
        st.write("**팀원 2:** 신수아")


elif page == "대화 코치 💬":
    st.markdown("## 대화 코치 💬")
    line()
    rel = st.selectbox("상대방과의 관계 👀", ["친구", "썸/연애", "가족", "선배/후배", "선생님/멘토", "기타"])
    mood = st.selectbox("대화 분위기 😶", ["잘 모르겠음", "기분 좋음 🙂", "살짝 예민함 😶‍🌫️", "힘들어 보임 😢", "장난치는 분위기 😂"])
    chat_log = st.text_area("최근 대화 내용 ✏️", height=200, placeholder="예) 나: 요즘 너무 바쁘지?\n친구: 그니까 ㅠ 시험이랑 과제가 너무 많아…")

    if st.button("💡 답변 추천 받기"):
        if not chat_log.strip():
            st.warning("먼저 대화 내용을 조금만 적어 주세요! 🤏")
        else:
            st.markdown("### ✨ 추천 답변 예시 (AI 생성)")
            try:
                prompt = f"""
상대방과의 관계: {rel}
대화 분위기: {mood}
최근 대화:
{chat_log}

상황을 자연스럽게 이어가며 부담 없고 따뜻한 3가지 답변을 만들어줘.
"""
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user","content":prompt}],
                    temperature=0.7,
                )
                ai_replies = response.choices[0].message.content.strip().split("\n")
                for i, msg in enumerate(ai_replies, start=1):
                    if msg.strip():
                        st.info(f"추천 답변 {i}\n\n{msg.strip()}")
            except Exception as e:
                st.error(f"AI 답변 생성 오류: {e}")

elif page == "패션 & 퍼스널 컬러 👗":
    st.markdown("## 코디 추천 👗")
    line()
    style_mood = st.selectbox("오늘의 스타일 무드 😎", ["귀엽게 💕", "시크하게 🖤", "공부하러 가는 날 📚", "사진 많이 찍는 날 📸", "편하게 🛋️"])
    uploaded_image = st.file_uploader("얼굴 사진 업로드 (퍼스널 컬러 분석용) 📸", type=["jpg","jpeg","png"])

    if st.button("👗 퍼스널 컬러 분석"):
        if not uploaded_image:
            st.warning("먼저 얼굴 사진을 업로드 해 주세요.")
        else:
            image = Image.open(uploaded_image).convert("RGB")
            np_image = np.array(image)
            # 얼굴 영역 단순 중앙 crop
            h, w, _ = np_image.shape
            crop = np_image[h//4:h*3//4, w//4:w*3//4, :]
            avg_color = crop.mean(axis=(0,1)).astype(int)
            st.write(f"추정 평균 색상 (RGB): {tuple(avg_color)}")
            color_block = np.zeros((50,50,3), dtype=np.uint8)
            color_block[:,:] = avg_color
            st.image(color_block, caption="추정 퍼스널 컬러")

elif page == "SNS 브랜딩 📸":
    st.markdown("## SNS 브랜딩 & 피드 추천 📸")
    line()
    msg = st.text_area("사진에 담고 싶은 메시지/분위기 🌈", placeholder="예) 오늘 너무 뿌듯한 하루였어!")
    vibe = st.selectbox("계정 전체 분위기", ["꾸안꾸 데일리", "공부/기록 계정", "갬성 사진 위주", "친구들이랑 노는 계정", "아직 잘 모르겠음"])

    if st.button("📸 브랜딩 추천 받기"):
        if not msg.strip():
            st.warning("메시지를 간단히 적어 주세요! ✏️")
        else:
            st.markdown("### ✨ 추천 브랜딩 요소")
            if any(k in msg for k in ["공부","기록","노트","플래너","과제"]):
                filter_rec = "화이트 톤 깔끔 필터"
                font_rec = "얇은 산세리프 폰트"
                music_rec = "잔잔한 Lofi/공부 브금"
            elif any(k in msg for k in ["밤","야경","별"]):
                filter_rec = "어두운 배경 + 네온/보라빛 필터"
                font_rec = "네온사인 느낌 폰트"
                music_rec = "몽환적 R&B/시티팝"
            else:
                filter_rec = "자연광 느낌 필터"
                font_rec = "깔끔 산세리프"
                music_rec = "잔잔한 BGM"
            st.write(f"- 추천 필터: {filter_rec}")
            st.write(f"- 추천 폰트 스타일: {font_rec}")
            st.write(f"- 추천 음악/사운드: {music_rec}")

# =========================================================
# 요즘 밈 설명
# =========================================================
elif page == "요즘 밈 설명 😂":
    st.markdown("## 요즘 밈 설명서 😂")
    line()
    meme = st.selectbox("궁금한 밈", ["선택 안 함","어? 왜 안돼요?","멍 때리다 현실 복귀","00학번 갬성"])
    if meme == "어? 왜 안돼요?":
        st.write("갑자기 에러가 나거나 당황할 때 쓰는 밈입니다.")
    elif meme == "멍 때리다 현실 복귀":
        st.write("멍하다가 갑자기 현실로 돌아올 때 쓰는 짤입니다.")
    elif meme == "00학번 갬성":
        st.write("옛날 디카/필카 느낌 필터 밈입니다.")

# =========================================================
# 오늘의 밤티 점수
# =========================================================
elif page == "오늘의 밤티 점수 🔮":
    st.markdown("## 오늘의 밤티 점수 분석 🔮")
    line()
    st.write("각 항목을 오늘 기분대로 선택 (1 = 전혀 아니다, 5 = 매우 그렇다)")
    q1 = st.slider("대화할 준비 😄", 1,5,3)
    q2 = st.slider("옷차림 만족 👗", 1,5,3)
    q3 = st.slider("SNS에 올리고 싶은 마음 📸",1,5,3)
    q4 = st.slider("멘탈 안정 🧠",1,5,3)
    q5 = st.slider("새로운 도전 정신 🚀",1,5,3)

    if st.button("🔮 오늘의 밤티 점수 보기"):
        raw_score = q1 + q2 + q3 + q4 + q5
        max_score = 25
        score = int(raw_score / max_score * 100)
        st.markdown("### ✨ 오늘의 밤티 종합 점수")
        st.metric("오늘의 BAME 밤티 점수", f"{score} / 100")

        if score >= 80:
            msg = "오늘 밤티 점수 최상위 💜 무엇을 해도 잘 풀릴 기세예요."
        elif score >= 60:
            msg = "오늘 꽤 괜찮은 상태예요 🙂 약간의 휴식만 챙기면 부드럽게 흘러갈 거예요."
        elif score >= 40:
            msg = "조금 피곤하거나 예민할 수 있는 날이에요. 오늘은 가볍게 기록만 남겨도 좋아요 🌱"
        else:
            msg = "지금은 쉬어야 하는 타이밍일 수도 있어요. 낮은 점수도 괜찮아요. 충전의 시간입니다 ☁️"

        st.info(msg)
        st.caption("※ 원형 차트 없이 점수만 표시하도록 구성됨.")
