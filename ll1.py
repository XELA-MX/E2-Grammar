import nltk
from nltk import CFG, ChartParser
import sys
sys.stdout.reconfigure(encoding='utf-8')


nltk.data.path.append("C:/Users/emipe/nltk_data")
nltk.download('punkt')
nltk.download('punkt_tab')


grammar = CFG.fromstring("""
    O  -> T Op
    Op -> 'ou' T Op | 
    T  -> F Tp
    Tp -> 'e' F Tp | 
    F  -> SV G Pr
    SV -> 'eu' 'estou' | 'você' 'está' | 'ele' 'está' | 'ela' 'está' | 'nós' 'estamos' | 'vocês' 'estão' | 'eles' 'estão' | 'elas' 'estão'
    G  -> 'falando' | 'comendo' | 'andando' | 'correndo' | 'estudando' | 'pensando'
    Prep -> 'no' | 'na' | 'em' | 'ao_lado_de' | 'perto_de'
    L  -> 'parque' | 'escola' | 'casa' | 'cinema'
    Pr -> Prep L | 
""")

parser = ChartParser(grammar)

def analizar_y_mostrar(oracion):
    try:
        tokens = nltk.word_tokenize(oracion.lower(), language='portuguese')
        tokens_unidos = []
        i = 0
        while i < len(tokens):
            if i + 2 < len(tokens) and tokens[i] == 'ao' and tokens[i+1] == 'lado' and tokens[i+2] == 'de':
                tokens_unidos.append('ao_lado_de')
                i += 3
            elif i + 1 < len(tokens) and tokens[i] == 'perto' and tokens[i+1] == 'de':
                tokens_unidos.append('perto_de')
                i += 2
            else:
                tokens_unidos.append(tokens[i])
                i += 1
        arboles = list(parser.parse(tokens_unidos))
        

        print(f"\nOración: {oracion}")
        if arboles:
            print("Análisis CORRECTO. Árbol de derivación:")
            for arbol in arboles:
                arbol.pretty_print(unicodelines=True)
            return True
        else:
            print("Análisis INCORRECTO: No se pudo construir el árbol")
            return False
            
    except Exception as e:
        print(f"Error al analizar: {str(e)}")
        return False

# Pruebas
pruebas_correctas = [
    "eu estou falando no parque",
    "você está comendo na escola",
    "nós estamos correndo perto_de casa e eles estão estudando no cinema"
]

pruebas_incorrectas = [
    "eu está andando no cinema",
    "ela pensando na escola",
    "nós estamos escola",
    "estou falando em casa"
]

print("=== PRUEBAS CORRECTAS ===")
for oracion in pruebas_correctas:
    analizar_y_mostrar(oracion)

print("\n=== PRUEBAS INCORRECTAS ===")
for oracion in pruebas_incorrectas:
    analizar_y_mostrar(oracion)

# Modo interactivo
print("\n=== MODO INTERACTIVO ===")
print("Escribe una oración en portugués (o 'salir' para terminar):")
while True:
    entrada = input("> ")
    if entrada.lower() == 'salir':
        break
    analizar_y_mostrar(entrada)
