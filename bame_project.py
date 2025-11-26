import streamlit as st
import numpy as np
from PIL import Image
import openai
import matplotlib.pyplot as plt

# ---------------------------
# OpenAI API 키 로드 (Secret 방식)
# ---------------------------
openai.api_key = st.secrets["OPENAI_API_KEY"]

# ---------------------------
# 기본 UI 설정
# ---------------------------
st.set_page_config(
    page_title="BAME - bamtiescape",
    page_icon="🌙",
    layout="centered"
)

PRIMARY = "#3D3B8E"
BG = "#F9F9F9"
PINK = "#FFD8D8"
MINT = "#B0E298"

def card(text):
    st.markdown(
        f"""
        <div style="
            background:{PINK};
            padding:18px;
            border-radius:14px;
            color:{PRIMARY};
            font-size:17px;
            margin-bottom:10px;
            box-shadow:0 0 6px rgba(0,0,0,0.1);
        ">
        {text}
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------
# AI 대화 코치
# ---------------------------
def ai_generate_replies(relation, mood, chat_log):
    prompt = f"""
상대방과의 관계: {relation}
대화 분위기: {mood}
최근 대화 내용:
{chat_log}

위 상황을 자연스럽게 이어가는 부담 없고 따뜻한 톤의 답변을 3개 생성해줘.
각 답변은 1~2문장 정도로 해줘.
"""
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role":"user","content":p]()
