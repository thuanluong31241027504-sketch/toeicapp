# Dữ liệu câu hỏi bổ sung - Có thể thêm bất kỳ lúc nào
QUESTIONS = [
    {
        'id': 101,
        'part': 'Part 5',
        'section': 'Incomplete Sentences',
        'question': 'The new policy will _____ affect all employees.',
        'options': ['direct', 'directly', 'directed', 'directing'],
        'correct': 1,
        'explanation': 'Dùng trạng từ để bổ nghĩa cho động từ.'
    },
    {
        'id': 102,
        'part': 'Part 5',
        'section': 'Incomplete Sentences',
        'question': 'We need to _____ this issue immediately.',
        'options': ['address', 'addresses', 'addressed', 'addressing'],
        'correct': 0,
        'explanation': 'Dùng động từ nguyên thể sau "to".'
    }
]

QUESTIONS_INFO = {
    'name': 'TOEIC Reading Practice Set 2',
    'description': 'Bộ câu hỏi bổ sung cho phần Reading TOEIC',
    'total_questions': len(QUESTIONS),
    'difficulty': 'Advanced'
}
