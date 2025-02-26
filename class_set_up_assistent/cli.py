# External imports

from beaupy import select
from rich.console import Console
from rich import print


console = Console()


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
    subjects = list(dataframe['Matéria'].unique().tolist())
    subjects.append('[yellow]Não filtrar[/yellow]')

    print_ufabc_logo()
    print('[cyan]Selecione a matéria:[/cyan]\n')
    selected_subject = select(subjects, cursor='🢧')
    console.clear()

    if selected_subject == '[yellow]Não filtrar[/yellow]':
        return dataframe

    dataframe = dataframe[dataframe['Matéria'] == selected_subject]

    return dataframe

def print_ufabc_logo():
    print('''
█░█ █▀▀ ▄▀█ █▄▄ █▀▀
█▄█ █▀░ █▀█ █▄█ █▄▄
    ''')


def print_start_decoration():
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