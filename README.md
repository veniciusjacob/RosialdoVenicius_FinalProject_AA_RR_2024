# Executor Simbólico para o Problema do Caixeiro Viajante (TSP)

O Executor Simbólico é uma técnica de análise estática que explora todas as execuções possíveis de um programa utilizando entradas simbólicas ao invés de valores concretos. Isso permite uma avaliação abrangente dos caminhos de execução do programa, auxiliando na detecção de bugs e na otimização de soluções. O conceito foi introduzido por James C. King em seu artigo seminal, "Symbolic Execution and Program Testing".

## Relacionamento com o Z3

O Z3 é um solver SMT (Satisfiability Modulo Theories) desenvolvido para resolver problemas de decisão baseados em lógica matemática. No contexto deste projeto, o Z3 é utilizado para formular o Problema do Caixeiro Viajante (TSP) como um conjunto de restrições matemáticas, permitindo a modelagem e solução do problema. A execução simbólica é empregada para representar as decisões de rota como variáveis simbólicas e o Z3 resolve essas variáveis para satisfazer todas as restrições impostas pelo problema.

## Problema do Caixeiro Viajante (TSP)

O TSP é um problema de otimização combinatória onde um agente deve visitar um conjunto de cidades exatamente uma vez e retornar à cidade de origem, minimizando a distância total percorrida. O Z3 é utilizado para definir e resolver este problema, onde as cidades são representadas como nós e as viagens entre cidades são variáveis de decisão. A execução simbólica ajuda a garantir que todas as rotas possíveis sejam avaliadas e que a solução encontrada seja a mais eficiente.

## Visão Geral

O código utiliza conceitos de execução simbólica descritos por James C. King e emprega o solver Z3 para encontrar a solução para o TSP. A execução simbólica modela as decisões do Caixeiro Viajante e o Z3 garante que todas as restrições sejam respeitadas, fornecendo a rota mais curta possível.

## Como Funciona

1. **Criação das Variáveis de Decisão:**
   - Uma matriz de variáveis simbólicas `x[i][j]` é criada para representar se um caminho entre a cidade `i` e a cidade `j` é incluído na solução.

2. **Restrições de Valores das Variáveis:**
   - As variáveis `x[i][j]` são binárias (0 ou 1).
   - A restrição `x[i][i]` deve ser 0 para garantir que não haja laços.

3. **Restrições de Precisão das Cidades:**
   - Cada cidade deve ter exatamente uma entrada e uma saída, garantindo a formação de um ciclo. Isso é garantido com as restrições `Sum(saidas) == 1` e `Sum(entradas) == 1`.

4. **Função Objetivo:**
   - A função objetivo é minimizar a distância total percorrida, e o Z3 é utilizado para minimizar essa função através de `solver.minimize(objective)`.

5. **Verificação e Exibição dos Resultados:**
   - O código verifica a satisfação das restrições e exibe o caminho encontrado e a distância total percorrida.

## Como Usar

1. **Instale o Z3:**
   - Certifique-se de que o Z3 esteja instalado. Você pode instalar a biblioteca usando pip:
     ```bash
     pip install z3-solver
     ```

2. **Execute o Código:**
   - Salve o código em um arquivo chamado `app_saidaComum.py` ou `app_saidaDetalhada.py` e execute-o com o Python:
     ```bash
     app_saidaComum.py
     ```

3. **Saída Esperada:**
   - Para cada matriz de distâncias fornecida, o código exibirá o caminho mais curto encontrado e a distância total percorrida.

## Testes

O código inclui vários testes com diferentes matrizes de distâncias para avaliar sua eficácia:

- **Teste 1:** Caso Simples (3 cidades)
- **Teste 2:** Distâncias Variadas (4 cidades)
- **Teste 3:** Assimetrias no Caminho (4 cidades)
- **Teste 4:** Caminhos Longos e Curtos (4 cidades)
- **Teste 5:** Cidades Muito Próximas (5 cidades)
- **Teste 6:** Grande Desigualdade nas Distâncias (5 cidades)
- **Teste 7:** Distâncias Aleatórias (6 cidades)
- **Teste 8:** Matriz Grande com Simetria (8 cidades)

Cada teste cobre diferentes cenários, desde distâncias aleatórias até distâncias com grande desigualdade.

## Referência

Este código utiliza conceitos descritos por James C. King em seu artigo seminal "Symbolic Execution and Program Testing":

- James C. King. 1976. Symbolic execution and program testing. Commun. ACM 19, 7 (July 1976), 385–394.
- [Link para o artigo](https://doi.org/10.1145/360248.360252)

