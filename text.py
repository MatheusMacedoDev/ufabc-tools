def get_subject_from_class_title(class_title):
    title_array = class_title.split('-')
    title_array.pop()
    return '-'.join(title_array)[:-3]


def get_class_number_from_class_title(class_title):
    title_array = class_title.split('-')
    title_array.pop()
    return ' '.join(title_array).split(' ').pop()


def get_subject_code_from_class_code(class_code):
    return class_code[3:-2]


def format_text(text):
    if text == 'nan' or text == '0':
        return '-'

    text = text.replace('\r', ' ')

    return text