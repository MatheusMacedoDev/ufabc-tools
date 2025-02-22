import tabula

classes_pdf_uri = 'turmas_ofertadas.pdf'

classes_dataframe = tabula.read_pdf(classes_pdf_uri, pages='1', encoding='latin-1')
classes_dataframe[0].columns = ['Curso', 'Código de turma', 'Turma', 'Teoria', 'Prática', 'Campus', 'Turno', 'T-P-I', 'Vagas totais', 'Vagas veteranos', 'Docente teoria', 'Docente teoria 2', 'Docente prática', 'Docente prática 2']

classes_dataframe[0] = classes_dataframe[0].drop('Docente teoria 2', axis=1)
classes_dataframe[0] = classes_dataframe[0].drop('Docente prática 2', axis=1)

classes_dataframe[0]['Curso'] = classes_dataframe[0]['Curso'].str.replace('\r', ' ')
classes_dataframe[0]['Docente teoria'] = classes_dataframe[0]['Docente teoria'].str.replace('\r', ' ')
classes_dataframe[0]['Docente prática'] = classes_dataframe[0]['Docente prática'].str.replace('\r', ' ')

print(classes_dataframe[0].iloc[0])
print(classes_dataframe[0].dtypes)