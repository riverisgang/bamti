# -*- coding: utf-8 -*-
import streamlit as st
import random
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import openai

# ---------------- OpenAI API ----------------
# ⚠️ 위험 감수하고 코드에 키 직접 입력
openai.api_key = "sk-여기에_실제_API_KEY_입력"

# ---------------- 기본 설정 ----------------
st.set_page_config(
    page_title="BAME - Bamti Escape",
    page_icon="💜",
    layout="wide",
)

# CSS 카드형 UI
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

# ----------------- 대화 코치 ------
