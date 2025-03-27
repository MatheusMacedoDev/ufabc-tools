# External imports

from beaupy import select
from beaupy.spinners import *
from rich.console import Console
from rich import print

# Internal imports

import config


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

spinner = Spinner(ARC, 'Carregando...')

def spinner_loading(callback_fn):
    spinner.start()
    return_of_callback = callback_fn()
    spinner.stop()

    return return_of_callback



def select_input(options_list, description):
    last_option_text = '[yellow]Não filtrar[/yellow]'

    if last_option_text not in options_list:
        options_list.append(last_option_text)

    print_ufabc_logo()
    print(f'[cyan]{description}[/cyan]\n')

    selected_item = select(options_list, cursor='🢧')

    console.clear()

    if selected_item == '[yellow]Não filtrar[/yellow]':
        return ['', True]

    return [selected_item, False]


def filter_classes_by_turn(dataframe):
    [selected_turn, is_filter_empty] = select_input(config.turns, 'Selecione o turno:')

    if is_filter_empty:
        return dataframe


    dataframe = dataframe[dataframe.Turno == selected_turn]

    return dataframe


def filter_classes_by_campus(dataframe):
    [selected_campus, is_filter_empty] = select_input(config.campus, 'Selecione o campus:')

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