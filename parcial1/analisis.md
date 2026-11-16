MARIA SOLEDAD INTA LARICO

# P1.1 Analizar

## a) Cuatro fragmentos (costo en el peor caso)

**F1: O(n).** El bucle da n vueltas y en cada una hace una sola suma, que cuesta lo mismo sin importar n: n x 1 = n.

**F2: O(n²).** El bucle de adentro hace n-1, n-2, ..., 1, 0 pasos (la comparación y el contador cuestan 1), y esa suma es n(n-1)/2, que crece como n².

**F3: O(log n).** En cada vuelta k se divide entre 2, y como se necesitan log2(n) divisiones para llegar a 1, el bucle da log2(n) vueltas.

**F4: O(n log n).** El bucle de afuera da n vueltas y en cada una k se duplica de 1 hasta n (log2(n) pasos), así que el total es n x log2(n).

## b) Recurrencias (teorema maestro de bolsillo)

**(i) T(n) = 3T(n/2) + n**
- a = 3 (tres llamadas), b = 2 (n se divide entre 2), d = 1 (el trabajo extra es n^1)
- b^d = 2^1 = 2
- Comparación: a = 3 es mayor que b^d = 2, así que domina la parte recursiva
- Forma: T(n) = O(n^(log2 3)), aproximadamente O(n^1,58)

**(ii) T(n) = T(n/2) + n²**
- a = 1 (una llamada), b = 2, d = 2 (el trabajo extra es n^2)
- b^d = 2^2 = 4
- Comparación: a = 1 es menor que b^d = 4, así que domina el trabajo de cada nivel
- Forma: T(n) = O(n^d) = O(n²)
