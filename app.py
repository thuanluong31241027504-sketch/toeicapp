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
    st.error("Loi import module: " + str(e))
    st.stop()

# Cấu hình trang
st.set_page_config(
    page_title=UI_CONFIG['app_title'],
    page_icon=UI_CONFIG['app_icon'],
    layout="wide"
)

# CSS tùy chỉnh
st.markdown(
    '''
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
    </style>
    ''',
    unsafe_allow_html=True
)

# Khởi tạo session state
if 'current_questions' not in st.session_state:
    st.session_state.current_questions = load_questions()
    st.session_state.question_sets = ['questions']

if 'user_answers' not in st.session_state:
    st.session_state.user_answers = {}

if 'submitted' not in st.session_state:
    st.session_state.submitted = False

def reset_app():
    st.session_state.user_answers = {}
    st.session_state.submitted = False
    st.rerun()

def load_question_set(set_names):
    if set_names:
        st.session_state.current_questions = merge_questions(set_names)
        st.session_state.question_sets = set_names
        st.session_state.user_answers = {}
        st.session_state.submitted = False
        st.rerun()

def get_user_answer(question_id):
    return st.session_state.user_answers.get(str(question_id), None)

# Sidebar
with st.sidebar:
    st.title("📚 TOEIC Reading")
    
    st.subheader("📖 Select Question Set")
    available_sets = get_available_question_sets()
    
    if available_sets:
        default_values = []
        if 'questions' in st.session_state.question_sets:
            if 'questions' in available_sets:
                default_values = ['questions']
        elif st.session_state.question_sets:
            default_values = [s for s in st.session_state.question_sets if s in available_sets]
        
        selected_sets = st.multiselect(
            "Choose question sets:",
            available_sets,
            default=default_values if default_values else None
        )
        
        if selected_sets and selected_sets != st.session_state.question_sets:
            load_question_set(selected_sets)
    else:
        st.warning("No question sets found.")
    
    st.subheader("ℹ️ Test Information")
    total_q = len(st.session_state.current_questions)
    st.info("Total Questions: " + str(total_q))
    
    answered = len([a for a in st.session_state.user_answers.values() if a is not None])
    st.info("Answered: " + str(answered) + "/" + str(total_q))
    
    if st.button("🔄 Reset All", use_container_width=True):
        reset_app()
    
    with st.expander("📝 How to Use"):
        st.write("1. Select Question Set from dropdown")
        st.write("2. Answer questions by clicking on options")
        st.write("3. Submit to see results")
        st.write("4. Review your performance")
        st.write("")
        st.write("Scoring System:")
        st.write("- Score based on correct answers ratio")
        st.write("- Band levels: Beginner to Advanced")
        st.write("- Maximum score: 495")

# Main content
st.markdown("<h1 class='main-header'>📚 TOEIC Reading Practice & Assessment</h1>", unsafe_allow_html=True)

# Thông tin
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Questions", len(st.session_state.current_questions))
with col2:
    answered = len([a for a in st.session_state.user_answers.values() if a is not None])
    st.metric("Answered", str(answered) + "/" + str(len(st.session_state.current_questions)))
with col3:
    if st.session_state.submitted and len(st.session_state.current_questions) > 0:
        correct_count = 0
        for q in st.session_state.current_questions:
            user_ans = st.session_state.user_answers.get(str(q['id']))
            if user_ans is not None and user_ans == q['correct']:
                correct_count += 1
        result = calculate_toeic_reading_score(correct_count, answered)
        st.metric("Score", str(result['score']) + "/495")

# Questions
st.markdown("---")
st.subheader("📝 Questions")

if not st.session_state.current_questions:
    st.warning("No questions available. Please check your data files.")
    st.info("How to add questions:")
    st.write("1. Create a new file in the data folder")
    st.write("2. Define a QUESTIONS list with the correct format")
    st.write("3. The app will automatically detect it")
else:
    questions_by_part = {}
    for q in st.session_state.current_questions:
        part = q.get('part', 'Unknown')
        if part not in questions_by_part:
            questions_by_part[part] = []
        questions_by_part[part].append(q)
    
    tab_names = list(questions_by_part.keys())
    if tab_names:
        tabs = st.tabs(tab_names)
        
        for i, (part, questions) in enumerate(questions_by_part.items()):
            with tabs[i]:
                section_name = SECTIONS.get(part, {}).get('name', '')
                if section_name:
                    st.write("### " + part + " - " + section_name)
                else:
                    st.write("### " + part)
                
                for q in questions:
                    with st.container():
                        st.markdown(
                            '<div class="question-container"><p><b>' + 
                            str(q['id']) + '. ' + q['question'] + 
                            '</b></p></div>',
                            unsafe_allow_html=True
                        )
                        
                        options = q['options']
                        user_ans = get_user_answer(q['id'])
                        
                        default_index = None
                        if user_ans is not None and isinstance(user_ans, int) and 0 <= user_ans < len(options):
                            default_index = user_ans
                        
                        selected = st.radio(
                            "Choose your answer:",
                            options,
                            key="q_" + str(q['id']),
                            index=default_index,
                            horizontal=True,
                            label_visibility="collapsed"
                        )
                        
                        if selected:
                            selected_index = options.index(selected)
                            st.session_state.user_answers[str(q['id'])] = selected_index
                        
                        if st.session_state.submitted:
                            correct = q['correct']
                            if selected and selected_index is not None:
                                is_correct = selected_index == correct
                                if is_correct:
                                    st.success("Correct!")
                                else:
                                    st.error("Incorrect. Correct answer: " + options[correct])
                                    if 'explanation' in q:
                                        st.info("Explanation: " + q['explanation'])
                            else:
                                st.warning("Not answered")
                        
                        st.markdown("---")

# Submit button
if len(st.session_state.current_questions) > 0:
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

# Results
if st.session_state.submitted and len(st.session_state.current_questions) > 0:
    st.markdown("---")
    st.subheader("📊 Your Results")
    
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
    
    result = calculate_toeic_reading_score(total_correct, total_attempted)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(
            '<div class="score-card"><h3>Score</h3><h1 style="font-size: 48px;">' + 
            str(result['score']) + 
            '</h1><p>/ 495</p></div>',
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            '<div class="score-card"><h3>Correct</h3><h1 style="font-size: 48px;">' + 
            str(total_correct) + '/' + str(total_attempted) + 
            '</h1><p>' + str(result['correct_percentage']) + '%</p></div>',
            unsafe_allow_html=True
        )
    with col3:
        st.markdown(
            '<div class="score-card"><h3>Band Level</h3><h2 style="font-size: 24px;">' + 
            result['band_level'] + 
            '</h2></div>',
            unsafe_allow_html=True
        )
    with col4:
        status_class = 'status-pass' if result['status'] == 'Pass' else 'status-fail'
        st.markdown(
            '<div class="score-card"><h3>Status</h3><h1 class="' + 
            status_class + '" style="font-size: 40px;">' + 
            result['status'] + 
            '</h1></div>',
            unsafe_allow_html=True
        )
    
    if correct_by_section or attempted_by_section:
        st.subheader("📈 Performance by Section")
        section_scores = get_section_scores(correct_by_section, attempted_by_section)
        
        section_data = []
        for section, data in section_scores.items():
            section_data.append({
                'Section': section,
                'Correct': data['correct'],
                'Attempted': data['attempted'],
                'Accuracy': str(data['percentage']) + '%',
                'Status': data['status']
            })
        
        if section_data:
            df = pd.DataFrame(section_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.subheader("💡 Recommendations")
    score = result['score']
    if score >= 400:
        st.success("Excellent! You have a strong command of English reading.")
        st.balloons()
    elif score >= 300:
        st.info("Good job! You have a solid foundation.")
    elif score >= 200:
        st.warning("Keep practicing! Work on building vocabulary.")
    else:
        st.error("Don't give up! Start with basic reading materials.")
    
    if section_data:
        st.subheader("📚 Suggested Practice")
        weak_sections = [s for s, d in section_scores.items() if d['percentage'] < 70]
        if weak_sections:
            st.write("Focus on improving: " + ', '.join(weak_sections))
        else:
            st.write("You're doing great in all sections!")

# Footer
st.markdown("---")
st.caption("Tip: You can add more question files in the 'data' folder.")

if st.session_state.current_questions:
    st.caption("Loaded: " + str(len(st.session_state.current_questions)) + " questions from " + ', '.join(st.session_state.question_sets))
