import streamlit as st
import pandas as pd
from config import TOEIC_CONFIG, UI_CONFIG, SECTIONS
from utils.scoring import calculate_toeic_reading_score, get_section_scores
from utils.data_loader import load_questions, get_available_question_sets, merge_questions

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
    }
    .score-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
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
</style>
""", unsafe_allow_html=True)

# Khởi tạo session state
if 'current_questions' not in st.session_state:
    # Load mặc định từ file questions
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
    st.image("https://img.icons8.com/color/96/000000/toeic.png", width=80)
    st.title("📚 TOEIC Reading")
    
    # Phần chọn bộ câu hỏi
    st.subheader("📖 Select Question Set")
    available_sets = get_available_question_sets()
    
    if available_sets:
        default_index = [available_sets.index('questions')] if 'questions' in available_sets else [0]
        selected_sets = st.multiselect(
            "Choose question sets:",
            available_sets,
            default=default_index if 'questions' in st.session_state.question_sets else None
        )
        
        if selected_sets and selected_sets != st.session_state.question_sets:
            load_question_set(selected_sets)
    
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
    if st.session_state.submitted:
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
    st.warning("No questions available. Please check your data files.")
else:
    # Nhóm câu hỏi theo phần
    questions_by_part = {}
    for q in st.session_state.current_questions:
        part = q.get('part', 'Unknown')
        if part not in questions_by_part:
            questions_by_part[part] = []
        questions_by_part[part].append(q)
    
    # Tạo tabs cho từng phần
    tabs = st.tabs(list(questions_by_part.keys()))
    
    for i, (part, questions) in enumerate(questions_by_part.items()):
        with tabs[i]:
            st.write(f"### {part} - {SECTIONS.get(part, {}).get('name', '')}")
            
            for q in questions:
                with st.container():
                    col1, col2 = st.columns([0.9, 0.1])
                    with col1:
                        st.write(f"**{q['id']}. {q['question']}**")
                    
                    # Hiển thị options
                    options = q['options']
                    user_ans = get_user_answer(q['id'])
                    
                    # Tạo radio buttons cho mỗi câu hỏi
                    selected = st.radio(
                        "Choose your answer:",
                        options,
                        key=f"q_{q['id']}",
                        index=options.index(user_ans) if user_ans in options else None,
                        horizontal=True
                    )
                    
                    # Lưu câu trả lời
                    if selected:
                        selected_index = options.index(selected)
                        st.session_state.user_answers[str(q['id'])] = selected_index
                    
                    # Nếu đã submit, hiển thị kết quả
                    if st.session_state.submitted:
                        correct = q['correct']
                        is_correct = selected_index == correct if selected_index is not None else False
                        
                        if selected_index is not None:
                            if is_correct:
                                st.success("✅ Correct!")
                            else:
                                st.error(f"❌ Incorrect. Correct answer: {options[correct]}")
                                if 'explanation' in q:
                                    st.info(f"💡 Explanation: {q['explanation']}")
                        else:
                            st.warning("⚠️ Not answered")
                    
                    st.markdown("---")

# Nút Submit và xem kết quả
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    if not st.session_state.submitted:
        if st.button("📊 Submit & Get Score", use_container_width=True, type="primary"):
            st.session_state.submitted = True
            st.rerun()
    else:
        if st.button("📝 Review Answers", use_container_width=True):
            st.session_state.submitted = False
            st.rerun()

# Hiển thị kết quả chi tiết
if st.session_state.submitted:
    st.markdown("---")
    st.subheader("📊 Your Results")
    
    # Tính toán kết quả
    total_correct = 0
    total_attempted = 0
    correct_by_section = {}
    attempted_by_section = {}
    
    for q in st.session_state.current_questions:
        part = q.get('part', 'Unknown')
        user_ans = st.session_state.user_answers.get(str(q['id']))
        
        if user_ans is not None:
            total_attempted += 1
            attempted_by_section[part] = attempted_by_section.get(part, 0) + 1
            
            if user_ans == q['correct']:
                total_correct += 1
                correct_by_section[part] = correct_by_section.get(part, 0) + 1
    
    # Tính điểm tổng
    result = calculate_toeic_reading_score(total_correct, total_attempted)
    
    # Hiển thị kết quả tổng
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class='score-card'>
            <h3>Score</h3>
            <h1>{result['score']}</h1>
            <p>/ 495</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class='score-card'>
            <h3>Correct</h3>
            <h1>{total_correct}/{total_attempted}</h1>
            <p>{result['correct_percentage']}%</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class='score-card'>
            <h3>Band Level</h3>
            <h2>{result['band_level']}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        status_class = 'status-pass' if result['status'] == 'Pass' else 'status-fail'
        st.markdown(f"""
        <div class='score-card'>
            <h3>Status</h3>
            <h1 class='{status_class}'>{result['status']}</h1>
        </div>
        """, unsafe_allow_html=True)
    
    # Phân tích theo phần
    st.subheader("📈 Performance by Section")
    section_scores = get_section_scores(correct_by_section, attempted_by_section)
    
    # Tạo dataframe cho từng phần
    section_data = []
    for section, data in section_scores.items():
        section_data.append({
            'Section': section,
            'Correct': data['correct'],
            'Attempted': data['attempted'],
            'Accuracy': f"{data['percentage']}%",
            'Status': data['status']
        })
    
    if section_data:
        df = pd.DataFrame(section_data)
        st.dataframe(df, use_container_width=True)
    
    # Lời khuyên
    st.subheader("💡 Recommendations")
    if result['score'] >= 400:
        st.success("🌟 Excellent! You have a strong command of English reading. Keep practicing to maintain your level.")
    elif result['score'] >= 300:
        st.info("📈 Good job! You have a solid foundation. Focus on your weaker sections to improve.")
    elif result['score'] >= 200:
        st.warning("📚 Keep practicing! Work on building vocabulary and reading comprehension skills.")
    else:
        st.error("💪 Don't give up! Start with basic reading materials and practice regularly.")
    
    # Đề xuất bài tập
    st.subheader("📚 Suggested Practice")
    weak_sections = [s for s, d in section_scores.items() if d['percentage'] < 70]
    if weak_sections:
        st.write(f"Focus on improving: **{', '.join(weak_sections)}**")
        st.write("Try more practice questions in these sections to improve your score.")

# Footer
st.markdown("---")
st.caption("💡 Tip: You can add more question files in the 'data' folder. The app will automatically detect them.")
