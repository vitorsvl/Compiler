## SYNTACTIC EXCEPTIONS ##
class SyntacticError(Exception):
    def __init__(self, line, customMessage='') -> None:
        message = f"Syntax error at line {line}. " + customMessage
        super().__init__(message)

class MissingTokenError(Exception):
    def __init__(self, token, line=None) -> None:
        if not line:
            message = f"Syntax Error. Missing '{token}'"
        else:
            message = f"Syntax Error. Missing '{token}' at line {line}"
        super().__init__(message)

class InvalidSyntaxError(Exception):
    def __init__(self, token) -> None:
        message = f"Syntax Error. Unexpected token '{token.name}' at line {token.location[0]}\nInvalid syntax"
        super().__init__(message)

## SYNTACTIC EXCEPTIONS ##
