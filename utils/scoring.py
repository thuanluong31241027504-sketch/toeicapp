def calculate_toeic_reading_score(correct_count, total_attempted):
    """
    Tính điểm TOEIC Reading dựa trên số câu đúng và số câu đã làm
    
    Args:
        correct_count (int): Số câu trả lời đúng
        total_attempted (int): Tổng số câu đã làm
    
    Returns:
        dict: {
            'score': int,  # Điểm TOEIC Reading
            'correct_percentage': float,  # % đúng
            'attempted_percentage': float,  # % đã làm
            'band_level': str,  # Band level
            'status': str  # Pass/Fail
        }
    """
    if total_attempted == 0:
        return {
            'score': 0,
            'correct_percentage': 0.0,
            'attempted_percentage': 0.0,
            'band_level': 'No attempt',
            'status': 'Not started'
        }
    
    # Tính tỷ lệ phần trăm đúng trên số câu đã làm
    correct_percentage = (correct_count / total_attempted) * 100
    
    # Tính tỷ lệ phần trăm đã làm
    attempted_percentage = (total_attempted / 100) * 100  # 100 là tổng số câu
    
    # Quy đổi điểm TOEIC Reading (công thức tham khảo)
    # Dựa trên tỷ lệ đúng để tính điểm (5-495)
    if correct_percentage >= 90:
        score = 470
        band_level = 'Advanced (C1)'
    elif correct_percentage >= 80:
        score = 420
        band_level = 'High Intermediate (B2)'
    elif correct_percentage >= 70:
        score = 370
        band_level = 'Intermediate (B1)'
    elif correct_percentage >= 60:
        score = 320
        band_level = 'Pre-Intermediate (A2)'
    elif correct_percentage >= 50:
        score = 270
        band_level = 'Elementary (A1)'
    elif correct_percentage >= 30:
        score = 200
        band_level = 'Beginner'
    else:
        score = 100
        band_level = 'Beginner'
    
    # Điều chỉnh điểm dựa trên số câu đã làm
    # Nếu chưa làm hết, giảm điểm một chút
    if attempted_percentage < 50:
        score = max(5, score - 50)
    
    # Xác định trạng thái
    status = 'Pass' if score >= 300 else 'Fail'
    
    return {
        'score': score,
        'correct_percentage': round(correct_percentage, 1),
        'attempted_percentage': round(attempted_percentage, 1),
        'band_level': band_level,
        'status': status
    }

def get_section_scores(correct_by_section, attempted_by_section):
    """
    Tính điểm cho từng phần của bài thi
    
    Args:
        correct_by_section (dict): Số câu đúng theo từng phần
        attempted_by_section (dict): Số câu đã làm theo từng phần
    
    Returns:
        dict: Điểm và tỷ lệ cho từng phần
    """
    section_results = {}
    
    for section, correct in correct_by_section.items():
        attempted = attempted_by_section.get(section, 0)
        
        if attempted > 0:
            percentage = (correct / attempted) * 100
            score = int((percentage / 100) * 100)  # Điểm phần
            status = 'Good' if percentage >= 70 else 'Needs Improvement'
        else:
            percentage = 0.0
            score = 0
            status = 'Not attempted'
        
        section_results[section] = {
            'correct': correct,
            'attempted': attempted,
            'percentage': round(percentage, 1),
            'score': score,
            'status': status
        }
    
    return section_results
