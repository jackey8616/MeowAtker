from __future__ import unicode_literals, print_function 

from prompt_toolkit.document import Document

def printText(outputField, text, end='\n'):
    if type(outputField) != list:
        outputField = [outputField]
    for eachField in outputField:
        new_text = eachField.text + str(text) + end
        eachField.buffer.document = Document(
            text=new_text, cursor_position=len(new_text)
        )

def println(outputField, inputField, end='\n'):
    if type(outputField) != list:
        outputField = [outputField]
    for eachField in outputField:
        new_text = eachField.text + inputField.text + end 
        eachField.buffer.document = Document(
            text=new_text, cursor_position=len(new_text)
        )
    inputField.text = ''
