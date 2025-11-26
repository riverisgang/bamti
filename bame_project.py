# -*- coding: utf-8 -*-
import streamlit as st
import random
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import openai

# ---------------- OpenAI API ----------------
openai.api_key = "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"

# ---------------- 기본 설정 ----------------
st.set_page_config(
    page_title="BAME - Bamti Escape",
    page_icon="💜",
    layout="wide",
)

st.markdown("""
<style>
.stApp {background-color: #fdf6ff;}
.card {padding:15px; margin:10px 0; border-radius:12px; background-color:#fff0f5; box-shadow:2px 2px 8px #d3d3d3;}
.title {color:#6a0dad; font-weight:bold;}
</style>
""", unsafe_allow_html=True)

st.sidebar.title("BAME (Bamti Escape) 💜")
st.sidebar.write("SNS 시대 통합 자기관리 앱 데모")

page = st.sidebar.radio(
    "메뉴 선택 👀",
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

# ----------------- HOME -----------------
if page == "HOME 🏠":
    st.markdown("## BAME (Bamti Escape) 💜")
    line()
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("### 🧾 앱 소개")
        st.write(
            "BAME는 대화, 패션, SNS 브랜딩을 한 번에 도와주는 통합 자기관리 앱입니다.\n"
            "- 카톡/DM 대화 코칭\n"
            "- 퍼스널 컬러 기반 코디 추천\n"
            "- 피드/스토리 브랜딩 가이드\n"
            "사용자가 자연스럽게 성장하도록 돕는 것을 목표로 합니다."
        )
        st.markdown("### 🎯 개발 목표")
        st.write(
            "현대 사회에서 SNS 활동은 필수적인 것으로 여겨집니다. "
            "BAME는 소통 부담, 패션 고민, SNS 경쟁력 부족을 한 번에 해결하며 "
            "사용자의 매력을 자연스럽고 입체적으로 성장시키는 것을 목표로 합니다. "
            "대화 추천, 코디 분석, 스토리 추천 기능 제공으로 사용자의 인플루언서 성장 가능성도 높여줍니다."
        )
    with col2:
        st.markdown("### 👥 팀 정보")
        st.write("**팀원 1:** 강민서")
        st.write("**팀원 2:** 신수아")
        st.success("이 화면은 실제 서비스 기획을 Streamlit으로 시연하는 데모입니다 🙂")

# ----------------- 대화 코치 -----------------
elif page == "대화 코치 💬":
    st.markdown("## 대화 코치 (카톡/DM 분석) 💬")
    st.write("상대방과의 관계, 대화 내용을 바탕으로 자연스러운 답변을 추천합니다.")
    line()

    rel = st.selectbox("상대방과의 관계 👀", ["친구", "썸/연애", "가족", "선배/후배", "선생님/멘토", "기타"])
    mood = st.selectbox("대화 분위기 😶", ["잘 모르겠음", "기분 좋음 🙂", "살짝 예민함 😶‍🌫️", "힘들어 보임 😢", "장난치는 분위기 😂"])
    chat_log = st.text_area("최근 카톡/DM 대화 기록 ✏️", height=200, placeholder="예) 나: 요즘 너무 바쁘지?\n친구: ㅠㅠ 시험이 많아…")

    if st.button("💡 AI 답변 추천"):
        if not chat_log.strip():
            st.warning("먼저 대화 내용을 입력해 주세요!")
        else:
            st.markdown("### ✨ 추천 답변")
            prompt = f"""
            상대방과의 관계: {rel}
            대화 분위기: {mood}
            최근 대화:
            {chat_log}

            상황을 자연스럽게 이어가며 부담 없고 따뜻한 3가지 답변을 만들어줘.
            """
