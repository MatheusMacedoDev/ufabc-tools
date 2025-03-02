# External imports

import pandas
import tabula

# Internal imports

import config
import text

def format_classes_dataframe(dataframe):
    dataframe.columns = config.starter_classes_table_columns

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


def add_filtered_by_substrings_elements_to_mask(mask, dataframe, substrings):
    for substring in substrings:
        mask |= (
            dataframe['Teoria'].str.contains(substring, case=False, na=False) |
            dataframe['Prática'].str.contains(substring, case=False, na=False)
        )


def filter_dataframe_by_day_and_timetable(dataframe, include_timetables, exclude_timetables, include_days_of_week, exclude_days_of_week):
    if (len(include_timetables) == 0 and len(include_days_of_week) == 0):
        return dataframe

    include_mask = pandas.Series(False, index=dataframe.index)
    exclude_mask = pandas.Series(False, index=dataframe.index)

    if (len(include_timetables) > 0):
        add_filtered_by_substrings_elements_to_mask(include_mask, dataframe, include_timetables)
        add_filtered_by_substrings_elements_to_mask(exclude_mask, dataframe, exclude_timetables)

    if (len(include_days_of_week) > 0):
        add_filtered_by_substrings_elements_to_mask(include_mask, dataframe, include_days_of_week)
        add_filtered_by_substrings_elements_to_mask(exclude_mask, dataframe, exclude_days_of_week)

    return dataframe[include_mask & ~exclude_mask]