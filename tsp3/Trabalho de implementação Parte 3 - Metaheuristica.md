## Trabalho de implementação: Parte 3 - Metaheurística

 **Autor: Daniel Carneiro Freire**

Nessa parte do trabalho implementamos uma metaheurística para o problema do caixeiro viajante. A metaheurística escolhida foi o Tabu Search, sem memória a longo prazo, com lista tabu de tamanho variável e função de vizinhança 2-OPT.

O critério de parada escolhido para o algorítmo foi a quantidade de iterações antes da última melhora. Para os experimentos realizados esse valor foi configurado para 500 iterações. Possívelmente esse valor poderia ser bem menor e obter resultados similares. O algorítmo teve uma performance de tempo similar ao VND para os paramêtros utilizados.

Na implementação foi utilizada uma estratégia de alteração no tamanho da lista tabu, principalmente para compensar a falta de memória a longo prazo. A estratégia é sempre que o custo obtido em uma iteração for o mesmo do melhor custo, nós aumentamos o tamanho da lista em um fator de 1.2 arredondado para baixo, sempre que obtemos um resultado melhor, o tamanho da lista volta ao tamanho original. Esse valor de 1.2 é um metaparametro que foi obtido com poucos experimentos, então provavelmente existem valores melhores.

Os resultados estão resumidos no gráfico abaixo. A porcentagem indica o quanto a mais o valor da solução obtida foi, comparado ao valor da solução ótima, e foi obtida realizando a operação $\frac{\text{Heuristic}}{\text{Optimal}} - 1$. Incluí também o resultado da heuristica implementada nas partes 1 e 2, para ter uma idéia de quanto melhor é o tabu search.

![](/home/shi/Documents/UFMG/Heuristics/tsp3/output.png)
