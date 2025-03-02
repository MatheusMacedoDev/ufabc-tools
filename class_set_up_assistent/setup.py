# External imports

from tabulate import tabulate

from beaupy import confirm, select, select_multiple

from rich import print
from rich.console import Console

# Internal imports

import cli
import table
import config


console = Console()

console.clear()

cli.print_start_decoration()

if confirm('[cyan]Esse script promete te ajudar a montar sua grade na UFABC. Deseja prosseguir?[/cyan]', default_is_yes=True):

    console.clear()
    cli.print_ufabc_logo()

    classes_dataframe = cli.spinner_loading(
        lambda: table.get_classes_dataframe(config.classes_pdf_uri)
    )

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

            selected_days_of_week = select_multiple(config.days_of_week, tick_character='✓')

            unselected_days_of_week = config.days_of_week
            for selected_day_of_week in selected_days_of_week:
                unselected_days_of_week.remove(selected_day_of_week)

            console.clear()

            print('[cyan]Selecione o horário da aula:[/cyan]')

            selected_timetables = select_multiple(config.timetables, tick_character='✓')

            unselected_timetables = config.timetables
            for selected_timetable in selected_timetables:
                unselected_timetables.remove(selected_timetable)

            console.clear()

            should_filter_exclusively = confirm('[cyan]Mostrar exclusivamente aqueles que seguem o filtro?[/cyan]', default_is_yes=True)

            if should_filter_exclusively:
                filtered_dataframe = table.filter_dataframe_by_day_and_timetable(filtered_dataframe, selected_timetables, unselected_timetables, selected_days_of_week, unselected_days_of_week)
            else:
                filtered_dataframe = table.filter_dataframe_by_day_and_timetable(filtered_dataframe, selected_timetables, [], selected_days_of_week, [])

        console.clear()
        print(tabulate(filtered_dataframe, headers='keys', tablefmt='mixed_grid', maxcolwidths=12, maxheadercolwidths=8, numalign='center', stralign='center', showindex=False))
        print('\n')

        isRunning = confirm('[cyan]Deseja fazer uma nova busca?[/cyan]', default_is_yes=True)