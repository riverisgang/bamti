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

def warm_cool_classify(avg_rgb):
    r, g, b = avg_rgb
    h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
    hue_deg = h * 360
    red_bias = r - b
    if red_bias >= 10 or (30 <= hue_deg <= 70):
        return "warm"
    if red_bias <= -10 or (180 <= hue_deg <= 260):
        return "cool"
    return "neutral"

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
    st.write("bamtiescape.streamlit.app")
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
    st.markdown("## 코디 추천 👗")
    line()
    style_mood = st.selectbox("오늘의 스타일 무드 😎", ["귀엽게 💕", "시크하게 🖤", "공부하러 가는 날 📚", "사진 많이 찍는 날 📸", "편하게 🛋️"])
    uploaded_image = st.file_uploader("얼굴 사진 업로드 📸", type=["jpg","jpeg","png"])

    if st.button("👗 퍼스널 컬러 분석"):
        if not uploaded_image:
            st.warning("얼굴 사진을 업로드 해 주세요.")
        else:
            image = Image.open(uploaded_image).convert("RGB")
            np_image = np.array(image)
            avg_rgb = calc_mean_color(np_image)
            h_mean, s_mean, v_mean = calc_mean_hsv(np_image)
            wc_type = warm_cool_classify(avg_rgb)

            st.write(f"평균 RGB: {avg_rgb} / HEX: {rgb_to_hex(avg_rgb)}")
            st.write(f"HSV 평균: Hue {h_mean}°, Saturation {s_mean}%, Value {v_mean}%")
            st.write(f"분류: {wc_type.upper()} 계열")
            show_color_block(avg_rgb, caption="추정 퍼스널 컬러")

# =========================================================
# SNS 브랜딩 (AI 모델 연동)
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
            "경쾌하게 춤추는 영상이 눈에 들어온다. 단순한 유행을 넘어, 이 밈은 디지털 세대가 몸과 리듬으로 "
            "소통하는 새로운 방식의 언어로 자리 잡았다.\n\n"
            "이 밈의 매력은 직관적이라는 점이다. 긴 설명 없이도 한눈에 ‘리듬’, ‘분위기’, ‘유머’가 전달된다. "
            "친구와 공유할 때, 댓글로 반응할 때, 짧은 영상 한 편이 모두의 공감을 즉시 만들어낸다. "
            "음악과 움직임, 텍스트가 결합된 이 작은 숏폼 속에서 사람들은 웃고, 따라 하고, 변주하며 "
            "자신만의 해석을 덧붙인다.\n\n"
            "밈은 짧지만 강렬하다. 순간적으로 소비되고, 또 빠르게 다음 트렌드로 넘어가지만, 동시에 세대의 감각과 유머, "
            "그리고 디지털 소통 방식을 반영하는 거울이 된다. “내 골반이 멈추지 않는 탓일까?”라는 한마디가 전하는 웃음과 "
            "공감 속에서, 우리는 오늘도 새로운 리듬 위에서 소통한다.\n\n"
            "밈은 멈추지 않는 골반처럼, 언제나 다음 움직임을 기다린다. 그리고 우리는 그 리듬에 맞춰 또 한 번 웃고, "
            "반응하며, 춤춘다."
        )

    line()

    # 밤티
    with st.container(border=True):
        st.markdown("### 🌙 밤티")
        st.write(
            "온라인 커뮤니티를 조금만 들여다보면 ‘밤티’라는 단어가 자주 눈에 띈다. 한때는 단순히 게임 속 한 아바타의 이름에서 "
            "시작된 표현이었지만, 지금은 사람, 패션, 물건, 심지어 분위기까지도 가볍게 평가하는 밈 언어로 자리 잡았다.\n\n"
            "밤티의 매력은 짧고 직관적이라는 데 있다. 한마디로 사람들에게 인상적인 느낌을 전달할 수 있으며, 과장된 표현을 통해 "
            "재미와 유머를 동시에 담는다. “이번 옷 완전 밤티 난다”라고 하면, 촌스럽거나 과한 느낌을 바로 떠올리게 하면서도 웃음을 준다. "
            "말하자면, 밤티는 온라인 세대가 만들어낸 ‘감정 전달형 신조어’인 셈이다.\n\n"
            "흥미로운 점은 이 단어가 단순한 풍자나 평가에 그치지 않고, 자기 비하적 유머나 친근한 농담으로도 쓰인다는 것이다. "
            "“오늘 내 스타일 밤티 완전 폭발”이라는 식으로, 자신의 과장된 모습을 재치 있게 표현할 때도 활용된다. "
            "이처럼 밤티는 밈으로서 재미를 주는 동시에, 온라인 소통에서 자연스럽게 감정과 분위기를 전달하는 역할을 한다.\n\n"
            "결국 밤티는 단순한 유행어를 넘어, 디지털 시대 젊은 세대가 언어로 유머와 감정을 조율하는 방식의 한 예라고 할 수 있다. "
            "짧지만 강렬한 인상을 주는 한 단어 안에, 온라인 문화의 유연함과 재미가 고스란히 담겨 있는 셈이다. "
            "오늘도 우리는 댓글과 채팅 속에서, 웃음과 감정을 담아 ‘밤티’ 한 마디를 던지며 소통한다."
        )

    line()

    # 아자스
    with st.container(border=True):
        st.markdown("### 🙌 아자스")
        st.write(
            "최근 온라인과 SNS를 중심으로 젊은 세대 사이에서 유행하는 ‘아자스’라는 표현을 마주할 때면, "
            "그 단순한 세 글자 안에 담긴 문화적 의미가 묘하게 흥미롭다. 아자스는 일본어 ‘ありがとうございます(감사합니다)’의 "
            "구어체 축약형으로, 원래 일본 청년층 사이에서 쓰이던 친근한 감사 표현이 한국의 인터넷 커뮤니티와 댓글 문화 속으로 "
            "자연스럽게 흘러들어온 것이다. 짧고 경쾌한 발음 덕분에 댓글, 채팅, 영상 리액션 등 다양한 맥락에서 쉽게 쓰이면서 "
            "‘감사’를 넘어 ‘공감’, ‘인정’, ‘유머’의 의미까지 포괄하게 되었다.\n\n"
            "그런데 아자스가 흥미로운 이유는 단순히 외래어의 유행이라는 점에 있지 않다. 이것은 온라인 세대가 소통에서 원하는 것, "
            "즉 빠른 반응과 즉각적인 감정 공유, 그리고 친밀한 유대감을 한 단어로 담아내려는 시도의 결과다. 친구와의 대화에서, "
            "혹은 댓글에서 ‘아자스’라고 한마디 건네면, 단순한 감사의 의미를 넘어서 상대방을 향한 긍정과 공감, 때로는 유머러스한 "
            "드립까지 담아낼 수 있다.\n\n"
            "하지만 모든 유행어가 그렇듯, 아자스 역시 맥락을 벗어나면 오해를 부를 수 있다. 공식적인 자리나 처음 만난 사람과의 "
            "대화에서 사용하면 격식 없는 표현으로 비칠 수 있고, 일부 커뮤니티에서는 비판이나 냉소를 담은 뒤 ‘아자스’를 붙이는 방식으로 "
            "원래 의미를 흐리는 경우도 있다. 결국 언어는 의사소통의 도구이자 문화의 표현이라는 점에서, 친근하고 간결한 표현이라도 "
            "사용 맥락과 상대방을 고려하는 지혜가 필요하다.\n\n"
            "아자스는 세대와 문화가 만들어낸 언어적 유희이자, 시대가 요구하는 소통 방식의 한 단면이다. 짧은 단어 속에 감정과 공감, "
            "유머와 친밀감을 담아내는 능력은, 디지털 시대의 커뮤니케이션이 얼마나 빠르고 감각적이며 동시에 미묘하게 사회적 의미를 "
            "띠고 있는지를 보여준다. 그러나 그 속에 담긴 의미를 제대로 이해하지 못한 채 남용할 경우, 유머가 냉소로, 친근감이 무례로 "
            "변할 수 있다는 점을 잊어서는 안 된다. 아자스라는 단어는, 그래서 단순한 밈이 아니라, 디지털 문화 속 소통의 유연함과 "
            "책임을 동시에 생각하게 하는 작은 언어 실험인 셈이다."
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


