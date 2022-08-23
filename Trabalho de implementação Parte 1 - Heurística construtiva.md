## Trabalho de implementação: Parte 1 - Heurística construtiva

 **Autor: Daniel Carneiro Freire**

Essa primeira parte do trabalho teve como objetivo implementar uma heurística construtiva para o problema do caixeiro viajante. Optei por implementar a heuristica gulosa[^1], que no caso dos arquivos de teste providos, é equivalente a heurística de vizinhos mais próximos, por se tratar de grafos completos.

A implementação foi feita em duas funções. A primeira, `read_file/1` lê o arquivo de teste e retorna a matriz de adjacencia com pesos de cada aresta para o grafo correspondente, sua complexidade é dominada pelo preenchimento dos valores da matriz que é $O(n^2)$. A segunda, `tsp_optimized/1` realiza a heuristica, sua complexidade é dominada pela operação de encontrar o vizinho mais próximo ($O(n)$) que é realizada $O(n)$ vezes, portanto a complexidade da função é $O(n²)$.

Os resultados estão resumidos no gráfico abaixo. A porcentagem indica o quanto a mais o valor da solução obtida foi, comparado ao valor da solução ótima, e foi obtida realizando a operação $\frac{\text{Heuristic}}{\text{Optimal}} - 1$.

![](/home/shi/Documents/UFMG/Heuristics/output.png)



[^1]:Aarts, E, Lenstra, J. (1997) Local Search in Combinatorial Optimization. John Wiley & Sons Ltd.