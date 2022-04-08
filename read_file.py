import re


def read_file(path: str) -> str:
    """
    Gets a text file and returns it's content in a string
    """
    with open(path, "r") as file:
        s = file.read()
        return s

    
def identify_tokens(text: str) -> List:
    """
    Returns a list of the successfully identified tokens found in the  text
    """
    sentinel = 0 # pointer that starts at the begining of the text
    look_ahead = 0 # pointer to look ahead of sentinel
    while sentinel < len(text):
        c = text[sentinel] 
        # verificar em quais tipos o caractere c se encaixa, em seguida o look ahead anda para identificar o token







if __name__ == '__main__':
    # test

    s = 'this is a Code test for python re 3hdhfdh 12sdas (aa _abc'
    
    print(re.findall(r"\b[a-zA-Z]\w+|\b_\w+", s))
