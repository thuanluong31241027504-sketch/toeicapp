# Cấu hình toàn ứng dụng
TOEIC_CONFIG = {
    'total_questions': 100,  # Tổng số câu TOEIC Reading
    'passing_score': 300,    # Điểm đạt
    'max_score': 495,        # Điểm tối đa TOEIC Reading
    'min_score': 5,          # Điểm tối thiểu
    'score_per_question': 4.95,  # Mỗi câu đúng được bao nhiêu điểm
}

# Cấu hình hiển thị
UI_CONFIG = {
    'app_title': 'TOEIC Reading Practice & Assessment',
    'app_icon': '📚',
    'primary_color': '#FF4B4B',
    'secondary_color': '#0066CC'
}

# Các phần của bài thi TOEIC Reading
SECTIONS = {
    'Part 5': {'name': 'Incomplete Sentences', 'questions': 30, 'start': 0},
    'Part 6': {'name': 'Text Completion', 'questions': 16, 'start': 30},
    'Part 7': {'name': 'Reading Comprehension', 'questions': 54, 'start': 46}
}
