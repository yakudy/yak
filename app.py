import streamlit as st
import datetime
import html
import base64

st.set_page_config(
    page_title="마음을 담은 감성 편지지 💌",
    page_icon="💌",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Google Fonts import */
    @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Nanum+Myeongjo:wght@400;700&family=Nanum+Pen+Script&family=Sunflower:wght@300;500&family=Noto+Sans+KR:wght@300;400;700&display=swap');

    /* Sidebar Customization */
    .css-1d3t15x {
        background-color: #f8f9fa;
    }
    
    /* Global Styles */
    .stTextArea textarea {
        font-family: 'Noto Sans KR', sans-serif;
        font-size: 15px;
        line-height: 1.6;
        border-radius: 10px;
    }

    /* Print styling rules */
    @media print {
        body * {
            visibility: hidden;
        }
        #printable-letter, #printable-letter * {
            visibility: visible;
        }
        #printable-letter {
            position: absolute;
            left: 0;
            top: 0;
            width: 100%;
        }
    }
</style>
""", unsafe_allow_html=True)

SAMPLE_TEMPLATES = {
    "직접 작성": {
        "recipient": "소중한 당신에게",
        "content": "여기에 따뜻한 마음을 담은 편지 내용을 입력해 보세요...",
        "sender": "당신의 친구"
    },
    "🎉 생일 축하": {
        "recipient": "사랑하는 OO이에게",
        "content": "태어나줘서 고마운 OO아!\n\n오늘 너의 특별한 생일을 진심으로 축하해. 올 한 해 네가 바라는 모든 일들이 이루어지고, 늘 웃음과 행복이 가득하길 바랄게.\n\n맛있는 것 많이 먹고 세상에서 가장 행복한 하루 보내!\n언제나 네 편이야.",
        "sender": "늘 응원하는 00이가"
    },
    "💐 감사 편지": {
        "recipient": "존경하는 선생님께",
        "content": "선생님, 그동안 보내주신 따뜻한 가르침과 배려에 진심으로 감사드립니다.\n\n선생님의 따뜻한 한마디와 격려 덕분에 많은 용기와 힘을 얻을 수 있었습니다. 늘 건강하시고 행복한 일들만 가득하시길 기원합니다.\n\n조만간 꼭 직접 찾아뵙고 인사드리겠습니다.",
        "sender": "올림"
    },
    "☕ 안부 편지": {
        "recipient": "보고 싶은 친구에게",
        "content": "잘 지내고 있지?\n\n바쁜 일상 속에서 문득 네 생각이 나서 이렇게 편지를 남겨.\n요즘 날씨도 많이 변했는데 건강 잘 챙기고 있는지 궁금하다.\n\n시간 날 때 언제 한번 얼굴 보고 소소하게 차 한잔하자.\n항상 건강하고 좋은 하루 보내!",
        "sender": "너를 생각하며"
    },
    "❤️ 사랑의 편지": {
        "recipient": "내 소중한 사람에게",
        "content": "함께하는 매 순간이 소중하고 감사한 너에게.\n\n너와 함께 길을 걷고, 이야기를 나누고, 같은 곳을 바라볼 수 있어서 하루하루가 참 특별해.\n네 곁에서 언제나 든든한 버팀목이 되어줄게.\n\n오늘도 많이 고맙고, 사랑해.",
        "sender": "영원한 너의 짝꿍이"
    }
}

THEME_STYLES = {
    "✨ 앤틱 빈티지 (Classic Antique)": {
        "bg_color": "#fbf2e3",
        "border": "3px double #8c6d46",
        "font_color": "#3e2723",
        "line_color": "#d7ccc8",
        "header_color": "#5d4037",
        "seal_color": "#8d6e63",
        "paper_shadow": "0 8px 20px rgba(89, 60, 31, 0.15)"
    },
    "🌸 파스텔 로맨틱 (Pastel Pink)": {
        "bg_color": "#fff5f7",
        "border": "2px dashed #f48fb1",
        "font_color": "#4a148c",
        "line_color": "#f8bbd0",
        "header_color": "#c2185b",
        "seal_color": "#f48fb1",
        "paper_shadow": "0 8px 20px rgba(233, 30, 99, 0.12)"
    },
    "🌿 숲속 은은함 (Forest Sage)": {
        "bg_color": "#f1f8f5",
        "border": "2px solid #a5d6a7",
        "font_color": "#1b5e20",
        "line_color": "#c8e6c9",
        "header_color": "#2e7d32",
        "seal_color": "#81c784",
        "paper_shadow": "0 8px 20px rgba(46, 125, 50, 0.12)"
    },
    "🌙 미드나잇 모던 (Midnight Blue)": {
        "bg_color": "#1e2430",
        "border": "1px solid #3f4b61",
        "font_color": "#e2e8f0",
        "line_color": "#2d3748",
        "header_color": "#90cdf4",
        "seal_color": "#4a5568",
        "paper_shadow": "0 8px 25px rgba(0, 0, 0, 0.4)"
    },
    "📑 깔끔 모던 (Minimal White)": {
        "bg_color": "#ffffff",
        "border": "1px solid #e2e8f0",
        "font_color": "#2d3748",
        "line_color": "#edf2f7",
        "header_color": "#1a202c",
        "seal_color": "#cbd5e0",
        "paper_shadow": "0 6px 18px rgba(0, 0, 0, 0.08)"
    }
}

FONT_OPTIONS = {
    "나눔명조 (격식있는 명조체)": "'Nanum Myeongjo', serif",
    "고운바탕 (따뜻한 바탕체)": "'Gowun Batang', serif",
    "나눔손글씨 (친근한 손글씨)": "'Nanum Pen Script', cursive",
    "해바라기 (귀여운 정갈함)": "'Sunflower', sans-serif",
    "노토산스 (깔끔한 고딕)": "'Noto Sans KR', sans-serif"
}

if "recipient" not in st.session_state:
    st.session_state.recipient = "소중한 당신에게"
if "content" not in st.session_state:
    st.session_state.content = "여기에 따뜻한 마음을 담은 편지 내용을 입력해 보세요."
if "sender" not in st.session_state:
    st.session_state.sender = "당신의 마음으로부터"

with st.sidebar:
    st.title("⚙️ 편지지 설정")
    st.write("나만의 특별한 편지를 만들어보세요.")
    
    # Template Selection
    st.subheader("💡 샘플 서식 불러오기")
    selected_sample = st.selectbox(
        "템플릿 선택",
        options=list(SAMPLE_TEMPLATES.keys()),
        index=0
    )
    
    if st.button("템플릿 적용하기", use_container_width=True):
        tmpl = SAMPLE_TEMPLATES[selected_sample]
        st.session_state.recipient = tmpl["recipient"]
        st.session_state.content = tmpl["content"]
        st.session_state.sender = tmpl["sender"]
        st.rerun()

    st.markdown("---")
    
    # Styling Controls
    st.subheader("🎨 디자인 및 테마")
    selected_theme_name = st.selectbox("편지지 디자인 테마", list(THEME_STYLES.keys()))
    theme = THEME_STYLES[selected_theme_name]
    
    selected_font_name = st.selectbox("글꼴 선택", list(FONT_OPTIONS.keys()), index=1)
    font_family = FONT_OPTIONS[selected_font_name]
    
    font_size = st.slider("글자 크기 (px)", min_value=14, max_value=28, value=18)
    line_spacing = st.slider("줄 간격", min_value=1.4, max_value=2.8, value=1.9, step=0.1)
    
    st.markdown("---")
    st.subheader("📮 우표 & 장식")
    stamp_icon = st.selectbox("우표 아이콘 선택", ["💌", "🌹", "🌿", "☕", "🐱", "🌙", "🎂", "🧸", "🕊️", "🎁"], index=0)
    stamp_label = st.text_input("우표 라벨", value="AIR MAIL")
    
    has_lines = st.checkbox("편지지 줄표시 보이기", value=True)
    text_align = st.radio("정렬 방식", ["left", "center", "right"], format_func=lambda x: "왼쪽" if x=="left" else ("중앙" if x=="center" else "오른쪽"))

st.title("💌 감성 웹 편지지 제작기")
st.caption("작성한 편지를 아름다운 디자인으로 실시간 확인하고, 저장 및 인쇄할 수 있습니다.")

col_input, col_preview = st.columns([1, 1.2])

with col_input:
    st.subheader("📝 편지 작성하기")
    
    st.session_state.recipient = st.text_input(
        "받는 사람 (To)",
        value=st.session_state.recipient,
        placeholder="예: 사랑하는 어머니께"
    )
    
    st.session_state.content = st.text_area(
        "편지 내용",
        value=st.session_state.content,
        height=320,
        placeholder="마음을 담아 내용을 써주세요..."
    )
    
    st.session_state.sender = st.text_input(
        "보내는 사람 (From)",
        value=st.session_state.sender,
        placeholder="예: 아들 홍길동 올림"
    )
    
    letter_date = st.date_input("날짜", datetime.date.today())
    formatted_date = letter_date.strftime("%Y년 %m월 %d일")
    
    # Text metrics
    char_count = len(st.session_state.content)
    word_count = len(st.session_state.content.split())
    st.info(f"📊 글자 수: **{char_count}** 자 | 단어 수: **{word_count}** 개")

formatted_content = html.escape(st.session_state.content).replace("\n", "<br>")
bg_lines_style = f"background-image: linear-gradient(transparent {int(font_size*line_spacing - 1)}px, {theme['line_color']} {int(font_size*line_spacing - 1)}px);" if has_lines else ""

letter_html = f"""
<div id="printable-letter" style="
    background-color: {theme['bg_color']};
    border: {theme['border']};
    box-shadow: {theme['paper_shadow']};
    border-radius: 12px;
    padding: 45px 40px;
    color: {theme['font_color']};
    font-family: {font_family};
    position: relative;
    min-height: 520px;
    margin: 10px 0;
    transition: all 0.3s ease;
">
    <!-- Stamp -->
    <div style="
        position: absolute;
        top: 30px;
        right: 35px;
        border: 2px dashed {theme['seal_color']};
        padding: 6px 12px;
        border-radius: 6px;
        text-align: center;
        background: rgba(255, 255, 255, 0.3);
    ">
        <div style="font-size: 26px; line-height: 1;">{stamp_icon}</div>
        <div style="font-size: 10px; color: {theme['header_color']}; font-weight: bold; margin-top: 3px; letter-spacing: 1px;">{stamp_label}</div>
    </div>

    <!-- Date -->
    <div style="font-size: 14px; opacity: 0.8; margin-bottom: 25px; color: {theme['header_color']};">
        📅 {formatted_date}
    </div>

    <!-- Recipient -->
    <div style="
        font-size: {font_size + 4}px;
        font-weight: bold;
        margin-bottom: 25px;
        color: {theme['header_color']};
        border-bottom: 2px solid {theme['line_color']};
        padding-bottom: 8px;
    ">
        To. {html.escape(st.session_state.recipient)}
    </div>

    <!-- Letter Body -->
    <div style="
        font-size: {font_size}px;
        line-height: {line_spacing};
        text-align: {text_align};
        min-height: 240px;
        {bg_lines_style}
        background-size: 100% {font_size * line_spacing}px;
        padding-top: 4px;
        word-break: break-word;
        white-space: pre-wrap;
    ">{formatted_content}</div>

    <!-- Sender -->
    <div style="
        margin-top: 40px;
        text-align: right;
        font-size: {font_size + 2}px;
        font-weight: bold;
        color: {theme['header_color']};
        border-top: 1px dashed {theme['line_color']};
        padding-top: 15px;
    ">
        From. {html.escape(st.session_state.sender)}
    </div>
</div>
"""

with col_preview:
    st.subheader("🖼️ 실시간 편지지 미리보기")
    st.markdown(letter_html, unsafe_allow_html=True)
    
    # Download & Export options
    st.markdown("---")
    st.subheader("💾 편지 저장 및 내보내기")
    
    # Printable Standalone HTML page structure
    full_export_html = f"""<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>편지 - To. {html.escape(st.session_state.recipient)}</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=Nanum+Myeongjo:wght@400;700&family=Nanum+Pen+Script&family=Sunflower:wght@300;500&family=Noto+Sans+KR:wght@300;400;700&display=swap');
        body {{
            background-color: #f4f6f9;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }}
    </style>
</head>
<body>
    <div style="max-width: 650px; width: 100%;">
        {letter_html}
    </div>
</body>
</html>
"""

    btn_col1, btn_col2 = st.columns(2)
    
    with btn_col1:
        st.download_button(
            label="📄 HTML 웹 편지 파일 다운로드",
            data=full_export_html,
            file_name=f"Letter_{st.session_state.recipient}.html",
            mime="text/html",
            use_container_width=True
        )

    with btn_col2:
        # Generate raw plain text copy helper
        plain_text_letter = f"To. {st.session_state.recipient}\n\n{st.session_state.content}\n\nFrom. {st.session_state.sender}\n({formatted_date})"
        st.download_button(
            label="📝 텍스트(.txt) 저장",
            data=plain_text_letter,
            file_name=f"Letter_{st.session_state.recipient}.txt",
            mime="text/plain",
            use_container_width=True
        )

st.markdown("---")
with st.expander("ℹ️ **Streamlit Cloud 배포 가이드 & 사용 팁**"):
    st.markdown("""
    ### 🚀 Streamlit Cloud에 무료로 배포하는 방법
    1. 이 코드를 `app.py`라는 이름으로 GitHub 저장소(Repository)에 업로드합니다.
    2. 저장소 루트에 `requirements.txt` 파일을 추가하고 아래 내용을 적습니다:
       ```text
       streamlit
       ```
    3. [Streamlit Cloud](https://share.streamlit.io/)에 접속하여 GitHub 계정으로 로그인합니다.
    4. **'New app'** 버튼을 누르고 GitHub 저장소와 `app.py`를 선택하여 배포를 완료합니다!

    ### 🖨️ 인쇄 및 PDF 저장 팁
    - 다운로드한 `.html` 파일을 브라우저(Chrome/Edge)에서 연 후 `Ctrl + P` (Mac은 `Cmd + P`)를 눌러 **'PDF로 저장'**을 선택하면 고화질 PDF 편지로 변환됩니다.
    """)
