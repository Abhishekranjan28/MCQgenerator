import os
import PyPDF2
import json
import traceback
import pandas as pd

def read_file(file):
    if file.name.endswith('.pdf'):
        try:
            pdf_reader=PyPDF2.PdfReader(file)
            text=""
            for page in pdf_reader.pages:
                text+=page.extract_text()
            return text
        
        except Exception as e:
            raise Exception("Could not read the pdf file")
    
    elif file.name.endswith('.txt'):
        return file.read().decode('utf-8')

    else:
        raise Exception("Unsupported file format")
    

import json
import traceback

def get_table_data(quiz_str):
    try:
        
        quiz_json_str = quiz_str.lstrip().split('\n', 1)[-1]

        quiz_dict = json.loads(quiz_json_str)
        quiz_data_table = []

        for key, value in quiz_dict.items():
            mcq = value['mcq']
            options = " || ".join([f"{option}-> {option_value}" for option, option_value in value["options"].items()])
            correct = value['correct']
            quiz_data_table.append({'MCQ': mcq, 'options': options, 'correct': correct})

        return quiz_data_table

    except Exception as e:
        traceback.print_exception(type(e), e, e.__traceback__)
        return False
