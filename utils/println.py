from __future__ import unicode_literals, print_function 

import sys
from prompt_toolkit.document import Document

def printText(text, end='\n', outputField=None):
    if outputField == None:
        frameLocals = sys._getframe().f_back.f_back.f_locals
        if 'self' in frameLocals:
            outputField = frameLocals['self'].__dict__['printField']
            #outputField = frameLocals['self']['printField']
        else:
            return
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
