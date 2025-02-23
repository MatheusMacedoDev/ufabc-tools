import tabula
import pandas

from beaupy import confirm, select

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


def format_classes_dataframe(dataframe):
    dataframe.columns = ['Curso', 'Código de turma', 'Turma', 'Teoria', 'Prática', 'Campus', 'Turno', 'T-P-I', 'Vagas totais', 'Vagas veteranos', 'Docente teoria', 'Docente teoria 2', 'Docente prática', 'Docente prática 2']

    dataframe = dataframe.drop('Docente teoria 2', axis=1)
    dataframe = dataframe.drop('Docente prática 2', axis=1)

    dataframe['Curso'] = dataframe['Curso'].str.replace('\r', ' ')
    dataframe['Docente teoria'] = dataframe['Docente teoria'].str.replace('\r', ' ')
    dataframe['Docente prática'] = dataframe['Docente prática'].str.replace('\r', ' ')
    dataframe['Turma'] = dataframe['Turma'].str.replace('\r', ' ')
    dataframe['Teoria'] = dataframe['Teoria'].str.replace('\r', ' ')
    dataframe['Prática'] = dataframe['Prática'].str.replace('\r', ' ')

    dataframe['Matéria'] = dataframe['Turma'].apply(get_subject_from_class_title)
    dataframe['Turma'] = dataframe['Turma'].apply(get_class_number_from_class_title)

    dataframe['Código da matéria'] = dataframe['Código de turma'].apply(get_subject_code_from_class_code)

    dataframe = dataframe.drop('Código de turma', axis=1)

    return dataframe


def get_classes_dataframe(pdf_uri):

    classes_dataframe_pdf = tabula.read_pdf(pdf_uri, pages='all', encoding='latin-1', lattice=True)
    classes_dataframe = pandas.concat(classes_dataframe_pdf)
    classes_dataframe = format_classes_dataframe(classes_dataframe)

    return classes_dataframe


def filter_classes_by_turn(dataframe):
    turns = [
        'Matutino',
        'Noturno',
        '[yellow]Não filtrar[/yellow]'
    ]

    selected_turn = select(turns, cursor='🢧')

    if selected_turn == '[yellow]Não filtrar[/yellow]':
        return dataframe

    dataframe = dataframe[dataframe.Turno == selected_turn]

    return dataframe


def filter_classes_by_campus(dataframe):
    campus = [
        'SA',
        'SB',
        '[yellow]Não filtrar[/yellow]'
    ]

    selected_campus = select(campus, cursor='🢧')

    if selected_campus == '[yellow]Não filtrar[/yellow]':
        return dataframe

    dataframe = dataframe[dataframe.Campus == selected_campus]

    return dataframe


def filter_classes_by_course(dataframe):
    courses = list(dataframe['Curso'].unique().tolist())
    courses.append('[yellow]Não filtrar[/yellow]')

    selected_course = select(courses, cursor='🢧')

    if selected_course == '[yellow]Não filtrar[/yellow]':
        return dataframe

    dataframe = dataframe[dataframe.Curso == selected_course]

    return dataframe


def filter_classes_by_subject(dataframe):
    subjects = list(filtered_dataframe['Matéria'].unique().tolist())
    subjects.append('[yellow]Não filtrar[/yellow]')

    selected_subject = select(subjects, cursor='🢧')

    if selected_subject == '[yellow]Não filtrar[/yellow]':
        return dataframe

    dataframe = dataframe[dataframe['Matéria'] == selected_subject]

    return dataframe


if True or confirm('Esse script promete te ajudar a montar sua grade na UFABC. Deseja prosseguir? '):

    classes_pdf_uri = 'turmas_ofertadas.pdf'
    classes_dataframe = get_classes_dataframe(classes_pdf_uri)

    isRunning = True;

    while(isRunning):
        # Filter by class turn
        filtered_dataframe = filter_classes_by_turn(classes_dataframe)

        # Filter by class campus
        filtered_dataframe = filter_classes_by_campus(filtered_dataframe)

        # Filter by class course
        filtered_dataframe = filter_classes_by_course(filtered_dataframe)

        # Filter by class subject
        filtered_dataframe = filter_classes_by_subject(filtered_dataframe)

        print(filtered_dataframe)

        print('\n')

        isRunning = confirm('[cyan]Deseja fazer uma nova busca?[/cyan]')