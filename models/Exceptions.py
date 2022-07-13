# message = Text(f'{path} l.{line}: ') + Text(f"syntax error ", style=ERROR) + Text(customMessage + '[/not b]')
from email import message
from rich.text import Text

ERROR = '#ff2222'
## SYNTACTIC EXCEPTIONS ##
class SyntacticError(Exception):
    def __init__(self, line, customMessage='') -> None:
        message = f'Syntax Error at line {line}. ' + customMessage
        super().__init__(message)

class MissingTokenError(Exception):
    def __init__(self, token, line=None) -> None:
        if not line:
            message = f"Missing '{token}'"
        else:
            message = f"Missing '{token}' at line {line}"
        super().__init__(message)

class InvalidSyntaxError(Exception):
    def __init__(self, token) -> None:
        message = f"Unexpected token '{token.name}' at line {token.location[0]}\nInvalid syntax"
        super().__init__(message)

## SEMANTIC EXCEPTIONS ##
class UndeclaredIdError(Exception):
    def __init__(self, varName, line) -> None:
        message = f'Undeclared identifier at line {line} : {varName}'
        super().__init__(message)

class IncompatibleTypeError(Exception):
    def __init__(self, t1, t2, line, opr=False, isAtr=False) -> None:
        if not opr:
            message = f'Cannot perform operation for types {t1} and {t2} [line {line}]' 
        else:
            message = f'Operation {opr} not defined for type {t1}'

        super().__init__(message)

class AtribuitionError(Exception):
    def __init__(self, val, typev) -> None:
        message = f'Cannot assign value {val} to variable of type {typev}'
        super().__init__(message)