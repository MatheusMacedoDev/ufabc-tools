# External imports

from beaupy import select
from rich.console import Console
from rich import print


console = Console()

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


def select_input(options_list, description):
    options_list.append('[yellow]Não filtrar[/yellow]')

    print_ufabc_logo()
    print(f'[cyan]{description}[/cyan]\n')

    selected_item = select(options_list, cursor='🢧')

    console.clear()

    if selected_item == '[yellow]Não filtrar[/yellow]':
        return ['', True]

    return [selected_item, False]


def filter_classes_by_turn(dataframe):
    turns = [
        'Matutino',
        'Noturno',
    ]

    [selected_turn, is_filter_empty] = select_input(turns, 'Selecione o turno:')

    if is_filter_empty:
        return dataframe


    dataframe = dataframe[dataframe.Turno == selected_turn]

    return dataframe


def filter_classes_by_campus(dataframe):
    campus = [
        'SA',
        'SB',
    ]

    [selected_campus, is_filter_empty] = select_input(campus, 'Selecione o campus:')

    if is_filter_empty:
        return dataframe

    dataframe = dataframe[dataframe.Campus == selected_campus]

    return dataframe


def filter_classes_by_course(dataframe):
    courses = list(dataframe['Curso'].unique().tolist())

    [selected_course, is_filter_empty] = select_input(courses, 'Selecione o curso:')

    if is_filter_empty:
        return dataframe

    dataframe = dataframe[dataframe.Curso == selected_course]

    return dataframe


def filter_classes_by_subject(dataframe):
    subjects = list(dataframe['Matéria'].unique().tolist())

    [selected_subject, is_filter_empty] = select_input(subjects, 'Selecione a matéria:')

    if is_filter_empty:
        return dataframe

    dataframe = dataframe[dataframe['Matéria'] == selected_subject]

    return dataframe