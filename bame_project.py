# -*- coding: utf-8 -*-
import streamlit as st
import random
from PIL import Image
import numpy as np
import colorsys
import re
import openai

# ---------------- 기본 설정 ----------------
st.set_page_config(
    page_title="BAME - Bamti Escape",
    page_icon="💜",
    layout="wide",
)

st.sidebar.title("BAME")
openai.api_key = st.secrets["openai"]["api_key"]

# ---------------- 공용 함수 ----------------
def line():
    st.markdown("---")

def rgb_to_hex(rgb):
    return "#{:02X}{:02X}{:02X}".format(*rgb)

def hex_to_rgb(hex_color):
    hex_color = hex_color.strip().lstrip("#")
    if len(hex_color) == 6:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    return None

def image_center_crop(np_image, ratio=0.5):
    h, w, _ = np_image.shape
    ch = int(h * ratio)
    cw = int(w * ratio)
    h_start = (h - ch) // 2
    w_start = (w - cw) // 2
    return np_image[h_start:h_start+ch, w_start:w_start+cw, :]

def calc_mean_color(np_image):
    crop = image_center_crop(np_image, ratio=0.5)
    avg = crop.mean(axis=(0, 1)).astype(int)
    return tuple(avg)

def calc_mean_hsv(np_image):
    crop = image_center_crop(np_image, ratio=0.5)
    pixels = crop.reshape(-1, 3) / 255.0
    hsv = np.array([colorsys.rgb_to_hsv(*p) for p in pixels])
    h_mean = float(np.mean(hsv[:, 0])) * 360.0
    s_mean = float(np.mean(hsv[:, 1])) * 100.0
    v_mean = float(np.mean(hsv[:, 2])) * 100.0
    return (round(h_mean, 1), round(s_mean, 1), round(v_mean, 1))

def show_color_block(rgb, caption=None):
    block = np.zeros((60, 60, 3), dtype=np.uint8)
    block[:, :] = rgb
    st.image(block, caption=caption if caption else rgb_to_hex(rgb), use_column_width=False)

def parse_lines(text):
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    cleaned = []
    for l in lines:
        cleaned.append(re.sub(r"^[\-\d\.\)\s]+", "", l))
    return cleaned

# ---------------- 퍼스널 컬러 분류 ----------------
def seasonal_classify(h, s, v):
    if 20 <= h <= 50 and s > 40 and v > 60:
        return "봄웜 (Spring Warm)"
    elif 150 <= h <= 200 and s < 40 and v > 50:
        return "여름쿨 (Summer Cool)"
    elif 30 <= h <= 60 and s > 40 and v < 60:
        return "가을웜 (Autumn Warm)"
    elif 180 <= h <= 260 and v > 60:
        return "겨울쿨 (Winter Cool)"
    else:
        return "중립톤 (Neutral)"

palettes = {
    "봄웜 (Spring Warm)": ["#FFD1DC", "#FFFACD", "#B0E0E6"],
    "여름쿨 (Summer Cool)": ["#AEC6CF", "#CFCFC4", "#E6E6FA"],
    "가을웜 (Autumn Warm)": ["#C19A6B", "#556B2F", "#FFD700"],
    "겨울쿨 (Winter Cool)": ["#0000FF", "#000000", "#FFFFFF"],
    "중립톤 (Neutral)": ["#808080", "#D3D3D3", "#A9A9A9"]
}

# ---------------- 사이드 페이지 ----------------
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

# =========================================================
# HOME
# =========================================================
if page == "HOME 🏠":
    st.markdown("## BAME (Bamti Escape)")
    line()
    st.write("현대인의 소통 부담, 패션 고민, SNS 경쟁력 부족을 한 번에 해결하는 통합형 자기관리 앱")

# =========================================================
# 대화 코치
# =========================================================
elif page == "대화 코치 💬":
    st.markdown("## 대화 코치 💬")
    line()
    rel = st.selectbox("상대방과의 관계 👀", ["친구", "썸/연애", "가족", "선배/후배", "선생님/멘토", "기타"])
    mood = st.selectbox("대화 분위기 😶", ["잘 모르겠음", "기분 좋음 🙂", "살짝 예민함 😶‍🌫️", "힘들어 보임 😢", "장난치는 분위기 😂"])
    chat_log = st.text_area("최근 대화 내용 ✏️", height=200)

    if st.button("💡 답변 추천 받기"):
        if not chat_log.strip():
            st.warning("대화 내용을 입력해 주세요.")
        else:
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
            ai_replies = parse_lines(response.choices[0].message.content.strip())
            for i, msg in enumerate(ai_replies[:3], start=1):
                st.info(f"추천 답변 {i}\n\n{msg}")

# =========================================================
# 패션 & 퍼스널 컬러
# =========================================================
elif page == "패션 & 퍼스널 컬러 👗":
    st.markdown("## 퍼스널 컬러 & 코디 추천 👗")
    line()
    style_mood = st.selectbox(
        "오늘의 스타일 무드 😎",
        ["귀엽게 💕", "시크하게 🖤", "공부하러 가는 날 📚", "사진 많이 찍는 날 📸", "편하게 🛋️"]
    )
    uploaded_image = st.file_uploader("얼굴 사진 업로드 📸", type=["jpg","jpeg","png"])

    if st.button("👗 퍼스널 컬러 + 코디 분석"):
        if not uploaded_image:
            st.warning("얼굴 사진을 업로드 해 주세요.")
        else:
            image = Image.open(uploaded_image).convert("RGB")
            np_image = np.array(image)
            avg_rgb = calc_mean_color(np_image)
            h_mean, s_mean, v_mean = calc_mean_hsv(np_image)
            season = seasonal_classify(h_mean, s_mean, v_mean)

            st.write(f"분류 결과: {season}")
            st.write("추천 팔레트:")
            for hex_color in palettes[season]:
                show_color_block(hex_to_rgb(hex_color), caption=hex_color)

            # AI 코디 추천
            prompt = f"""
당신의 퍼스널 컬러는 {season} 입니다.
오늘의 스타일 무드는 {style_mood} 입니다.

퍼스널 컬러와 무드에 맞는 오늘의 코디를 추천해줘.
- 상의/하의/원피스/액세서리/신발 중 3~4가지 아이템
- 색상은 퍼스널 컬러 팔레트와 잘 어울리게
- 설명은 간단하고 직관적으로
"""
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}],
                temperature=0.8,
            )
            st.markdown("### ✨ 오늘의 코디 추천")
            st.write(response.choices[0].message.content.strip())
# =========================================================
# SNS 브랜딩
# =========================================================
elif page == "SNS 브랜딩 📸":
    st.markdown("## SNS 브랜딩 & 피드 추천 📸")
    line()
    msg = st.text_area("사진에 담고 싶은 메시지/분위기 🌈", height=120)
    vibe = st.selectbox("계정 전체 분위기", ["꾸안꾸 데일리", "공부/기록 계정", "갬성 사진 위주", "친구들이랑 노는 계정", "아직 잘 모르겠음"])
    photo = st.file_uploader("올릴 사진 추가 📷", type=["jpg","jpeg","png"])

    if st.button("📸 AI 브랜딩 추천 받기"):
        if not msg.strip():
            st.warning("메시지를 입력해 주세요.")
        else:
            prompt = f"""
사용자가 올릴 사진 분위기: {vibe}
메시지: {msg}

위 정보를 바탕으로 인스타그램 브랜딩 요소를 추천해줘.
- 필터 스타일
- 폰트 스타일
- 음악/사운드
- 캡션 문구
- 스티커/그래픽 요소
"""
            response = openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}],
                temperature=0.8,
            )
            st.markdown("### ✨ 추천 브랜딩 요소")
            st.write(response.choices[0].message.content.strip())
            if photo:
                st.image(photo, caption="업로드한 사진 미리보기", use_column_width=True)

# =========================================================
# 요즘 밈 설명 (매거진/칼럼 스타일, 줄글 전체)
# =========================================================
elif page == "요즘 밈 설명 😂":
    st.markdown("## 요즘 밈 설명서 😂")
    line()
    st.markdown("### 📰 이번 달 밈 매거진")

    # 내 골반이 멈추지 않는 탓일까
    with st.container(border=True):
        st.markdown("### 🕺 내 골반이 멈추지 않는 탓일까?")
        st.write(
            "요즘 SNS를 스크롤하다 보면, 어느 순간 “내 골반이 멈추지 않는 탓일까?”라는 자막과 함께 "
            "경쾌하게 춤추는 영상이 눈에 들어온다. ... (중략, 전체 줄글 그대로 넣기)"
        )

    line()

    # 밤티
    with st.container(border=True):
        st.markdown("### 🌙 밤티")
        st.write(
            "온라인 커뮤니티를 조금만 들여다보면 ‘밤티’라는 단어가 자주 눈에 띈다. ... (중략)"
        )

    line()

    # 아자스
    with st.container(border=True):
        st.markdown("### 🙌 아자스")
        st.write(
            "최근 온라인과 SNS를 중심으로 젊은 세대 사이에서 유행하는 ‘아자스’라는 표현을 마주할 때면, ... (중략)"
        )

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
