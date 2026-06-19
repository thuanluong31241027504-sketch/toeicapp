import streamlit as st
import pandas as pd
import sys
from pathlib import Path

# Thêm đường dẫn vào sys.path
sys.path.insert(0, str(Path(__file__).parent))

# Import các module
try:
    from config import TOEIC_CONFIG, UI_CONFIG, SECTIONS
    from utils.scoring import calculate_toeic_reading_score, get_section_scores
    from utils.data_loader import load_questions, get_available_question_sets, merge_questions
except ImportError as e:
    st.error(f"Lỗi import module: {e}")
    st.stop()

# Cấu hình trang
st.set_page_config(
    page_title=UI_CONFIG['app_title'],
    page_icon=UI_CONFIG['app_icon'],
    layout="wide"
)

# CSS tùy chỉnh
st.markdown("""
<style>
    .main-header {
        color: #FF4B4B;
        text-align: center;
        padding: 20px;
        font-size: 40px;
    }
    .score-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        text-align: center;
    }
    .band-level {
        font-size: 24px;
        font-weight: bold;
        color: #0066CC;
    }
    .status-pass {
        color: #00CC66;
        font-weight: bold;
    }
    .status-fail {
        color: #FF4B4B;
        font-weight: bold;
    }
    .question-container {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
        border: 1px solid #e0e0e0;
    }
    .stRadio > div {
        flex-direction: row;
        gap: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo session state
if 'current_questions' not in st.session_state:
    st.session_state.current_questions = load_questions()
    st.session_state.question_sets = ['questions']

if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

def reset_app():
    """Reset toàn bộ ứng dụng"""
    st.session_state.user_answers = {}
    st.session_state.submitted = False
    st.rerun()

def load_question_set(set_names):
    """Load bộ câu hỏi được chọn"""
    if set_names:
        st.session_state.current_questions = merge_questions(set_names)
        st.session_state.question_sets = set_names
        st.session_state.user_answers = {}
        st.session_state.submitted = False
        st.rerun()

def get_user_answer(question_id):
    """Lấy câu trả lời của user cho 1 câu hỏi"""
    return st.session_state.user_answers.get(str(question_id), None)

# Sidebar - Điều khiển
with st.sidebar:
    st.title("📚 TOEIC Reading")
    
    # Phần chọn bộ câu hỏi
    st.subheader("📖 Select Question Set")
    available_sets = get_available_question_sets()
    
    if available_sets:
        # Xác định default values
        default_values = []
        if 'questions' in st.session_state.question_sets:
            # Nếu đang dùng bộ 'questions', chọn nó
            if 'questions' in available_sets:
                default_values = ['questions']
        elif st.session_state.question_sets:
            # Nếu đang dùng bộ khác, chọn bộ đó
            default_values = [s for s in st.session_state.question_sets if s in available_sets]
        
        selected_sets = st.multiselect(
            "Choose question sets:",
            available_sets,
            default=default_values if default_values else None
        )
        
        if selected_sets and selected_sets != st.session_state.question_sets:
            load_question_set(selected_sets)
    else:
        st.warning("No question sets found. Please add question files to the 'data' folder.")
    
    # Thông tin bài thi
    st.subheader("ℹ️ Test Information")
    total_q = len(st.session_state.current_questions)
    st.info(f"Total Questions: **{total_q}**")
    
    # Đếm câu đã làm
    answered = len([a for a in st.session_state.user_answers.values() if a is not None])
    st.info(f"Answered: **{answered}/{total_q}**")
    
    # Nút Reset
    if st.button("🔄 Reset All", use_container_width=True):
        reset_app()
    
    # Hướng dẫn
    with st.expander("📝 How to Use"):
        st.markdown("""
        1. **Select Question Set**: Chọn bộ câu hỏi từ dropdown
        2. **Answer Questions**: Chọn đáp án cho từng câu hỏi
        3. **Submit**: Nhấn Submit để xem kết quả
        4. **Review**: Xem điểm và phân tích chi tiết
        
        **Scoring System:**
        - Điểm được tính dựa trên tỷ lệ câu đúng
        - Band điểm từ Beginner đến Advanced
        - Điểm tối đa: 495
        """)

# Main content
st.markdown("<h1 class='main-header'>📚 TOEIC Reading Practice & Assessment</h1>", unsafe_allow_html=True)

# Hiển thị thông tin bộ câu hỏi hiện tại
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Questions", len(st.session_state.current_questions))
with col2:
    answered = len([a for a in st.session_state.user_answers.values() if a is not None])
    st.metric("Answered", f"{answered}/{len(st.session_state.current_questions)}")
with col3:
    if st.session_state.submitted and len(st.session_state.current_questions) > 0:
        # Tính điểm dựa trên câu trả lời
        correct_count = 0
        for q in st.session_state.current_questions:
            user_ans = st.session_state.user_answers.get(str(q['id']))
            if user_ans is not None and user_ans == q['correct']:
                correct_count += 1
        
        result = calculate_toeic_reading_score(correct_count, answered)
        st.metric("Score", f"{result['score']}/495")

# Hiển thị câu hỏi
st.markdown("---")
st.subheader("📝 Questions")

if not st.session_state.current_questions:
    st.warning("⚠️ No questions available. Please check your data files.")
    st.info("""
    **How to add questions:**
    1. Create a new file in the `data` folder
    2. Define a `QUESTIONS` list with the correct format
    3. The app will automatically detect it
    
    **Example format:**
    ```python
    QUESTIONS = [
        {
            'id': 1,
            'part': 'Part 5',
            'section': 'Incomplete Sentences',
            'question': 'Your question here?',
            'options': ['Option A', 'Option B', 'Option C', 'Option D'],
            'correct': 0,  # Index of correct answer (0-based)
            'explanation': 'Explanation for the correct answer'
        }
    ]
