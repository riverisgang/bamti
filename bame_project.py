# -*- coding: utf-8 -*-
import streamlit as st
import random
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import openai
import face_recognition

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
            try:
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role":"user","content":prompt}],
                    temperature=0.7,
                )
                
                message_content = response['choices'][0]['message']['content']
                
                for msg in message_content.split("\n"):
                    clean_msg = msg.strip()
                    if clean_msg:
                        st.markdown(f"<div class='card'>{clean_msg}</div>", unsafe_allow_html=True)
                        
            except Exception as e:
                st.error(f"AI 답변 생성 오류 발생: {e}")

# ----------------- 패션 & 퍼스널 컬러 -----------------
elif page == "패션 & 퍼스널 컬러 👗":
    st.markdown("## 패션 & 퍼스널 컬러 코디 추천 👗")
    st.write("퍼스널 컬러와 옷장 아이템 기반 코디 추천")
    line()
    col1, col2 = st.columns(2)
    with col1:
        style_mood = st.selectbox("스타일 무드 😎", ["귀엽게 💕","시크하게 🖤","공부하러 가는 날 📚","사진 많이 찍는 날 📸","편하게 🛋️"])
        weather = st.selectbox("날씨 🌤️", ["상관 없음","더움 🔥","선선함 🍃","추움 ❄️"])
    with col2:
        items = st.multiselect("오늘 입을 옷 👕", ["후드티","셔츠","블라우스","니트","청바지","슬랙스","스커트","원피스","운동화","로퍼","부츠"])
        acc = st.multiselect("액세서리 💍", ["모자","목걸이","귀걸이","시계","가방","헤어핀"])
        face_img = st.file_uploader("얼굴 이미지 업로드 (퍼스널 컬러 분석)", type=["png","jpg","jpeg"])

    if st.button("👗 코디 추천"):
        st.markdown("### ✨ 오늘의 코디 제안")
        if face_img:
            img = Image.open(face_img).convert("RGB")
            img_arr = np.array(img)

            # 얼굴 위치 감지 (face_recognition 사용)
            face_locations = face_recognition.face_locations(img_arr)
            if face_locations:
                top, right, bottom, left = face_locations[0]
                face_region = img_arr[top:bottom, left:right]

                avg_color = face_region.mean(axis=(0,1)).astype(int)
                st.write(f"- 얼굴 평균 RGB: {tuple(avg_color)}")

                R, G, B = avg_color
                if R > B:
                    tone = "Warm"
                    palette = ["#FFDAB9", "#FF7F50", "#FFE4B5"]
                else:
                    tone = "Cool"
                    palette = ["#ADD8E6", "#87CEFA", "#9370DB"]

                st.write(f"- 분석 톤: {tone}")

                fig, ax = plt.subplots(figsize=(4,1))
                ax.imshow([palette])
                ax.axis('off')
                st.pyplot(fig)
            else:
                st.warning("얼굴을 찾을 수 없습니다.")
        else:
            st.info("얼굴 이미지를 업로드하면 자동으로 퍼스널 컬러 분석이 가능합니다.")

        # 스타일 & 아이템 출력
        style_msg = {
            "귀엽게 💕":"루즈핏 상의 + 밝은 하의",
            "시크하게 🖤":"올블랙 또는 블랙+그레이",
            "공부하러 가는 날 📚":"편한 상의 + 넉넉한 바지 + 운동화",
            "사진 많이 찍는 날 📸":"대비되는 색 하나 포함",
            "편하게 🛋️":"후드티/니트 + 편한 바지"
        }
        st.write(f"- 스타일 무드: {style_msg.get(style_mood)}")
        if items:
            st.write(f"- 선택 아이템 활용: {', '.join(items)}")
        if acc:
            st.write(f"- 액세서리 포인트: {', '.join(acc)}")

# ----------------- SNS 브랜딩 -----------------
elif page == "SNS 브랜딩 📸":
    st.markdown("## SNS 브랜딩 & 피드 추천 📸")
    st.write("사진 기반 필터, 폰트, 음악, 스티커 추천")
    line()
    msg = st.text_area("전달하고 싶은 메시지 🌈", placeholder="오늘 너무 뿌듯한 하루였어!")
    vibe = st.selectbox("계정 분위기", ["꾸안꾸 데일리","공부/기록","갬성 사진","친구들과","아직 잘 모르겠음"])
    img_file = st.file_uploader("사진 업로드", type=["png","jpg","jpeg"])
    if st.button("📸 브랜딩 추천"):
        if not msg.strip():
            st.warning("메시지를 입력해주세요")
        else:
            st.markdown("### ✨ 추천 브랜딩 요소")
            st.write("- 추천 필터: 자연광 느낌 필터")
            st.write("- 추천 폰트: 깔끔한 산세리프 폰트")
            st.write("- 추천 음악/사운드: 잔잔한 BGM")
            st.write("- 스티커 사용 팁: 하트, 별, 체크리스트 스티커")
            st.write("- 캡션 작성 팁: 짧은 한 문장 + 구체적 이야기")

# ----------------- 밈 설명 -----------------
elif page == "요즘 밈 설명 😂":
    st.markdown("## 요즘 밈 설명")
    meme = st.selectbox("궁금한 밈", ["선택 안 함","어? 왜 안돼요?","멍 때리다 현실 복귀","00학번 갬성","전체 설명"])
    if meme=="어? 왜 안돼요?":
        st.write("에러나거나 이해 안될 때 귀엽게 당황한 밈")
    elif meme=="멍 때리다 현실 복귀":
        st.write("멍하다가 갑자기 현실로 돌아올 때 쓰는 짤")
    elif meme=="00학번 갬성":
        st.write("옛날 디카/필카 느낌 필터")

# ----------------- 오늘의 밤티 점수 -----------------
elif page == "오늘의 밤티 점수 🔮":
    st.markdown("## 오늘의 밤티 점수 🔮")
    st.write("점수가 높을수록 안 좋음 🔥")
    line()
    q1 = st.slider("대화 준비 😄",1,5,3)
    q2 = st.slider("옷차림 만족 👗",1,5,3)
    q3 = st.slider("SNS 올릴 의향 📸",1,5,3)
    q4 = st.slider("멘탈 안정 🧠",1,5,3)
    q5 = st.slider("도전 정신 🚀",1,5,3)
    if st.button("🔮 점수 보기"):
        score = int((q1+q2+q3+q4+q5)/25*100)
        st.metric("오늘의 밤티 점수", f"{score}/100")
        fig, ax = plt.subplots()
        ax.pie([score,100-score], labels=["점수","남은"], colors=["#ff6f61","#cfcfcf"], startangle=90, counterclock=False)
        st.pyplot(fig)
        if score>=80:
            msg="오늘 밤티 점수 최상위 💜 충전 필요"
        elif score>=60:
            msg="오늘 꽤 괜찮아요 🙂 약간 휴식만"
        elif score>=40:
            msg="조금 피곤하거나 예민할 수 있어 🌱"
        else:
            msg="휴식 권장 ☁️"
        st.info(msg)
