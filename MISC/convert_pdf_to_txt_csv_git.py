#Import the libraries
from pypdf import PdfReader 
from unidecode import unidecode
import pandas as pd
import re

#Input parameters: 
file_path=list(input("Insert file/s path, seperated by comma").split(','))
date_format=input("Insert date format")
final_file_destination = input("Insert final file destination")

for file in file_path:
    new_files = []
    # creating a pdf reader object 
    reader = PdfReader(file) 

    # creating a page object 
    page = reader.pages[0] 
    
    # extracting text from page 
    page_text = page.extract_text()
    exclude_from_end = len('Medicalc4 - nemocniční informační systém - www.medicalc.cz')

    #Extracting relevant content 
    relevant_text = page_text[92:-exclude_from_end]

    # Split the main string into individual lines
    lines = relevant_text.split('\n')

    # Initialize an empty list to collect data parts
    data_list = []

    # Loop over each set of three lines and add them to the list
    for i in range(0, len(lines), 3):
        data_parts = lines[i:i+3]
        data_list.append(data_parts)

    # Create the DataFrame from the list
    df = pd.DataFrame(data_list, columns=['Time', 'Name and Birthdate', 'Examination Details'])
    df = df[['Time', 'Name and Birthdate']] 

    #split Name and Birthdate column to seperate columns 
    df[['name','add','date of birth']] = df['Name and Birthdate'].str.split(', ', expand=True)
    df = df[['Time','name','date of birth']]

    def find_uppercase_words(text):
        words = text.split()
        uppercase_words = [word for word in words if word.isupper()]
        return uppercase_words

    def find_propercase_words(text):
        pattern = r'\b[A-Z][a-z]+\b'
        return re.findall(pattern, text)
    
    df['surename'] = df['name'].astype(str).apply(find_uppercase_words)
    df['firstname'] = df['name'].astype(str).apply(find_propercase_words)
    df['surename'] = df['surename'].apply(lambda x: ''.join(x))
    df['firstname'] = df['firstname'].apply(lambda x: ''.join(x))

    #Formatting date of birth column 
    #tomy - ddmmyyyy
    #oculus - dd.mm.yyyy
    df['date of birth'] = df['date of birth'].str.split('nar: ').str[1]
    df['date of birth'] = pd.to_datetime(df['date of birth'], format='%d.%m.%Y')

    if date_format == 'tomy':
        df['date of birth tomy'] = df['date of birth'].dt.strftime('%d%m%Y')
    if date_format == 'oculus':
        df['date of birth oculus'] = df['date of birth'].dt.strftime('%d.%m.%Y')
    else:
        df['date of birth tomy'] = df['date of birth'].dt.strftime('%d%m%Y')
        df['date of birth oculus'] = df['date of birth'].dt.strftime('%d.%m.%Y')

    #keeping only new formatted columns
    if date_format == 'tomy':
        df = df[['Time', 'surename', 'firstname','date of birth tomy']]
    if date_format == 'oculus':
        df = df[['Time', 'surename', 'firstname','date of birth oculus']]
    if date_format not in ('tomy','oculus'):
        df = df[['Time', 'surename', 'firstname','date of birth tomy','date of birth oculus']]

    #remove special charecters
    df['firstname'] = df['firstname'].apply(lambda x: unidecode(x))
    df['surename'] = df['surename'].apply(lambda x: unidecode(x))

    #drop null rows
    df = df.dropna()

    new_files.append(df)
    print(new_files)

#concat all dataframes to one 
df_combined = pd.concat(new_files, axis=0, ignore_index=True)
print(df_combined)

#save to file
df_combined.to_csv(final_file_destination)


#file_path - full pdf file path, inside the square parentheses
#date format - tomy / oculus
#final_file_path - full final file desired path + format
#final_file_format - csv / txt
convert_pdf(file_path=['/Users/may/Downloads/Fake appointments.pdf','/Users/may/Downloads/Fake appointments copy.pdf'], 
            date_format='all', 
            final_file_path='/Users/may/Documents/Python/final_doc.csv')
    