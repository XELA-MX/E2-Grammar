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

- O -> S V G Pr | O 'e' O | O 'ou' O
- S -> 'eu' | 'você' | 'ele' | 'ela' | 'nós' | 'vocês' | 'eles' | 'elas'
- V -> 'estou' | 'está' | 'estamos' | 'estão'
- G -> 'falando' | 'comendo' | 'andando' | 'correndo' | 'estudando'
- Prep -> 'no' | 'na' | 'em' | 'ao lado de' | 'perto de'
- L -> 'parque' | 'escola' | 'casa' | 'cinema'
- Pr -> Prep L

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

- O -> T Oa
- Oa -> 'ou' T Oa | ε
- T -> F Ta
- Ta -> 'e' F Ta | ε
- F -> S V G Pr
- S -> 'eu' | 'você' | 'ele' | 'ela' | 'nós' | 'vocês' | 'eles' | 'elas'
- V -> 'estou' | 'está' | 'estamos' | 'estão'
- G -> 'falando' | 'comendo' | 'andando' | 'correndo' | 'estudando'
- Prep-> 'no' | 'na' | 'em' | 'ao lado de' | 'perto de'
- L -> 'parque' | 'escola' | 'casa' | 'cinema'
- Pr -> Prep L


Con esta gramática, una oración como:

- **"Eu estou falando na escola e você está correndo no parque ou ele está estudando no cinema"**

solo puede agruparse de una forma, por ejemplo:

![](./imgs/amb-1.jfif)


Esto fuerza la precedencia y elimina la ambigüedad, ya que "e" (and) se agrupa antes que "ou" (or).

> **Nota:**  
> Aunque la ambigüedad se elimina, la gramática aún puede tener recursividad izquierda, que se abordará en el siguiente paso.

## Eliminar recursividad izquierda

Este punto es importante, principalmente porque la forma en que los parsers procesan el lenguaje está definida por esa gramática. En nuestro caso, el analizador LL(1) es un analizador descendente que comienza por el símbolo inicial de la gramática e intenta derivar la cadena de entrada expandiendo los no terminales según las reglas de producción.

La recursividad izquierda puede crear una llamada recursiva infinita, haciendo que el parser intente expandir los no terminales indefinidamente sin consumir ninguna parte de la entrada.

Esta es la lógica que se siguió a continuación:

En la gramática original, las reglas con recursividad izquierda eran:  
1. **O → O 'ou' T | T**  
2. **T → T 'e' F | F**

### Proceso de Eliminación  
#### Para la regla **O → O 'ou' T | T**:  
1. **¿Dónde sucede?**:  
   - β = T  
   - α = 'ou' T  

2. **Generar nueva instrucción**:  
   - **O → T O'** (β seguido de nuevo no terminal)  
   - **O' → 'ou' T O' | ε** (maneja repeticiones de α)  

#### Para la regla **T → T 'e' F | F**:  
1. **¿Dónde sucede?**:  
   - β = F  
   - α = 'e' F  

2. **Generar nueva instrucción**:  
   - **T → F T'**  
   - **T' → 'e' F T' | ε**  


#### Nueva Gramática

- O  → T O'
- O' → 'ou' T O' | ε
- T  → F T'
- T' → 'e' F T' | ε
- F  → S V G Pr
- S  → 'eu' | 'você' | 'ele' | 'ela' | 'nós' | 'vocês' | 'eles' | 'elas'
- V  → 'estou' | 'está' | 'estamos' | 'estão'
- G  → 'falando' | 'comendo' | 'andando' | 'correndo' | 'estudando'
- Prep → 'no' | 'na' | 'em' | 'ao lado de' | 'perto de'
- L  → 'parque' | 'escola' | 'casa' | 'cinema'
- Pr → Prep L

De esta manera, por el lado izquierdo siempre encontrará los elementos terminales, mientras que del lado derecho irán apareciendo los no terminales hasta terminar con la oración que se corta con un épsilon ε.

---

**Referencia: (1)**  

---

## Análisis de Complejidad con la Jerarquía de Chomsky

La complejidad de la gramática se analiza utilizando la jerarquía de Chomsky, tanto antes como después de limpiar la gramática.

### Antes de la limpieza:
- **Gramática original**: Tipo 2 (Libre de contexto) con recursividad izquierda
- **Problemas**: Ambigüedad y recursividad izquierda impiden análisis LL(1)

### Después de la limpieza:
- **Gramática modificada**: Tipo 2 (Libre de contexto) sin recursividad izquierda
- **Ventajas**: Compatible con analizadores LL(1), determinista, sin ambigüedades

La transformación mantiene la gramática en el mismo nivel de la jerarquía de Chomsky (Tipo 2), pero la hace más eficiente para el análisis sintáctico descendente.

## Primer y siguiente estado

Para finalizar, realizamos nuestra tabla de primer y siguiente estado para preparar la construcción del parser. **First** ayuda cuando tienes un no terminal y quieres saber qué producción usar: comparas el token de entrada con los conjuntos de First de cada producción, si la entrada está aquí, la usas. **Follow** ayuda cuando en el no terminal se encuentra vacío (ε) en el First; si es el caso, usas estos.

### Tabla de conjuntos FIRST y FOLLOW

| Estado | Nullable? | First()                                                     | Follow()                                              |
|--------|-----------|-------------------------------------------------------------|-------------------------------------------------------|
| O      | ✗         | {eu, você, ele, ela, nós, vocês, eles, elas}               | {$}                                                   |
| O'     | ✓         | {ou, ε}                                                     | {$}                                                   |
| T      | ✗         | {eu, você, ele, ela, nós, vocês, eles, elas}               | {ou, $}                                               |
| T'     | ✓         | {e, ε}                                                      | {ou, $}                                               |
| F      | ✗         | {eu, você, ele, ela, nós, vocês, eles, elas}               | {e, ou, $}                                            |
| S      | ✗         | {eu, você, ele, ela, nós, vocês, eles, elas}               | {estou, está, estamos, estão}                        |
| V      | ✗         | {estou, está, estamos, estão}                              | {falando, comendo, andando, correndo, estudando}     |
| G      | ✗         | {falando, comendo, andando, correndo, estudando}           | {no, na, em, ao lado de, perto de}                   |
| Prep   | ✗         | {no, na, em, ao lado de, perto de}                         | {parque, escola, casa, cinema}                       |
| L      | ✗         | {parque, escola, casa, cinema}                             | {e, ou, $}                                            |
| Pr     | ✗         | {no, na, em, ao lado de, perto de}                         | {e, ou, $}                                            |

## Implementación y Pruebas

Ya que tenemos nuestra gramática, realizamos la implementación en Python. El programa analiza las oraciones llamando a una función que valida si la estructura es correcta según la gramática definida. Además, se incluyen pruebas automatizadas: si alguna prueba falla, el programa imprime "No se puede analizar". Puedes consultar el código completo en el archivo correspondiente de este repositorio.

### Pruebas correctas

Las siguientes oraciones cumplen con la gramática definida y son reconocidas correctamente por el analizador:

- eu estou falando no parque
- você está comendo na escola
- nós estamos correndo perto_de casa e eles estão estudando no cinema

### Pruebas incorrectas

Las siguientes oraciones no cumplen con la gramática y el programa responde con "No se puede analizar":

- eu está andando no cinema           // Error de conjugación
- ela pensando na escola              // Falta el verbo auxiliar
- nós estamos escola                  // Falta la preposición
- estou falando em casa               // Falta el sujeto

## Ejecutar el programa

Para ejecutar el programa, sigue estos pasos:

1. **Asegúrate de tener Python instalado** en tu sistema.
2. **Instala NLTK** si aún no lo tienes:
   
> pip install nltk

3. **Descarga el archivo** `ll1.py` que contiene la implementación del analizador y las pruebas.
4. **Ejecuta el programa desde la terminal** en la carpeta donde guardaste el archivo:

> python ll1.py

Al ejecutar el programa, la salida mostrará los árboles de derivación para las oraciones válidas y el mensaje "Análisis INCORRECTO: No se pudo construir el árbol" para las oraciones que no cumplen con la gramática.

## Bibliografías
(1) Teoría de la Computación. (2011). *Eliminación de recursividad izquierda*. Recuperado de http://teodelacomp.blogspot.com/2011/03/eliminacion-de-recursividad-izquierda.html
Kevin Lajpop. (2021, 21 septiembre). Cálculo de primeros y siguientes: LL1 [Vídeo]. YouTube. https://www.youtube.com/watch?v=FX9bQ_YNlIc

