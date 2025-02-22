import tabula
import pandas

from beaupy import confirm, select

def format_classes_dataframe(dataframe):
    dataframe.columns = ['Curso', 'Código de turma', 'Turma', 'Teoria', 'Prática', 'Campus', 'Turno', 'T-P-I', 'Vagas totais', 'Vagas veteranos', 'Docente teoria', 'Docente teoria 2', 'Docente prática', 'Docente prática 2']

    dataframe = dataframe.drop('Docente teoria 2', axis=1)
    dataframe = dataframe.drop('Docente prática 2', axis=1)

    dataframe['Curso'] = dataframe['Curso'].str.replace('\r', ' ')
    dataframe['Docente teoria'] = dataframe['Docente teoria'].str.replace('\r', ' ')
    dataframe['Docente prática'] = dataframe['Docente prática'].str.replace('\r', ' ')

    return dataframe


def get_classes_dataframe(pdf_uri):
    classes_dataframe_pdf = tabula.read_pdf(pdf_uri, pages='1', encoding='latin-1')
    classes_dataframe = pandas.concat(classes_dataframe_pdf)
    classes_dataframe = format_classes_dataframe(classes_dataframe)

    return classes_dataframe


def apply_classes_dataframe_filters(dataframe, turn):
    dataframe = dataframe[dataframe.Turno == turn]

    return dataframe


if confirm('Esse script promete te ajudar a montar sua grade na UFABC. Deseja prosseguir? '):
    turns = [
        'Matutino',
        'Noturno'
    ]

    selected_turn = select(turns, cursor='🢧')

    classes_pdf_uri = 'turmas_ofertadas.pdf'

    classes_dataframe = get_classes_dataframe(classes_pdf_uri)
    classes_dataframe = apply_classes_dataframe_filters(classes_dataframe, selected_turn)

    print(classes_dataframe)
    print(classes_dataframe.dtypes)