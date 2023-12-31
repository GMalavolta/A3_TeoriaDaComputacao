import ply.lex as lex
import ply.yacc as yacc

# Análise Léxica
tokens = ('COR', 'TEXTO')

def t_COR(t):
    r'red|blue|green|yellow|purple|orange|black|white'
    return t

t_TEXTO = r'[a-zA-Z]+'  # Permitindo dois pontos no texto

t_ignore = ' \t\n'

def t_error(t):
    print(f"Erro léxico: Caractere inválido: {t.value[0]}")
    t.lexer.skip(1)
    parser.success = False  # Indica que houve um erro

# Análise Sintática
def p_sentenca(p):
    '''
    sentenca : COR TEXTO
            | COR
    '''
    p[0] = (p[1], p[2] if len(p) > 2 else None)

def p_error(p):
    if p:
        print(f"Erro sintático na posição {p.lexpos}: '{p.value}'")
        parser.success = False  # Indica que houve um erro
    else:
        print("Erro sintático no final da entrada")

# Análise Semântica
class ColorInterpreter:
    def __init__(self):
        self.colors = {
            "red": "Cor da paixão e energia.",
            "blue": "Cor da tranquilidade e confiança.",
            "green": "Cor da natureza e renovação.",
            "yellow": "Cor do otimismo e alegria.",
            "purple": "Cor da criatividade e espiritualidade.",
            "orange": "Cor da vitalidade e entusiasmo.",
            "black": "Cor da elegância e mistério.",
            "white": "Cor da pureza e paz.",
        }

    def verificar_semantica(self, cor, texto):
        if texto and texto.lower() not in self.colors:
            raise ValueError(f" A palavra '{texto}' não está no dicionário após a cor '{cor}'")

# Construir o analisador léxico e sintático
lexer = lex.lex()
parser = yacc.yacc()
parser.success = True  # Flag para indicar se a análise foi bem-sucedida

# Entrada do usuário
entrada_cor = input("Digite a cor em Inglês: ")

# Análise léxica e sintática
try:
    resultado_analise = parser.parse(entrada_cor, lexer=lexer)
except Exception as e:
    print(f"Erro na análise léxica/sintática: {e}")
    resultado_analise = None

# Verificar se houve erros na análise
if resultado_analise and not isinstance(resultado_analise, int) and parser.success:
    # Análise semântica
    interprete = ColorInterpreter()
    cor, texto = resultado_analise
    try:
        interprete.verificar_semantica(cor, texto)
        significado_cor = interprete.colors.get(cor.lower(), "Significado desconhecido")

        # Exibir o resultado
        if texto:
            print(f"A cor {cor} significa: {significado_cor} - Texto adicional: {texto}")
        else:
            print(f"A cor {cor} significa: {significado_cor}")

    except ValueError as e:
        print(f"Erro semântico: {e}")
else:
    print("Corrija a entrada.")
