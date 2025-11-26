import streamlit as st
import random

# ---------------- 공통 설정 ----------------
st.set_page_config(
    page_title="BAME - Bamti Escape",
    page_icon="💜",
    layout="wide",
)

# ---------------- 사이드바 ----------------
st.sidebar.title("BAME (Bamti Escape) 💜")
st.sidebar.write("SNS 시대 통합 자기관리 플랫폼")

page = st.sidebar.radio(
    "메뉴를 선택해 주세요",
    [
        "HOME 🏠",
        "대화 코치 (카톡/DM) 💬",
        "패션 & 퍼스널 컬러 👗",
        "SNS 브랜딩 & 피드 추천 📸",
        "요즘 밈 설명서 😂",
        "오늘의 밤티 점수 🔮",
    ],
)

# ---------------- 공통 헤더 함수 ----------------
def header_title(title, subtitle=None):
    st.markdown(f"## {title}")
    if subtitle:
        st.write(subtitle)
    st.markdown("---")


# ---------------- HOME ----------------
if page == "HOME 🏠":
    header_title(
        "BAME (Bamti Escape) 💜",
        "SNS 시대에 맞춘 **대화·패션·브랜딩** 통합 자기관리 앱 데모입니다.",
    )

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🧾 앱 소개")
        st.write(
            """
BAME는  
- **대화 코칭(카톡·DM)**  
- **패션 & 퍼스널 컬러 기반 코디 추천**  
- **SNS 피드/스토리 브랜딩**  

을 한 번에 도와주는 통합 플랫폼이에요.  
사용자가 자연스럽게 매력을 키우고, 인플루언서처럼 성장할 수 있도록 돕는 것을 목표로 합니다. ✨
"""
        )

        st.markdown("### 🎯 개발 목표")
        st.write(
            """
- SNS 소통 부담, 패션 고민, SNS 경쟁력 부족을 한 번에 해결  
- 사용자의 **대화 내용·옷장·피드 분위기**를 분석해 맞춤형 추천  
- ‘밤티 점수’ 분석으로 오늘의 나를 점검하고 성장 포인트 제안
"""
        )

    with col2:
        st.markdown("### 👥 팀 정보")
        st.write("**팀원 1:** 강민서")
        st.write("**팀원 2:** 신수아")
        st.write("**소프트웨어 명:** BAME (Bamti Escape)")
        st.success("이 화면은 실제 서비스 기획을 스트림릿으로 시연하는 데모입니다 🙂")

# ---------------- 대화 코치 ----------------
elif page == "대화 코치 (카톡/DM) 💬":
    header_title(
        "대화 코치 (카톡/DM 분석) 💬",
        "상대방과의 관계와 대화 내용을 분석해 **자연스러운 답변**을 추천해 줍니다.",
    )

    rel = st.selectbox(
        "상대방과의 관계를 골라 주세요 👀",
        ["친구", "썸/연애", "가족", "선배/후배", "선생님/멘토", "기타"],
    )

    mood = st.selectbox(
        "상대방의 현재 분위기는 어떤가요? (느낌대로 골라보기) 😶",
        ["잘 모르겠음", "기분 좋음 🙂", "살짝 예민함 😶‍🌫️", "힘들어 보임 😢", "장난치는 분위기 😂"],
    )

    chat_log = st.text_area(
        "최근 카톡/DM 대화 내용을 붙여 넣어 주세요 (중요한 부분만 적어도 좋아요) ✏️",
        height=200,
        placeholder="예) 나: 요즘 너무 바쁘지?\n친구: 그니까 ㅠ 시험이랑 과제가 너무 많아…",
    )

    if st.button("💡 답변 추천 받기"):
        if not chat_log.strip():
            st.warning("먼저 대화 내용을 조금만 적어 주세요! 🤏")
        else:
            st.markdown("### ✨ 추천 답변 예시")
            suggestions = []

            # 아주 간단한 키워드 기반 예시 (진짜 AI 모델 대신 규칙으로만 데모)
            lower_log = chat_log.lower()

            if any(k in lower_log for k in ["시험", "숙제", "과제", "바빠", "공부"]):
                suggestions.append(
                    "요즘 진짜 너무 빡세지 ㅠㅠ 그래도 너라면 잘 해낼 거 같아. 필요하면 같이 공부 계획 짜보자! 📚"
                )
            if any(k in lower_log for k in ["힘들", "우울", "멘탈", "스트레스", "짜증"]):
                suggestions.append(
                    "괜찮아? 얘기 들어줄 사람 필요하면 나 불러. 지금 당장이 아니어도 언제든 편할 때 말해줘 💌"
                )
            if any(k in lower_log for k in ["고마워", "고맙", "thanks", "thx"]):
                suggestions.append(
                    "나도 항상 고마워! 너 있어서 진짜 든든해 😊 다음에 간식이라도 하나 사줄게 🍪"
                )
            if any(k in lower_log for k in ["보고 싶", "보고싶", "그리워"]):
                suggestions.append(
                    "나도 진짜 보고 싶다구 ㅠ 언제 한 번 시간 맞춰서 꼭 보자! 일정 한 번 맞춰볼까? 📅"
                )

            # 관계/분위기 토핑
            if rel in ["썸/연애"]:
                suggestions.append(
                    "너 힘든 얘기 해줘서 고마워. 네 옆에서 오래 듣고 싶어, 부담 안 되는 선에서만 말해줘 💜"
                )
            elif rel in ["선배/후배", "선생님/멘토"]:
                suggestions.append(
                    "항상 응원하고 있어요! 혹시 도움이 필요하면 언제든 편하게 말씀해 주세요 🙂"
                )

            if not suggestions:
                suggestions.append(
                    "그랬구나..! 네 얘기 들어보니까 그냥 넘길 일이 아닌 것 같아. 자세히 듣고 싶은데, 괜찮다면 조금만 더 말해줄래? 🌱"
                )

            for i, msg in enumerate(suggestions, start=1):
                st.info(f"**추천 답변 {i}**\n\n{msg}")

            st.markdown(
                "> ※ 실제 서비스에서는 **감정 분석·맥락 분석 모델**을 이용해 훨씬 더 정교한 답변을 추천하게 됩니다."
            )

# ---------------- 패션 & 퍼스널 컬러 ----------------
elif page == "패션 & 퍼스널 컬러 👗":
    header_title(
        "패션 & 퍼스널 컬러 코디 추천 👗",
        "퍼스널 컬러와 오늘의 분위기에 맞춰 **코디 아이디어**를 제안해 줍니다.",
    )

    col1, col2 = st.columns(2)

    with col1:
        personal_color = st.selectbox(
            "나의 퍼스널 컬러 톤을 골라 주세요 🎨",
            ["모르겠음", "봄 웜", "여름 쿨", "가을 웜", "겨울 쿨"],
        )

        style_mood = st.selectbox(
            "오늘의 스타일 무드는? 😎",
            ["귀엽게 💕", "시크하게 🖤", "공부하러 가는 날 📚", "사진 많이 찍는 날 📸", "편하게 🛋️"],
        )

        weather = st.selectbox(
            "오늘 날씨는 어때요? 🌤️",
            ["상관 없음", "더움 🔥", "선선함 🍃", "추움 ❄️"],
        )

    with col2:
        items = st.multiselect(
            "오늘 입을 수 있는 옷 아이템을 골라 주세요 (여러 개 선택 가능) 👕",
            ["후드티", "셔츠", "블라우스", "니트", "청바]()

