import importlib
import sys
from pathlib import Path

# Thêm đường dẫn data vào sys.path để import linh hoạt
data_path = Path(__file__).parent.parent / 'data'
if str(data_path) not in sys.path:
    sys.path.insert(0, str(data_path))

def load_questions(module_name='questions'):
    """
    Tải dữ liệu câu hỏi từ module chỉ định
    
    Args:
        module_name (str): Tên module chứa dữ liệu câu hỏi
    
    Returns:
        list: Danh sách câu hỏi
    """
    try:
        # Import module động
        module = importlib.import_module(f'data.{module_name}')
        questions = getattr(module, 'QUESTIONS', [])
        return questions
    except (ImportError, AttributeError):
        # Nếu không tìm thấy module, thử load trực tiếp
        try:
            # Thử import từ thư mục data
            import importlib.util
            file_path = Path(__file__).parent.parent / 'data' / f'{module_name}.py'
            if file_path.exists():
                spec = importlib.util.spec_from_file_location(module_name, file_path)
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                return getattr(module, 'QUESTIONS', [])
        except Exception:
            pass
        return []

def get_available_question_sets():
    """
    Lấy danh sách các bộ câu hỏi có sẵn
    
    Returns:
        list: Danh sách tên các bộ câu hỏi
    """
    data_dir = Path(__file__).parent.parent / 'data'
    question_files = []
    
    if data_dir.exists():
        for file in data_dir.glob('*.py'):
            if file.stem != '__init__':
                question_files.append(file.stem)
    
    return question_files

def merge_questions(question_sets):
    """
    Ghép nhiều bộ câu hỏi lại với nhau
    
    Args:
        question_sets (list): Danh sách tên các bộ câu hỏi
    
    Returns:
        list: Danh sách câu hỏi đã ghép
    """
    all_questions = []
    for set_name in question_sets:
        questions = load_questions(set_name)
        all_questions.extend(questions)
    
    return all_questions
