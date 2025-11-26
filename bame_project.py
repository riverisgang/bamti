import streamlit as st
import numpy as np
import cv2
from PIL import Image
import openai
import matplotlib.pyplot as plt

# ---------------------------
# 기본 설정
# ---------------------------
st.set_page_config(
    page_title="BAME - bamtiescape",
    page_icon="🌙",
    layout="centered"
)

openai.api_key = st.secrets["OPENAI_API_KEY"]

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
# AI 대화 추천
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
            model="gpt-4o-mini",
            messages=[{"role":"user", "content": prompt}],
            temperature=0.7
        )

        output = res.choices[0].message["content"].strip()
        replies = output.split("\n")
        replies = [r.replace("-", "").strip() for r in replies if r.strip()]
        return replies[:3]
    except:
        return ["⚠️ AI 요청에 문제가 발생했습니다. 다시 시도해주세요."]

# ---------------------------
# 퍼스널컬러 이미지 분석
# ---------------------------
def analyze_skin_tone(image):
    img = np.array(image)
    img_cv = cv2.cvtColor(img, cv2.COLOR_RGB2YCrCb)
    y, cr, cb = cv2.split(img_cv)

    avg_cr = np.mean(cr)
    avg_cb = np.mean(cb)
    avg_y = np.mean(y)

    if avg_cr > 140:
        tone = "Warm Tone"
        desc = "웜톤 (노란/골드 계열이 잘 어울려요!)"
    else:
        tone = "Cool Tone"
        desc = "쿨톤 (블루/실버 계열이 잘 어울려요!)"

    return tone, desc, avg_y, avg_cr, avg_cb

def show_palette(colors):
    fig, ax = plt.subplots(figsize=(4,1))
    ax.imshow([colors])
    ax.set_xticks([])
    ax.set_yticks([])
    st.pyplot(fig)


# ---------------------------
# 페이지 구분
# ---------------------------
st.sidebar.title("🌙 BAME")
page = st.sidebar.radio(
    "메뉴",
    ["Home", "대화 코치(AI)", "퍼스널컬러 분석", "SNS 브랜딩(보류)", "밈 설명", "오늘의 밤티 점수"]
)

# ---------------------------
# HOME
# ---------------------------
if page == "Home":
    st.markdown(f"""
        <h1 style="color:{PRIMARY}; font-weight:700;">🌙 BAME (bamtiescape)</h1>
        <p style="color:{PRIMARY};">
        현대인의 SNS·대화·패션 고민을 한 번에 해결하는 통합 자기관리 앱입니다.
        </p>
    """, unsafe_allow_html=True)

    card("✔ AI 기반 대화 코치로 자연스러운 답변 추천")  
    card("✔ 이미지 기반 퍼스널컬러 분석 및 코디 가이드")
    card("✔ SNS 브랜딩 기능(업데이트 예정)")
    card("✔ 최신 밈 설명 제공")
    card("✔ ‘밤티 점수’로 오늘의 상태 체크")

# ---------------------------
# AI 대화 코치
# ---------------------------
elif page == "대화 코치(AI)":
    st.subheader("💬 AI 대화 코치")

    relationship = st.selectbox("상대방과의 관계", ["친구", "썸", "연인", "직장/업무", "가족"])
    mood = st.selectbox("대화 분위기", ["가벼움", "진지함", "어색함", "설렘"])
    chat_log = st.text_area("최근 대화 내용을 붙여넣어주세요")

    if st.button("AI 답변 생성"):
        replies = ai_generate_replies(relationship, mood, chat_log)
        st.markdown("### ✨ 추천 답변")
        for r in replies:
            card(r)

# ---------------------------
# 퍼스널컬러 자동 분석
# ---------------------------
elif page == "퍼스널컬러 분석":
    st.subheader("🎨 퍼스널컬러 자동 분석")

    img_file = st.file_uploader("얼굴이 보이는 사진을 업로드해주세요", type=["jpg","jpeg","png"])

    if img_file is not None:
        image = Image.open(img_file).convert("RGB")
        st.image(image, caption="업로드한 이미지", use_column_width=True)

        tone, desc, y, cr, cb = analyze_skin_tone(image)

        st.markdown(f"### 🔍 분석 결과: **{tone}**")
        card(desc)

        st.markdown("### 🎨 평균 톤 정보")
        card(f"밝기(Y): {y:.2f} | Cr: {cr:.2f} | Cb: {cb:.2f}")

        st.markdown("### 추천 컬러 팔레트")
        if tone == "Warm Tone":
            palette = [[255,204,153], [255,153,102], [204,153,102], [153,102,51]]
        else:
            palette = [[153,204,255], [102,153,255], [102,102,204], [51,51,153]]
        palette = [np.array(p)/255 for p in palette]
        show_palette(palette)

# ---------------------------
# SNS 브랜딩 (보류)
# ---------------------------
elif page == "SNS 브랜딩(보류)":
    st.subheader("📷 SNS 브랜딩 기능")
    card("현재 재구성 중입니다! 곧 더 완성도 높은 버전으로 돌아올게요 ✨")

# ---------------------------
# 밈 설명
# ---------------------------
elif page == "밈 설명":
    st.subheader("😂 최신 밈 설명")
    st.write("이 페이지는 너희 팀이 직접 콘텐츠 넣으면 돼!")

# ---------------------------
# 밤티 점수
# ---------------------------
elif page == "오늘의 밤티 점수":
    st.subheader("🌙 오늘의 밤티 점수")
    st.write("현재 기본 버전입니다. 추후 강화 가능!")
