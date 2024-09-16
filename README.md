#Executor Simbólico:

- O executor simbólico é uma técnica de análise estática que busca explorar todas as execuções possíveis de um programa, considerando entradas simbólicas ao invés de valores concretos. Isso permite avaliar caminhos diferentes de execução do programa para detectar bugs ou otimizar soluções.
O artigo de James C. King introduz o conceito de execução simbólica, onde ele descreve como uma ferramenta para explorar sistematicamente diferentes comportamentos de um programa. No contexto atual, a execução simbólica é utilizada para resolver problemas de tomada de decisão dentro do programa, como o problema do Caixeiro Viajante.

## Relacionamento com o Z3:

- O Z3 é um solver SMT (Satisfiability Modulo Theories) que permite resolver problemas de decisão baseados em lógica matemática. No projeto atual, o Z3 pode ser utilizado para formular o problema do Caixeiro Viajante como um conjunto de restrições, como a necessidade de passar por todas as cidades sem retornar a uma cidade anterior antes de completar o ciclo.
A execução simbólica no Z3 pode modelar cada decisão de rota como uma variável simbólica, e o solver trabalha para satisfazer as restrições que garantem que o ciclo seja válido, sem redundâncias.

## Caixeiro Viajante (TSP):

- O TSP é um problema de otimização combinatória onde um agente deve visitar um conjunto de cidades exatamente uma vez e retornar à cidade de origem, minimizando a distância total percorrida.
- O Z3 pode ser utilizado para definir esse problema, onde as cidades são representadas como nós e as viagens entre cidades são variáveis de decisão. A execução simbólica ajuda a garantir que todas as possíveis rotas sejam avaliadas, e o Z3 encontra a solução que satisfaz todas as restrições.

- este código utiliza conceitos de execução simbólica descritos por James C. King em seu artigo seminal "Symbolic Execution and Program Testing". A execução simbólica nos permite modelar as diferentes decisões que o Caixeiro Viajante deve tomar, e o solver Z3 é usado para garantir que essas decisões respeitem as restrições do problema. Ao formular o TSP no Z3, utilizamos variáveis simbólicas para representar as cidades e os caminhos, garantindo que cada rota seja única e otimizada.

Referência: 
King, James C. "Symbolic execution and program testing." Communications of the ACM 19.7 (1976): 385-394.


