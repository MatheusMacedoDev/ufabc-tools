import tabula
from tabulate import tabulate
import pandas

from beaupy import confirm, select
from beaupy.spinners import *

from rich import print
from rich.console import Console

console = Console()

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


def print_ufabc_logo():
    print('''
█░█ █▀▀ ▄▀█ █▄▄ █▀▀
█▄█ █▀░ █▀█ █▄█ █▄▄
    ''')


def format_classes_dataframe(dataframe):
    dataframe.columns = ['Curso', 'Código de turma', 'Turma', 'Teoria', 'Prática', 'Campus', 'Turno', 'T-P-I', 'Vagas totais', 'Vagas veteranos', 'Docente teoria', 'Docente teoria 2', 'Docente prática', 'Docente prática 2']

    dataframe = dataframe.drop('Docente teoria 2', axis=1)
    dataframe = dataframe.drop('Docente prática 2', axis=1)

    dataframe = dataframe.astype({ 'Prática': str, 'Docente teoria': str, 'Docente prática': str, 'Teoria': str })

    dataframe['Curso'] = dataframe['Curso'].apply(format_text)
    dataframe['Docente teoria'] = dataframe['Docente teoria'].apply(format_text)
    dataframe['Docente prática'] = dataframe['Docente prática'].apply(format_text)
    dataframe['Turma'] = dataframe['Turma'].apply(format_text)
    dataframe['Teoria'] = dataframe['Teoria'].apply(format_text)

    dataframe['Prática'] = dataframe['Prática'].apply(format_text);

    dataframe['Matéria'] = dataframe['Turma'].apply(get_subject_from_class_title)
    dataframe['Turma'] = dataframe['Turma'].apply(get_class_number_from_class_title)

    dataframe['Código da matéria'] = dataframe['Código de turma'].apply(get_subject_code_from_class_code)

    dataframe = dataframe.drop('Código de turma', axis=1)

    dataframe = dataframe.iloc[:, [0, 11, 1, 9, 10, 2, 3, 4, 5, 6, 7, 8, 12]]

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

    print_ufabc_logo()
    print('[cyan]Selecione o turno:[/cyan]\n')
    selected_turn = select(turns, cursor='🢧')
    console.clear()

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

    print_ufabc_logo()
    print('[cyan]Selecione o campus:[/cyan]\n')
    selected_campus = select(campus, cursor='🢧')
    console.clear()

    if selected_campus == '[yellow]Não filtrar[/yellow]':
        return dataframe

    dataframe = dataframe[dataframe.Campus == selected_campus]

    return dataframe


def filter_classes_by_course(dataframe):
    courses = list(dataframe['Curso'].unique().tolist())
    courses.append('[yellow]Não filtrar[/yellow]')

    print_ufabc_logo()
    print('[cyan]Selecione o curso:[/cyan]\n')
    selected_course = select(courses, cursor='🢧')
    console.clear()

    if selected_course == '[yellow]Não filtrar[/yellow]':
        return dataframe

    dataframe = dataframe[dataframe.Curso == selected_course]

    return dataframe


def filter_classes_by_subject(dataframe):
    subjects = list(filtered_dataframe['Matéria'].unique().tolist())
    subjects.append('[yellow]Não filtrar[/yellow]')

    print_ufabc_logo()
    print('[cyan]Selecione a matéria:[/cyan]\n')
    selected_subject = select(subjects, cursor='🢧')
    console.clear()

    if selected_subject == '[yellow]Não filtrar[/yellow]':
        return dataframe

    dataframe = dataframe[dataframe['Matéria'] == selected_subject]

    return dataframe


spinner = Spinner(ARC, 'Carregando...')

console.clear()

print('''
⠀⠀⠀⠀⠀⠀⣤⡀⠀⠀⣠⢶⠀⠀⠀
⠀⠀⠀⣀⡤⣾⠀⠓⠒⠚⠛⣇⠀⠀⠀
⠀⠀⣼⠱⡥⣬⣧⠀⢀⡀⣀⠈⢷⠀⠀
⠀⠀⠈⠳⢧⠼⠌⠀⠈⠁⠉⢐⠛⠀⠀
⢠⡴⠦⠤⠬⡗⡆⠀⠀⠀⠀⠘⢦⠀⠀
⠘⣄⠈⠙⣲⠛⠉⠀⠀⠀⠀⠀⠀⠓⣦
⠀⠁⠙⠂⡉⡇⠀⠀⠀⡀⠀⠀⢸⠉⠉
⠀⠀⠀⠀⠀⠸⡄⠀⡌⠀⠱⣄⢸⠀⠀

█░█ █▀▀ ▄▀█ █▄▄ █▀▀
█▄█ █▀░ █▀█ █▄█ █▄▄

(Por: Matheus Macedo)
''')

if confirm('[cyan]Esse script promete te ajudar a montar sua grade na UFABC. Deseja prosseguir?[/cyan]', default_is_yes=True):

    console.clear()
    print_ufabc_logo()

    spinner.start()

    classes_pdf_uri = 'turmas_ofertadas.pdf'
    classes_dataframe = get_classes_dataframe(classes_pdf_uri)

    spinner.stop()

    isRunning = True;

    while(isRunning):
        console.clear()

        # Filter by class turn
        filtered_dataframe = filter_classes_by_turn(classes_dataframe)

        # Filter by class campus
        filtered_dataframe = filter_classes_by_campus(filtered_dataframe)

        # Filter by class course
        filtered_dataframe = filter_classes_by_course(filtered_dataframe)

        # Filter by class subject
        filtered_dataframe = filter_classes_by_subject(filtered_dataframe)

        console.clear()
        print(tabulate(filtered_dataframe, headers='keys', tablefmt='psql', maxcolwidths=12, maxheadercolwidths=8, numalign='center', stralign='center', showindex=False))

        print('\n')

        isRunning = confirm('[cyan]Deseja fazer uma nova busca?[/cyan]', default_is_yes=True)