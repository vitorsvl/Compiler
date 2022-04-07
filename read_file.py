import re
if __name__ == '__main__':
    # test

    s = 'this is a Code test for python re 3hdhfdh 12sdas (aa _abc'
    
    print(re.findall(r"\b[a-zA-Z]\w+|\b_\w+", s))
