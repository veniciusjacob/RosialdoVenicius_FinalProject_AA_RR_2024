# Executor Simbólico:

- O executor simbólico é uma técnica de análise estática que busca explorar todas as execuções possíveis de um programa, considerando entradas simbólicas ao invés de valores concretos. Isso permite avaliar caminhos diferentes de execução do programa para detectar bugs ou otimizar soluções.
O artigo de James C. King introduz o conceito de execução simbólica, onde ele descreve como uma ferramenta para explorar sistematicamente diferentes comportamentos de um programa. No contexto atual, a execução simbólica é utilizada para resolver problemas de tomada de decisão dentro do programa, como o problema do Caixeiro Viajante.

## Relacionamento com o Z3:

- O Z3 é um solver SMT (Satisfiability Modulo Theories) que permite resolver problemas de decisão baseados em lógica matemática. No projeto atual, o Z3 pode ser utilizado para formular o problema do Caixeiro Viajante como um conjunto de restrições, como a necessidade de passar por todas as cidades sem retornar a uma cidade anterior antes de completar o ciclo.
A execução simbólica no Z3 pode modelar cada decisão de rota como uma variável simbólica, e o solver trabalha para satisfazer as restrições que garantem que o ciclo seja válido, sem redundâncias.

## Caixeiro Viajante (TSP):

- O TSP é um problema de otimização combinatória onde um agente deve visitar um conjunto de cidades exatamente uma vez e retornar à cidade de origem, minimizando a distância total percorrida.
- O Z3 pode ser utilizado para definir esse problema, onde as cidades são representadas como nós e as viagens entre cidades são variáveis de decisão. A execução simbólica ajuda a garantir que todas as possíveis rotas sejam avaliadas, e o Z3 encontra a solução que satisfaz todas as restrições.

## Visão Geral

O código usa conceitos de execução simbólica descritos por James C. King em seu artigo seminal "Symbolic Execution and Program Testing". A execução simbólica permite modelar diferentes decisões que o Caixeiro Viajante deve tomar, e o solver Z3 é usado para garantir que essas decisões respeitem as restrições do problema.

## Como Funciona

**Criação das Variáveis de Decisão:**
- Uma matriz de variáveis simbólicas `x[i][j]` é criada para representar se um caminho entre a cidade `i` e a cidade `j` é parte da solução.

**Restrições de Valores das Variáveis:**
- As variáveis `x[i][j]` são restritas a 0 ou 1.
- A restrição `x[i][i]` deve ser 0, garantindo que não haja laços.

**Restrição de Precisão das Cidades:**
- Cada cidade deve ter exatamente uma entrada e uma saída, garantindo que o caminho formado seja um ciclo. As restrições de que cada cidade deve ter exatamente uma entrada e uma saída são implementadas de forma eficiente com `Sum(saidas) == 1` e `Sum(entradas) == 1.`

**Função Objetivo:**
- A função objetivo é minimizar a distância total percorrida e usa `solver.minimize(objective)` para isso.

**Verificação e Exibição dos Resultados:**
- O código verifica a satisfação das restrições e exibe o caminho encontrado e a distância total.
   
## Como Usar

1. **Instale o Z3:**
   
   Certifique-se de ter o Z3 instalado. Você pode instalar a biblioteca usando pip:
   ```bash
   pip install z3-solver
   ```

2. **Execute o Código:**
   ```bash
   python3 tsp_solver.py
   ```
3. **Saída Esperada:**: 

- Para cada matriz de distâncias, o código exibirá o caminho mais curto encontrado e a distância total.

## Testes

O código inclui vários testes com diferentes matrizes de distâncias:

- distance_matrix_test_1
- distance_matrix_test_2
- distance_matrix_test_3
- distance_matrix_test_4
- distance_matrix_test_5
- distance_matrix_test_6
- distance_matrix_test_7
- distance_matrix_test_8
- distance_matrix_test_9
- distance_matrix_test_10

Esses testes cobrem distâncias aleatórias, crescentes e grandes.

## Referência

- este código utiliza conceitos de execução simbólica descritos por James C. King em seu artigo seminal "Symbolic Execution and Program Testing". A execução simbólica nos permite modelar as diferentes decisões que o Caixeiro Viajante deve tomar, e o solver Z3 é usado para garantir que essas decisões respeitem as restrições do problema. Ao formular o TSP no Z3, utilizamos variáveis simbólicas para representar as cidades e os caminhos, garantindo que cada rota seja única e otimizada.

`James C. King. 1976. Symbolic execution and program testing. Commun. ACM 19, 7 (July 1976), 385–394.
https://doi.org/10.1145/360248.360252`


