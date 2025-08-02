import streamlit as st
import openai
import os
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="😄 한글 단어 유머 해석기",
    page_icon="😄",
    layout="wide"
)

# CSS 스타일링
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #FF6B6B;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    .word-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    .interpretation-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .fun-fact {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        font-style: italic;
    }
</style>
""", unsafe_allow_html=True)

# 제목
st.markdown('<h1 class="main-header">😄 한글 단어 유머 해석기</h1>', unsafe_allow_html=True)

# OpenAI API 키 설정
st.sidebar.header("🔑 API 설정")
api_key = st.sidebar.text_input("OpenAI API 키", type="password", help="OpenAI API 키를 입력하세요")

# 환경변수로도 설정 가능
if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    openai.api_key = api_key
    
    # 사이드바 설정
    st.sidebar.header("⚙️ 해석 설정")
    
    humor_level = st.sidebar.selectbox(
        "유머 수준",
        ["약간 유머러스", "매우 유머러스", "완전 개그", "창의적 해석"],
        help="해석의 유머 수준을 선택하세요"
    )
    
    interpretation_style = st.sidebar.selectbox(
        "해석 스타일",
        ["일상적 관점", "창의적 상상", "역사적 관점", "현대적 해석", "비유적 설명"],
        help="어떤 스타일로 해석할지 선택하세요"
    )
    
    # 메인 컨텐츠
    st.header("📝 단어 입력")
    
    # 단어 입력
    word_input = st.text_input(
        "해석할 한글 단어를 입력하세요",
        placeholder="예: 사과, 컴퓨터, 바람, 꿈...",
        help="한글 단어를 입력하면 유머러스하게 해석해드립니다!"
    )
    
    if word_input:
        st.markdown(f'<div class="word-card"><h2>🎯 입력된 단어: <strong>{word_input}</strong></h2></div>', unsafe_allow_html=True)
        
        # 해석 버튼
        if st.button("😄 유머러스하게 해석하기", type="primary"):
            with st.spinner("🤔 단어를 재미있게 해석하고 있습니다..."):
                try:
                    # 프롬프트 구성
                    prompt = f"""
다음 한글 단어를 {humor_level}하고 {interpretation_style}으로 해석해주세요.

단어: {word_input}

다음 형식으로 답변해주세요:
1. 재미있는 해석: (창의적이고 유머러스한 해석)
2. 일상적 관점: (실생활에서 어떻게 보는지)
3. 창의적 상상: (완전히 다른 관점에서의 해석)
4. 재미있는 팁: (이 단어와 관련된 재미있는 사실이나 조언)

답변은 친근하고 재미있게, 이모지를 적절히 사용해서 작성해주세요.
"""
                    
                    # OpenAI API 호출
                    response = openai.ChatCompletion.create(
                        model="gpt-4o-mini",
                        messages=[
                            {"role": "system", "content": "당신은 한글 단어를 재미있고 창의적으로 해석하는 전문가입니다. 항상 유머러스하고 친근한 톤으로 답변하세요."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=500,
                        temperature=0.8
                    )
                    
                    interpretation = response.choices[0].message.content
                    
                    # 결과 표시
                    st.markdown('<div class="interpretation-card">', unsafe_allow_html=True)
                    st.markdown("### 🎭 유머러스한 해석 결과")
                    st.write(interpretation)
                    st.markdown('</div>', unsafe_allow_html=True)
                    
                    # 해석 히스토리 저장
                    if 'interpretation_history' not in st.session_state:
                        st.session_state.interpretation_history = []
                    
                    history_item = {
                        'word': word_input,
                        'interpretation': interpretation,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'humor_level': humor_level,
                        'style': interpretation_style
                    }
                    st.session_state.interpretation_history.append(history_item)
                    
                except Exception as e:
                    st.error(f"해석 중 오류가 발생했습니다: {e}")
                    st.info("API 키가 올바른지 확인해주세요.")
    
    # 히스토리 표시
    if 'interpretation_history' in st.session_state and st.session_state.interpretation_history:
        st.header("📚 해석 히스토리")
        
        # 최근 5개만 표시
        recent_history = st.session_state.interpretation_history[-5:]
        
        for idx, item in enumerate(reversed(recent_history)):
            with st.expander(f"📝 {item['word']} - {item['timestamp']}"):
                st.write(f"**단어:** {item['word']}")
                st.write(f"**유머 수준:** {item['humor_level']}")
                st.write(f"**해석 스타일:** {item['style']}")
                st.write("**해석 결과:**")
                st.write(item['interpretation'])
        
        # 히스토리 초기화 버튼
        if st.button("🗑️ 히스토리 초기화"):
            st.session_state.interpretation_history = []
            st.success("히스토리가 초기화되었습니다!")
            st.rerun()
    
    # 재미있는 팁
    st.header("💡 재미있는 팁")
    st.markdown("""
    <div class="fun-fact">
    <h4>🎯 이 앱의 특징:</h4>
    <ul>
    <li>🤖 GPT-3.5-turbo를 사용한 창의적 해석</li>
    <li>😄 다양한 유머 수준과 해석 스타일 선택 가능</li>
    <li>📚 해석 히스토리 저장 및 관리</li>
    <li>🎨 아름다운 UI/UX 디자인</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # 예시 단어들
    st.header("🎲 재미있는 예시 단어들")
    example_words = ["사과", "바람", "꿈", "컴퓨터", "바다", "책", "음악", "친구", "시간", "미소"]
    
    cols = st.columns(5)
    for idx, word in enumerate(example_words):
        col_idx = idx % 5
        with cols[col_idx]:
            if st.button(word, key=f"example_{idx}"):
                st.session_state.word_input = word
                st.rerun()

else:
    st.error("⚠️ OpenAI API 키를 입력해주세요!")
    st.info("""
    ### 🔑 API 키 설정 방법:
    1. OpenAI 웹사이트에서 API 키를 발급받으세요
    2. 사이드바에 API 키를 입력하세요
    3. 또는 환경변수 OPENAI_API_KEY로 설정하세요
    """)

# 푸터
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>😄 한글 단어 유머 해석기 | OpenAI GPT-3.5-turbo 기반</p>
</div>
""", unsafe_allow_html=True) 