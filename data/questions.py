# Dữ liệu câu hỏi mẫu - Có thể mở rộng thêm
QUESTIONS = [
    {
        'id': 1,
        'part': 'Part 5',
        'section': 'Incomplete Sentences',
        'question': 'The company _____ a new marketing strategy next month.',
        'options': ['implement', 'implements', 'will implement', 'implemented'],
        'correct': 2,  # Index bắt đầu từ 0
        'explanation': 'Dùng thì tương lai đơn cho hành động sẽ xảy ra trong tương lai.'
    },
    {
        'id': 2,
        'part': 'Part 5',
        'section': 'Incomplete Sentences',
        'question': 'She is _____ than her sister.',
        'options': ['tall', 'taller', 'tallest', 'more tall'],
        'correct': 1,
        'explanation': 'Dùng so sánh hơn với tính từ ngắn.'
    },
    {
        'id': 3,
        'part': 'Part 5',
        'section': 'Incomplete Sentences',
        'question': 'The meeting was _____ because of the bad weather.',
        'options': ['cancel', 'canceling', 'canceled', 'cancels'],
        'correct': 2,
        'explanation': 'Dùng thì quá khứ đơn vì sự việc đã xảy ra.'
    },
    {
        'id': 4,
        'part': 'Part 6',
        'section': 'Text Completion',
        'question': 'Dear customers, We are pleased to _____ you about our new service.',
        'options': ['inform', 'informs', 'informed', 'informing'],
        'correct': 0,
        'explanation': 'Dùng động từ nguyên thể sau "to".'
    },
    {
        'id': 5,
        'part': 'Part 6',
        'section': 'Text Completion',
        'question': 'Please _____ your payment by the end of the month.',
        'options': ['make', 'makes', 'made', 'making'],
        'correct': 0,
        'explanation': 'Dùng động từ nguyên thể trong câu mệnh lệnh.'
    },
    {
        'id': 6,
        'part': 'Part 7',
        'section': 'Reading Comprehension',
        'question': 'What is the main purpose of the passage?',
        'options': ['To advertise', 'To inform', 'To persuade', 'To entertain'],
        'correct': 1,
        'explanation': 'Đoạn văn cung cấp thông tin về sản phẩm mới.'
    },
    {
        'id': 7,
        'part': 'Part 7',
        'section': 'Reading Comprehension',
        'question': 'According to the passage, the product is suitable for:',
        'options': ['Children', 'Adults', 'Elderly', 'All ages'],
        'correct': 3,
        'explanation': 'Sản phẩm phù hợp với mọi lứa tuổi.'
    },
    {
        'id': 8,
        'part': 'Part 7',
        'section': 'Reading Comprehension',
        'question': 'When was the product first introduced?',
        'options': ['2020', '2021', '2022', '2023'],
        'correct': 2,
        'explanation': 'Sản phẩm được giới thiệu vào năm 2022.'
    }
]

# Thông tin về bộ câu hỏi
QUESTIONS_INFO = {
    'name': 'TOEIC Reading Practice Set 1',
    'description': 'Bộ câu hỏi mẫu cho phần Reading TOEIC',
    'total_questions': len(QUESTIONS),
    'difficulty': 'Intermediate'
}
