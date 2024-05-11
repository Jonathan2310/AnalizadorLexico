import ply.lex as lex

# Lista de palabras reservadas
reserved = {
    'for': 'FOR',
    'do': 'DO',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE'
}

# Lista de tokens
tokens = [
    'LPAREN', 'RPAREN', 'ID'
] + list(reserved.values())

# Expresiones regulares para tokens simples
t_LPAREN = r'\('
t_RPAREN = r'\)'

# Palabras reservadas
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserved.get(t.value, 'ID')
    return t

# Ignorar espacios y tabs
t_ignore = ' \t'

# Control de errores
def t_error(t):
    print(f"Illegal character {t.value[0]}")
    t.lexer.skip(1)

# Construir el lexer
lexer = lex.lex()