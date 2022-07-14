from rich.console import Console
from rich.text import Text

# WARNING TYPES #
c = Console()
WARN = '#f0b432 '

class RedeclarationWarning():
    def __init__(self, varName: str, warnLine: int, atLine: int, path: str) -> None:
        t1 = Text(f'{path} l.{warnLine}: ', style='b')
        t2 = Text('warning: ', style=WARN + 'b')
        t3 = Text(f'Identifier {varName} was perviously declared at line {atLine}', style='not b')
        self._wmessage = t1 + t2 + t3

    def show(self):
        c.print(self._wmessage)

class NotInitializedWarning():
    def __init__(self, varName: str, wline: int, path: str) -> None:
        t1 = Text(f'{path} l.{wline}: ', style='b')
        t2 = Text('warning: ', style=WARN + 'b')
        t3 = Text(f'Identifier {varName} was not initialized.', style='not b')
        self._wmessage = t1 + t2 + t3

    def show(self):
        c.print(self._wmessage)
            

    