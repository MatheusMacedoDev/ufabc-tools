# External imports

import pandas
import tabula
from tabulate import tabulate

from beaupy import confirm, select
from beaupy.spinners import *

from rich import print
from rich.console import Console

# Internal imports

import text
import cli


def format_classes_dataframe(dataframe):
    dataframe.columns = ['Curso', 'Código de turma', 'Turma', 'Teoria', 'Prática', 'Campus', 'Turno', 'T-P-I', 'Vagas totais', 'Vagas veteranos', 'Docente teoria', 'Docente teoria 2', 'Docente prática', 'Docente prática 2']

    dataframe = dataframe.drop('Docente teoria 2', axis=1)
    dataframe = dataframe.drop('Docente prática 2', axis=1)

    dataframe = dataframe.astype({ 'Prática': str, 'Docente teoria': str, 'Docente prática': str, 'Teoria': str })

    dataframe['Curso'] = dataframe['Curso'].apply(text.format_text)
    dataframe['Docente teoria'] = dataframe['Docente teoria'].apply(text.format_text)
    dataframe['Docente prática'] = dataframe['Docente prática'].apply(text.format_text)
    dataframe['Turma'] = dataframe['Turma'].apply(text.format_text)
    dataframe['Teoria'] = dataframe['Teoria'].apply(text.format_text)

    dataframe['Prática'] = dataframe['Prática'].apply(text.format_text);

    dataframe['Matéria'] = dataframe['Turma'].apply(text.get_subject_from_class_title)
    dataframe['Turma'] = dataframe['Turma'].apply(text.get_class_number_from_class_title)

    dataframe['Código da matéria'] = dataframe['Código de turma'].apply(text.get_subject_code_from_class_code)

    dataframe = dataframe.drop('Código de turma', axis=1)

    dataframe = dataframe.iloc[:, [0, 11, 1, 9, 10, 2, 3, 4, 5, 6, 7, 8, 12]]

    return dataframe


def get_classes_dataframe(pdf_uri):

    classes_dataframe_pdf = tabula.read_pdf(pdf_uri, pages='all', encoding='latin-1', lattice=True)
    classes_dataframe = pandas.concat(classes_dataframe_pdf)
    classes_dataframe = format_classes_dataframe(classes_dataframe)

    return classes_dataframe


console = Console()

spinner = Spinner(ARC, 'Carregando...')

console.clear()

cli.print_start_decoration()

if confirm('[cyan]Esse script promete te ajudar a montar sua grade na UFABC. Deseja prosseguir?[/cyan]', default_is_yes=True):

    console.clear()
    cli.print_ufabc_logo()

    spinner.start()

    classes_pdf_uri = 'turmas_ofertadas.pdf'
    classes_dataframe = get_classes_dataframe(classes_pdf_uri)

    spinner.stop()

    isRunning = True;

    while(isRunning):
        console.clear()

        print('[cyan]Selecione o tipo de filtragem que deseja aplicar:[/cyan]')

        filter_options = [
            'Filtrar por categorias',
            'Filtrar por dia/horário'
        ]

        selected_filter_option = select(filter_options, cursor='🢧')

        filtered_dataframe = classes_dataframe

        console.clear()

        if selected_filter_option == filter_options[0]:

            # Filter by class turn
            filtered_dataframe = cli.filter_classes_by_turn(filtered_dataframe)

            # Filter by class campus
            filtered_dataframe = cli.filter_classes_by_campus(filtered_dataframe)

            # Filter by class course
            filtered_dataframe = cli.filter_classes_by_course(filtered_dataframe)

            # Filter by class subject
            filtered_dataframe = cli.filter_classes_by_subject(filtered_dataframe)

        if selected_filter_option == filter_options[1]:
            print('[cyan]Selecione o dia da semana:[/cyan]')

            days_of_week = [
                'Segunda',
                'Terça',
                'Quarta',
                'Quinta',
                'Sexta',
                'Sábado',
                'Domingo',
                '[yellow]Não filtrar[/yellow]'
            ]
            
            day_of_week = select(days_of_week, cursor='🢧')

            filtered_dataframe = filtered_dataframe[
                filtered_dataframe['Teoria'].str.contains(day_of_week, case=False, regex=False)
                | filtered_dataframe['Prática'].str.contains(day_of_week, case=False, regex=False)
            ]

            console.clear()

            print('[cyan]Selecione o horário da aula:[/cyan]')

            timetable = [
                '8:00 às 10:00',
                '10:00 às 12:00',
                '19:00 às 21:00',
                '21:00 às 23:00',
                '[yellow]Não filtrar[/yellow]'
            ]
            
            selected_timetable = select(timetable, cursor='🢧')

            filtered_dataframe = filtered_dataframe[
                filtered_dataframe['Teoria'].str.contains(selected_timetable, case=False, regex=False)
                | filtered_dataframe['Prática'].str.contains(selected_timetable, case=False, regex=False)
            ]

        console.clear()
        print(tabulate(filtered_dataframe, headers='keys', tablefmt='mixed_grid', maxcolwidths=12, maxheadercolwidths=8, numalign='center', stralign='center', showindex=False))
        print('\n')

        isRunning = confirm('[cyan]Deseja fazer uma nova busca?[/cyan]', default_is_yes=True)