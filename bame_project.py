import streamlit as st
import random

# ---------------- 기본 설정 ----------------
st.set_page_config(
    page_title="BAME - Bamti Escape",
    page_icon="💜",
    layout="wide",
)

st.sidebar.title("BAME (Bamti Escape) 💜")
st.sidebar.write("SNS 시대 통합 자기관리 앱 데모")

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


# ---------------- HOME ----------------
if page == "HOME 🏠":
    st.markdown("## BAME (Bamti Escape) 💜")
    line()

    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 🧾 앱 소개")
        st.write(
            "BAME는 대화, 패션, SNS 브랜딩을 한 번에 도와주는 통합 자기관리 앱입니다. \n"
            "- 카톡/DM 대화 코칭\n"
            "- 퍼스널 컬러 기반 코디 추천\n"
            "- 피드/스토리 브랜딩 가이드\n"
            "를 통해 사용자가 자연스럽게 성장하도록 돕는 것을 목표로 합니다."
        )

        st.markdown("### 🎯 개발 목표")
        st.write(
            "- SNS 소통 부담과 패션 고민, SNS 경쟁력 부족을 한 번에 해결\n"
            "- 사용자의 대화 내용, 옷장, 피드 분위기를 분석해 맞춤형 추천 제공\n"
            "- 오늘의 상태를 밤티 점수로 분석해 성장 포인트 제안"
        )

    with col2:
        st.markdown("### 👥 팀 정보")
        st.write("**팀원 1:** 강민서")
        st.write("**팀원 2:** 신수아")
        st.write("**소프트웨어 명:** BAME (Bamti Escape)")
        st.success("이 화면은 실제 서비스 기획을 스트림릿으로 시연하는 데모입니다 🙂")


# ---------------- 대화 코치 ----------------
elif page == "대화 코치 💬":
    st.markdown("## 대화 코치 (카톡/DM 분석) 💬")
    st.write("상대방과의 관계, 분위기, 대화 내용을 바탕으로 자연스러운 답변을 추천합니다.")
    line()

    rel = st.selectbox(
        "상대방과의 관계를 골라 주세요 👀",
        ["친구", "썸/연애", "가족", "선배/후배", "선생님/멘토", "기타"],
    )

    mood = st.selectbox(
        "지금 대화 분위기는 어떤가요? 😶",
        ["잘 모르겠음", "기분 좋음 🙂", "살짝 예민함 😶‍🌫️", "힘들어 보임 😢", "장난치는 분위기 😂"],
    )

    chat_log = st.text_area(
        "최근 카톡/DM 대화 내용을 적어 주세요 (핵심만 적어도 괜찮아요) ✏️",
        height=200,
        placeholder="예) 나: 요즘 너무 바쁘지?\n친구: 그니까 ㅠ 시험이랑 과제가 너무 많아…",
    )

    if st.button("💡 답변 추천 받기"):
        if not chat_log.strip():
            st.warning("먼저 대화 내용을 조금만 적어 주세요! 🤏")
        else:
            st.markdown("### ✨ 추천 답변 예시")

            suggestions = []
            lower_log = chat_log.lower()

            if "시험" in chat_log or "과제" in chat_log or "공부" in chat_log or "바빠" in chat_log:
                suggestions.append(
                    "요즘 진짜 너무 빡세지 ㅠㅠ 그래도 너라면 잘 해낼 거 같아. 필요하면 같이 공부 계획 짜보자! 📚"
                )
            if "힘들" in chat_log or "멘탈" in chat_log or "우울" in chat_log or "스트레스" in chat_log:
                suggestions.append(
                    "괜찮아? 얘기 들어줄 사람 필요하면 나 불러. 당장 아니어도 편할 때 말해줘 💌"
                )
            if "고마워" in chat_log or "고맙" in chat_log or "thanks" in lower_log or "thx" in lower_log:
                suggestions.append(
                    "나도 항상 고마워! 너 있어서 진짜 든든해 😊 다음에 간식이라도 하나 사줄게 🍪"
                )
            if "보고 싶" in chat_log or "보고싶" in chat_log:
                suggestions.append(
                    "나도 진짜 보고 싶다 ㅠ 언제 한 번 시간 맞춰서 꼭 보자! 일정 한 번 맞춰볼까? 📅"
                )

            if rel == "썸/연애":
                suggestions.append(
                    "너 힘든 얘기 해줘서 고마워. 네 얘기 오래 들어주고 싶어. 부담 안 되는 선에서만 말해줘 💜"
                )
            elif rel == "선배/후배" or rel == "선생님/멘토":
                suggestions.append(
                    "항상 응원하고 있어요! 혹시 도움이 필요하면 언제든 편하게 말씀해 주세요 🙂"
                )

            if not suggestions:
                suggestions.append(
                    "그랬구나..! 네 얘기 들어보니까 그냥 넘길 일이 아닌 것 같아. 괜찮다면 조금만 더 말해줄래? 🌱"
                )

            for i, msg in enumerate(suggestions, start=1):
                st.info(f"추천 답변 {i}\n\n{msg}")

            st.caption("※ 실제 서비스에서는 감정 분석·맥락 분석 모델을 사용해 더 정교한 답변을 추천합니다.")


# ---------------- 패션 & 퍼스널 컬러 ----------------
elif page == "패션 & 퍼스널 컬러 👗":
    st.markdown("## 패션 & 퍼스널 컬러 코디 추천 👗")
    st.write("퍼스널 컬러와 오늘 기분에 맞는 코디 아이디어를 제안합니다.")
    line()

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
            "오늘 입을 수 있는 옷 아이템을 선택해 주세요 👕",
            ["후드티", "셔츠", "블라우스", "니트", "청바지", "슬랙스", "스커트", "원피스", "운동화", "로퍼", "부츠"],
        )
        acc = st.multiselect(
            "오늘 쓸 수 있는 액세서리 💍",
            ["모자", "목걸이", "귀걸이", "시계", "가방", "헤어핀"],
        )

    if st.button("👗 코디 추천 받기"):
        st.markdown("### ✨ 오늘의 BAME 코디 제안")

        base_msg = ""
        if personal_color == "봄 웜":
            base_msg = "봄 웜톤에는 크림, 코랄, 라이트 베이지 계열이 잘 어울려요."
        elif personal_color == "여름 쿨":
            base_msg = "여름 쿨톤에는 라벤더, 소라색, 쿨핑크 같은 부드러운 쿨톤을 추천해요."
        elif personal_color == "가을 웜":
            base_msg = "가을 웜톤에는 브라운, 카멜, 카키, 버건디 계열이 잘 어울려요."
        elif personal_color == "겨울 쿨":
            base_msg = "겨울 쿨톤에는 블랙·화이트, 선명한 레드/블루처럼 대비 강한 색이 찰떡이에요."
        else:
            base_msg = "퍼스널 컬러를 모르겠다면 화이트 + 포인트 컬러 하나 조합이 가장 안전해요."

        st.write("- " + base_msg)

        if style_mood == "귀엽게 💕":
            st.write("- 귀여운 느낌을 위해 루즈핏 상의 + 밝은 색 하의를 추천해요.")
        elif style_mood == "시크하게 🖤":
            st.write("- 시크한 날엔 올블랙 또는 블랙+그레이 조합이 잘 어울려요.")
        elif style_mood == "공부하러 가는 날 📚":
            st.write("- 공부하는 날엔 편한 상의 + 넉넉한 바지 + 운동화 조합이 좋아요.")
        elif style_mood == "사진 많이 찍는 날 📸":
            st.write("- 사진 많이 찍는 날엔 대비되는 색 하나를 꼭 넣어서 사진에서 눈에 띄게 해 보세요.")
        else:
            st.write("- 편하게 입고 싶은 날엔 후드티나 니트 + 편한 바지가 마음도 편해요.")

        if items:
            st.write(f"- 오늘 선택한 아이템 중에서는 {', '.join(items)} 를 중심으로 코디를 짜보는 걸 추천해요.")
        if acc:
            st.write(f"- 액세서리는 {', '.join(acc)} 정도만 포인트로 주면 과하지 않게 예뻐요 ✨")

        st.caption("※ 실제 서비스에서는 옷장 사진과 퍼스널 컬러 분석 모델을 활용해 더 정교한 추천을 제공합니다.")


# ---------------- SNS 브랜딩 ----------------
elif page == "SNS 브랜딩 📸":
    st.markdown("## SNS 브랜딩 & 피드 추천 📸")
    st.write("올릴 사진과 메시지에 맞는 필터, 폰트, 음악, 문구 스타일을 추천합니다.")
    line()

    msg = st.text_area(
        "사진에 담고 싶은 메시지/분위기를 적어 주세요 🌈",
        placeholder="예) 오늘 너무 뿌듯한 하루였어! 작은 성취들도 기록해두고 싶다.",
    )

    vibe = st.selectbox(
        "계정 전체 분위기는 어떤 느낌인가요?",
        ["꾸안꾸 데일리", "공부/기록 계정", "갬성 사진 위주", "친구들이랑 노는 계정", "아직 잘 모르겠음"],
    )

    if st.button("📸 브랜딩 추천 받기"):
        if not msg.strip():
            st.warning("메시지를 간단히라도 적어 주세요! ✏️")
        else:
            st.markdown("### ✨ 추천 브랜딩 요소")

            lower_msg = msg.lower()

            if "공부" in msg or "기록" in msg or "노트" in msg:
                filter_rec = "화이트 톤을 살린 깔끔한 필터"
                font_rec = "또박또박한 얇은 글씨체"
                music_rec = "잔잔한 lofi / 공부 브금"
            elif "밤" in msg or "야경" in msg or "별" in msg:
                filter_rec = "어두운 배경에 네온/보라빛이 도는 필터"
                font_rec = "네온사인 느낌의 얇은 폰트"
                music_rec = "몽환적인 R&B 나 시티팝"
            elif "친구" in msg or "추억" in msg or "웃겼" in msg:
                filter_rec = "따뜻한 필름 카메라 느낌 필터"
                font_rec = "라운드형 캐주얼 폰트"
                music_rec = "밝은 팝송이나 K-POP"
            else:
                filter_rec = "피부톤과 배경만 살짝 밝히는 자연광 느낌 필터"
                font_rec = "깔끔한 산세리프 폰트"
                music_rec = "사진 분위기에 맞는 잔잔한 BGM"

            sticker_rec = "하트, 별, 체크리스트 스티커를 사진 구석에 살짝만 사용하는 것을 추천해요."
            caption_tip = "첫 줄에는 짧은 한 문장, 아래에는 구체적인 이야기와 해시태그를 적어 보세요."

            if vibe == "갬성 사진 위주":
                caption_tip = "이모지와 해시태그는 최소로, 여백이 느껴지는 짧은 문장 위주로 적어 보세요."
            elif vibe == "친구들이랑 노는 계정":
                sticker_rec = "움짤 느낌 스티커, 말풍선 스티커를 섞어 장난스럽게 연출해 보세요."

            st.write(f"- 추천 필터: {filter_rec}")
            st.write(f"- 추천 폰트 스타일: {font_rec}")
            st.write(f"- 추천 음악/사운드: {music_rec}")
            st.write(f"- 스티커 사용 팁: {sticker_rec}")
            st.write(f"- 캡션 작성 팁: {caption_tip}")

            st.caption("※ 실제 서비스에서는 이미지 인식과 계정 분석을 통해 더 정교한 브랜딩 가이드를 제공합니다.")


# ---------------- 요즘 밈 설명 ----------------
elif page == "요즘 밈 설명 😂":
    st.markdown("## 요즘 밈 설명서 😂")
    st.write("SNS에서 자주 보이는 밈을 간단하게 설명해 줍니다.")
    line()

    meme = st.selectbox(
        "궁금한 밈을 골라 보세요 (예시)",
        [
            "선택 안 함",
            "어? 왜 안돼요? (당황 밈)",
            "멍 때리다 현실 복귀하는 짤",
            "00학번 갬성 필터",
            "그냥 전체 설명 보기",
        ],
    )

    if meme == "어? 왜 안돼요? (당황 밈)":
        st.markdown("### 🙃 '어? 왜 안돼요?' 밈")
        st.write(
            "갑자기 에러가 나거나 본인이 한 행동이 이해 안 될 때, 귀엽게 당황한 척 하며 쓰는 표현입니다.\n"
            "- 시험 망쳤을 때: '어? 왜 안돼요? 분명 어제까지는 알았는데요…?'\n"
            "- 앱이 터질 때: '어? 왜 안돼요? 방금까지 잘 돌아갔는데요…?'"
        )
    elif meme == "멍 때리다 현실 복귀하는 짤":
        st.markdown("### 😵‍💫 멍 때리다 현실 복귀하는 밈")
        st.write(
            "아무 생각 없이 멍 하다가 갑자기 현실로 돌아올 때 쓰는 짤입니다.\n"
            "예: 면학 시간에 멍 때리다 갑자기 선생님이 부를 때 등."
        )
    elif meme == "00학번 갬성 필터":
        st.markdown("### 📼 '00학번 갬성' 필터")
        st.write(
            "옛날 디카/필카 느낌을 내는 필터를 말할 때 쓰는 표현입니다.\n"
            "노이즈, 약간 누렇게 뜬 색감, 시간 지난 느낌이 특징입니다."
        )
    else:
        st.markdown("### 📚 밈 설명 기능 소개")
        st.write(
            "실제 서비스에서는 밈의 출처, 쓰는 상황, 예시 문장을 정리해서 보여주고\n"
            "사용자의 계정 분위기에 맞게 어느 정도까지 써도 괜찮을지 가이드를 줄 수 있습니다."
        )


# ---------------- 오늘의 밤티 점수 ----------------
elif page == "오늘의 밤티 점수 🔮":
    st.markdown("## 오늘의 밤티 점수 분석 🔮")
    st.write("오늘의 나를 밤티 점수로 체크해 보고 간단한 피드백을 받아보는 페이지입니다.")
    line()

    st.write("각 항목을 오늘 기분대로 선택해 보세요. (1 = 전혀 아니다, 5 = 매우 그렇다)")

    q1 = st.slider("오늘 나는 사람들과 대화할 준비가 되어 있다 😄", 1, 5, 3)
    q2 = st.slider("오늘의 옷차림에 나름 만족한다 👗", 1, 5, 3)
    q3 = st.slider("오늘은 SNS에 뭐라도 올리고 싶은 마음이 있다 📸", 1, 5, 3)
    q4 = st.slider("오늘 멘탈은 비교적 안정적이다 🧠", 1, 5, 3)
    q5 = st.slider("새로운 걸 시도해보고 싶은 도전 정신이 있다 🚀", 1, 5, 3)

    if st.button("🔮 오늘의 밤티 점수 보기"):
        raw_score = q1 + q2 + q3 + q4 + q5
        max_score = 25
        score = int(raw_score / max_score * 100)

        st.markdown("### ✨ 오늘의 밤티 종합 점수")
        st.metric("오늘의 BAME 밤티 점수", f"{score} / 100")
        st.progress(score / 100)

        if score >= 80:
            msg = "오늘 밤티 점수 최상위 💜 무엇을 해도 잘 풀릴 기세예요."
        elif score >= 60:
            msg = "오늘 꽤 괜찮은 상태예요 🙂 약간의 휴식만 챙기면 부드럽게 흘러갈 거예요."
        elif score >= 40:
            msg = "조금 피곤하거나 예민할 수 있는 날이에요. 오늘은 가볍게 기록만 남겨도 좋아요 🌱"
        else:
            msg = "지금은 쉬어야 하는 타이밍일 수도 있어요. 낮은 점수도 괜찮아요. 충전의 시간입니다 ☁️"

        st.info(msg)
        st.caption("※ 실제 서비스에서는 장기 데이터를 함께 고려해 더 정교한 분석을 제공할 수 있습니다.")
