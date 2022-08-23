## Trabalho de implementação: Parte 2 - VND

 **Autor: Daniel Carneiro Freire**

Nessa parte do trabalho implementamos uma VND para o problema do caixeiro viajante. A VND implementada usa o algoritmo guloso utilizado na parte 1 do trabalho para gerar uma solução inicial, em seguida utiliza 2-OPT para buscar o ótimo local, em seguida usa o caminho obtido pelo 2-OPT para buscar no 3-OPT. Isso se repete até não ter melhora na solução.

Nessa implementação tanto o 3-OPT quanto o 2-OPT tem complexidades muito altas, por ter sido feito da maneira mais ingênua, e utilizando operações caras de lista em python. Desconsiderando o preço das operações de lista (que poderiam ser constantes utilizando uma estrutura de dados melhor), as complexidades para o 2-OPT e 3-OPT implementados é $O(n^2)$ e $O(n^3)$ respectivamente.

Os resultados estão resumidos no gráfico abaixo. A porcentagem indica o quanto a mais o valor da solução obtida foi, comparado ao valor da solução ótima, e foi obtida realizando a operação $\frac{\text{Heuristic}}{\text{Optimal}} - 1$. Incluí também o resultado da heuristica implementada na parte 1, para ter uma idéia de quanto melhor é o VND.

![](/home/shi/Documents/UFMG/Heuristics/tsp_2/output.png)



[^1]:Aarts, E, Lenstra, J. (1997) Local Search in Combinatorial Optimization. John Wiley & Sons Ltd.