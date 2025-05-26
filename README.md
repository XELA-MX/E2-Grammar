# E2-Grammar

Emilio Antonio Peralta Montiel A01712354

## Descripción

El idioma portugués, conocido como português, es una lengua romance derivada del latín, originada en la Península Ibérica a partir del galaicoportugués. Con cerca de 230 millones de hablantes nativos y entre 25 y 30 millones como segunda lengua, es la sexta lengua materna más hablada del mundo y la tercera europea en hablantes nativos. Predomina en Sudamérica y el Hemisferio Sur, especialmente en Brasil, siendo el idioma más hablado en estas regiones y el segundo en América Latina, tras el español. También es relevante en África, donde figura entre los 10 idiomas más hablados, y es oficial en organizaciones como la Unión Europea y Mercosur.

## Estructura del lenguaje

El portugués es un idioma con reglas gramaticales estructuradas, pero para simplificar, vamos a analizar solo oraciones en presente continuo afirmativo, negativo e interrogativo.

El presente continuo en portugués se utiliza para describir acciones que están ocurriendo en el momento de hablar o para planes futuros decididos. Se forma  según el pronombre, más el verbo principal en gerundio (-ando, -endo, -indo):

| Pronombre | Estar (presente) |
|-----------|------------------|
| Eu        | estou            |
| Você/Ele/Ela | está          |
| Nós       | estamos          |
| Vocês/Eles/Elas | estão      |

Luego se agrega el verbo principal en gerundio:

- Falar → falando
- Comer → comendo
- Partir → partindo

**Afirmativa:** Sujeto + estar + gerundio + complemento  
*Exemplo:* Eu estou estudando português.

**Negativa:** Sujeto + não + estar + gerundio + complemento  
*Exemplo:* Eles não estão trabalhando hoje.

**Interrogativa:** Estar + sujeito + gerundio + complemento + ?  
*Exemplo:* Você está aprendendo português?

---

Para implementar la solución, construiremos una gramática simple, eliminando ambigüedad y recursión izquierda para que sea adecuada para un analizador LL(1) creando una grámatica , eliminando la ambigüedad y eliminando la recursión izquierda.

## Creando una grámatica

En esta fase se identifican las unidades sintácticas básicas y las reglas que rigen la formación de oraciones en **presente continuo** en portugués. Se definen los siguientes elementos:

- Pronombres con su respectiva conjugación de el verbo "to be"
- Verbos en gerundio
- Preposiciones
- Lugares
- La conjunción de preposición y lugar
- Conjunciones para unir oraciones

### Gramática propuesta

O -> S V G Pr | O 'e' O | O 'ou' O
S -> 'eu' | 'você' | 'ele' | 'ela' | 'nós' | 'vocês' | 'eles' | 'elas'
V -> 'estou' | 'está' | 'estamos' | 'estão'
G -> 'falando' | 'comendo' | 'andando' | 'correndo' | 'estudando'
Prep -> 'no' | 'na' | 'em' | 'ao lado de' | 'perto de'
L -> 'parque' | 'escola' | 'casa' | 'cinema'
Pr -> Prep L

**Símbolos:**
- `O`  : oración completa
- `S`  : pronombre
- `V`  : conjugación de "estar" en presente
- `G`  : verbo en gerundio
- `Prep`: preposición
- `L`  : lugar
- `Pr` : preposición + lugar
- `'e'`: y
- `'ou'`: o

### Ejemplo de oraciones generadas

- Eu estou falando na escola  
- Ela está correndo no parque  
- Nós estamos comendo em casa  
- Eu estou estudando no cinema e vocês estão andando no parque


### Ambigüedad de la gramática

La gramática propuesta para el presente continuo en portugués es **ambigua** porque permite construir más de un árbol de derivación para ciertas oraciones compuestas, especialmente cuando se combinan las conjunciones "e" (y) y "ou" (o).

Por ejemplo, la oración:

- **"Eu estou falando na escola e você está correndo no parque ou ele está estudiando no cinema"**

#### Árbol 1

![](./imgs/a1.jfif)

#### Árbol 2

![](./imgs/a2.jfif)


### ¿Por qué es ambigua?

La ambigüedad ocurre porque la gramática permite diferentes formas de agrupar las oraciones cuando se usan varias conjunciones. Dependiendo de cómo se agrupen "e" y "ou", el significado de la frase puede cambiar, y esto se refleja en la existencia de varios árboles de derivación para una misma oración.

Esto significa que la gramática no es determinista y puede generar ambigüedad en el análisis sintáctico.

---

## Eliminar ambigüedad

Para eliminar la ambigüedad, añadimos estados intermedios y reglas que indican precedencia, evitando que una oración pueda agruparse de varias formas distintas. Así, la conjunción "ou" (or) tendrá menor precedencia que "e" (and), y la gramática solo crecerá por un lado del árbol.

Nueva grámatica:

O -> T Oa
Oa -> 'ou' T Oa | ε
T -> F Ta
Ta -> 'e' F Ta | ε
F -> S V G Pr
S -> 'eu' | 'você' | 'ele' | 'ela' | 'nós' | 'vocês' | 'eles' | 'elas'
V -> 'estou' | 'está' | 'estamos' | 'estão'
G -> 'falando' | 'comendo' | 'andando' | 'correndo' | 'estudando'
Prep-> 'no' | 'na' | 'em' | 'ao lado de' | 'perto de'
L -> 'parque' | 'escola' | 'casa' | 'cinema'
Pr -> Prep L


Con esta gramática, una oración como:

- **"Eu estou falando na escola e você está correndo no parque ou ele está estudando no cinema"**

solo puede agruparse de una forma, por ejemplo:






