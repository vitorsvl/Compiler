"""
Definition of the types used by the language

"""
import re


# Reserved words
rw = ['int', 'for', 'while', 'if', 'else', 'elif', 'True', 'False']

# Identifiers
identifier = 


class Type():
    rw = ['int', 'for', 'while', 'if', 'else', 'elif', 'True', 'False']
    identifier = 

class RegExTypes():
    """
    Defines the regular expressions for the language types

    RW = Reserved words
    ID = Identifier
    LOP = Logic Operator
    AOP = Arithmetic operator
    SEP = Separator
     
    """
    RW = r' *(int|float|for|if|else|while|True|False) *' 
    ID = r'\b[a-zA-Z]\w+|\b_\w+' # colocar um if not rw
    
