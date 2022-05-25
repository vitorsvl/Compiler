V = ['CODE', 'ATRIBUITION', 'EXPRESSION', 'DECLARATION', 'REPETITION', 'CONDITION', 'CODE_', 
    'LINE_CODE',, 'BLOCK', 'SCALAR_ATR', 'VECTOR_ATR', 'VAL', 'VSIZE', 'ELEM', 'NUM_ELEM', 
    'CHAR_ELEM', 'TYPE', 'ARTM_EXP', 'LOGICAL_EXP', 'TERM', 'ARTM_EXP_', 'F' 'TERM_', 'LOGICAL_OP', 'CONDITION_']

Terminals: ['eof', 'empty' ,'{' '}', 'id', '=', 'num', 'id', 'str' ,'[', ']', 'char', 'int', 'float', '(', '),', '+', '-', '*', '/', '%', '!=', '>', '<', '>=', '<=' ,'if' ,'else' 'for' 'while']

FIRST[CODE] = eof empty id num ID STR char int float ( if for while
FIRST[ATRIBUITION] = id
FIRST[EXPRESSION] = id num ID STR (
FIRST[DECLARATION] = char int float
FIRST[REPETITION] = for while
FIRST[CONDITION] = empty if
FIRST[CODE_] = empty id num ID STR char int float ( if for while
FIRST[LINE_CODE] = empty id num ID STR char int float ( if for while
FIRST[BLOCK] = empty { id num ID STR char int float ( if for while
FIRST[SCALAR_ATR] = id
FIRST[VECTOR_ATR] = id
FIRST[VAL] = num ID STR
FIRST[VSIZE] = empty num
FIRST[ELEM] = empty num char
FIRST[NUM_ELEM] = empty num
FIRST[CHAR_ELEM] = empty char
FIRST[TYPE] = char int float
FIRST[ARTM_EXP] = id num ID STR (
FIRST[LOGICAL_EXP] = id num ID STR (
FIRST[TERM] = id num ID STR (
FIRST[ARTM_EXP_] = empty + -
FIRST[F] = id (
FIRST[TERM_] = empty * / %
FIRST[LOGICAL_OP] = = != > < >= <=
FIRST[CONDITION_] = else
FOLLOW[CODE] =
FOLLOW[ATRIBUITION] = eof empty id num ID STR char int float ( ) if else for while
FOLLOW[EXPRESSION] = eof empty id = num ID STR char int float ( ) + - != > < >= <= if else for while
FOLLOW[DECLARATION] = eof empty id num ID STR char int float ( if else for while
FOLLOW[REPETITION] = eof empty id num ID STR char int float ( if else for while
FOLLOW[CONDITION] = eof empty id num ID STR char int float ( if else for while
FOLLOW[CODE_] = }
FOLLOW[LINE_CODE] = eof empty id num ID STR char int float ( if else for while
FOLLOW[BLOCK] = eof empty id num ID STR char int float ( if else for while
FOLLOW[SCALAR_ATR] = eof empty id num ID STR char int float ( ) if else for while
FOLLOW[VECTOR_ATR] = eof empty id num ID STR char int float ( ) if else for while
FOLLOW[VAL] = eof empty id = num ID STR char int float ( ) + - != > < >= <= if else for while
FOLLOW[VSIZE] = ]
FOLLOW[ELEM] = }
FOLLOW[NUM_ELEM] = }
FOLLOW[CHAR_ELEM] = }
FOLLOW[TYPE] = id
FOLLOW[ARTM_EXP] = eof empty id = num ID STR char int float ( ) + - != > < >= <= if else for while
FOLLOW[LOGICAL_EXP] = eof empty id = num ID STR char int float ( ) + - != > < >= <= if else for while
FOLLOW[TERM] = eof empty id = num ID STR char int float ( ) + - != > < >= <= if else for while
FOLLOW[ARTM_EXP_] = eof empty id = num ID STR char int float ( ) + - != > < >= <= if else for while
FOLLOW[F] = empty * / %
FOLLOW[TERM_] = eof empty id = num ID STR char int float ( ) + - != > < >= <= if else for while
FOLLOW[LOGICAL_OP] = id num ID STR (
FOLLOW[CONDITION_] = eof empty id num ID STR char int float ( if else for while 