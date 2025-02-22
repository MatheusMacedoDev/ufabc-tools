import tabula
import pandas

classes_pdf_uri = 'turmas_ofertadas.pdf'

classes_dataframe_pdf = tabula.read_pdf(classes_pdf_uri, pages='1', encoding='latin-1')
classes_dataframe = pandas.concat(classes_dataframe_pdf)

classes_dataframe.columns = ['Curso', 'Código de turma', 'Turma', 'Teoria', 'Prática', 'Campus', 'Turno', 'T-P-I', 'Vagas totais', 'Vagas veteranos', 'Docente teoria', 'Docente teoria 2', 'Docente prática', 'Docente prática 2']

classes_dataframe = classes_dataframe.drop('Docente teoria 2', axis=1)
classes_dataframe = classes_dataframe.drop('Docente prática 2', axis=1)

classes_dataframe['Curso'] = classes_dataframe['Curso'].str.replace('\r', ' ')
classes_dataframe['Docente teoria'] = classes_dataframe['Docente teoria'].str.replace('\r', ' ')
classes_dataframe['Docente prática'] = classes_dataframe['Docente prática'].str.replace('\r', ' ')

print(classes_dataframe.iloc[0])
print(classes_dataframe.dtypes)