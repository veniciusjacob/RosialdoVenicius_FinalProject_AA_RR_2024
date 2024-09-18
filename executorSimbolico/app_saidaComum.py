"""
Este código utiliza conceitos de execução simbólica descritos por James C. King em seu artigo seminal "Symbolic Execution and Program Testing". A execução simbólica nos permite modelar as diferentes decisões que o Caixeiro Viajante deve tomar, e o solver Z3 é usado para garantir que essas decisões respeitem as restrições do problema. Ao formular o TSP no Z3, utilizamos variáveis simbólicas para representar as cidades e os caminhos, garantindo que cada rota seja única e otimizada.

Referência: 
King, James C. "Symbolic execution and program testing." Communications of the ACM 19.7 (1976): 385-394.
"""

from z3 import *

def tsp_solver(distance_matrix):
    n = len(distance_matrix) #número de cidades 
    print(f"Número de cidades: {n} \n")

    x = [] # inicializa uma lista x que armazenará as variáveis inteiras que representarão se um caminho entre duas cidades é escolhido ou não.

    # O objetivo desta parte do código é criar uma matriz de variáveis de decisão. Essas variáveis representam se há ou não um caminho entre duas cidades

    for i in range(n): #Esse loop externo percorre cada cidade, onde i representa a cidade de origem.

        row = [] #Essa lista armazena as variáveis que representam os possíveis caminhos saindo da cidade i, para cada linha.

        for j in range(n): # percorre todas as cidades de destino, representadas por j. Assim, para cada cidade de origem i, estamos considerando todos os possíveis destinos j.

            var = Int(f'x[{i}][{j}]')  #Cria as variáveis inteira simbolicas usando o Z3 com o nome x_i_j, onde i e j representam as cidades de origem e destino. Essa variável representa a existência de um caminho da cidade i para a cidade j.
           
            row.append(var)#Após preencher a lista row com todas as variáveis de decisão para os caminhos saindo da cidade i, essa lista é adicionada à matriz x. Essa matriz x acaba sendo uma lista de listas (ou matriz) onde cada sublista row contém as variáveis para uma cidade específica.

        x.append(row) #No final do processo, x será uma matriz n x n onde cada elemento x[i][j] é uma variável que indica se o caminho da cidade i para a cidade j é parte da solução. O que temos nessa matriz são variáveis simbólicas, Essas variáveis não têm um valor

    #DESCOMENTAR PARA OBSERVAR A MATRIZ X
    # print("Matrix X de variáves simbólicas formada: ")
    # for matrizX in x:
    #     print(matrizX)

    solver = Optimize() #instancia de optimize,  que é utilizado para resolver problemas de otimização. Ao contrário de um solver simples que busca apenas encontrar uma solução que satisfaça as restrições, o Optimize permite também minimizar ou maximizar uma função objetivo. 

    # Adição das restrições: x[i][j] deve ser 0 ou 1, ou seja, para cada par de cidade i e j, a variavel x[i][j] deve ser 0 ou 1    

    for i in range(n):
        for j in range(n):
            if i != j: #verificamos se i e j são cidades diferentes. Isso porque não faz sentido viajar de uma cidade para ela mesma.

                solver.add(Or(x[i][j] == 0, x[i][j] == 1)) # Se i for diferente de j, adicionamos uma restrição ao solver. Essa restrição diz que a variável x[i][j] só pode ser 0 ou 1, ou seja, ou viajamos (1) ou não viajamos (0) de i para j.

            else: # Se i == j(ou seja, se estamos falando da mesma cidade)
                
                solver.add(x[i][j] == 0) #, adicionamos uma restrição dizendo que x[i][i] deve ser 0, porque não faz sentido viajar de uma cidade para ela mesma.

    # Restrição que garante uma única entrada e saída (uma entrada e uma saída por cidade)
    for i in range(n):

        # Criamos duas variáveis para contar quantas rotas saem de i e quantas chegam em i        
        sum_saida = 0
        sum_entrada = 0

        #loop sobre todas as cidades j.
        for j in range(n):

            sum_saida += x[i][j] # essa linha vai somar todas as rotas que saem da cidade i para todas as outras cidades j.
            sum_entrada += x[j][i] # Essa linha faz a soma de todas as rotas que entram na cidade i vindas de qualquer outra cidade j.
        solver.add(sum_saida == 1)  # Essa linha adiciona a restrição de que só pode haver uma rota saindo da cidade i. Ou seja, sum_saida deve ser exatamente igual a 1, o que impede que duas rotas saiam da mesma cidade.
        solver.add(sum_entrada == 1)  # De forma similar, essa linha garante que só uma rota entra na cidade i, ou seja, o vendedor só chega na cidade uma vez.

        """
            Se, por alguma razão, o solver tentasse permitir duas rotas saindo da mesma cidade, como:

            x[0][1] = 1 (A → B)
            x[0][2] = 1 (A → C)i

            Então, a soma sum_saida para a Cidade A seria:

            sum_saida = x[0][1] + x[0][2] = 1 + 1 = 2

            E isso violaria a restrição solver.add(sum_saida == 1), porque o solver está sendo forçado a garantir que sum_saida seja igual a 1.
        """

    # Variáveis auxiliares para evitar subciclos
    u = [Int(f'u[{i}]') for i in range(n)] # Aqui, estamos criando uma lista chamada u de variáveis inteiras (Int), com o mesmo tamanho do número de cidades n.
    # Cada cidade vai receber uma variável u[i], que será usada para ajudar a evitar subciclos. Subciclos são pequenos ciclos dentro do grande ciclo do Caixeiro Viajante que fariam o vendedor repetir cidades, o que não pode acontecer.
    for i in range(1, n):
        solver.add(u[i] >= 1)
        solver.add(u[i] <= n - 1)

    # Restrições de subtour elimination: se x[i][j] == 1, então u[i] + 1 == u[j]
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                solver.add(Implies(x[i][j] == 1, u[i] + 1 == u[j]))

    # Adicionando restrição para garantir que não haja subciclos
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                solver.add(Implies(x[i][j] == 1, u[i] != u[j]))

    # Função objetivo: minimizar a soma das distâncias percorridas
    objective = Int('objective')
    objective_expr = 0
    for i in range(n):
        for j in range(n):
            objective_expr += distance_matrix[i][j] * x[i][j]
    solver.add(objective == objective_expr)
    solver.minimize(objective)

    #Verificando a Solução
    if solver.check() == sat:
        model = solver.model()

        print("Solução encontrada:")
        caminho = []
        cidade_atual = 0  # Começando da cidade 0
        caminho.append(cidade_atual)

        for i in range(n - 1):  # Precisamos de n-1 movimentos para completar o ciclo
            for j in range(n):
                if model.evaluate(x[cidade_atual][j]) == 1:
                    caminho.append(j)
                    cidade_atual = j
                    break
        caminho.append(0)  # Volta para a cidade inicial
        print(f"Caminho completo: {caminho}")
    else:
        print('Nenhuma solução encontrada.')

# Teste com diferentes matrizes de distâncias

# Teste 1: Caso Simples (3 cidades)
# distance_matrix_test_1 = [
#     [0, 1, 1],
#     [1, 0, 1],
#     [1, 1, 0]
# ]
# print("Teste 1:")
# tsp_solver(distance_matrix_test_1)
# print()

# # Teste 2: Distâncias Variadas (4 cidades)
# distance_matrix_test_2 = [
#     [0, 10, 15, 20],
#     [10, 0, 35, 25],
#     [15, 35, 0, 30],
#     [20, 25, 30, 0]
# ]
# print("Teste 2:")
# tsp_solver(distance_matrix_test_2)
# print()

# # Teste 3: Assimetrias no Caminho (4 cidades)
# distance_matrix_test_3 = [
#     [0, 2, 9, 10],
#     [1, 0, 6, 4],
#     [15, 7, 0, 8],
#     [6, 3, 12, 0]
# ]
# print("Teste 3:")
# tsp_solver(distance_matrix_test_3)
# print()

# # Teste 4: Caminhos Longos e Curtos (4 cidades)
# distance_matrix_test_4 = [
#     [0, 100, 150, 200],
#     [100, 0, 120, 80],
#     [150, 120, 0, 90],
#     [200, 80, 90, 0]
# ]
# print("Teste 4:")
# tsp_solver(distance_matrix_test_4)
# print()

# # Teste 5: Matriz com Cidades Muito Próximas (5 cidades)
# distance_matrix_test_5 = [
#     [0, 2, 3, 4, 5],
#     [2, 0, 2, 3, 4],
#     [3, 2, 0, 2, 3],
#     [4, 3, 2, 0, 2],
#     [5, 4, 3, 2, 0]
# ]
# print("Teste 5:")
# tsp_solver(distance_matrix_test_5)
# print()

# # Teste 6: Grande Desigualdade nas Distâncias (5 cidades)
# distance_matrix_test_6 = [
#     [0, 5, 100, 100, 100],
#     [5, 0, 10, 10, 10],
#     [100, 10, 0, 5, 5],
#     [100, 10, 5, 0, 1],
#     [100, 10, 5, 1, 0]
# ]
# print("Teste 6:")
# tsp_solver(distance_matrix_test_6)
# print()

# # Teste 7: Distâncias Aleatórias (6 cidades)
# distance_matrix_test_7 = [
#     [0, 10, 15, 20, 5, 25],
#     [10, 0, 35, 25, 30, 20],
#     [15, 35, 0, 30, 10, 50],
#     [20, 25, 30, 0, 15, 40],
#     [5, 30, 10, 15, 0, 45],
#     [25, 20, 50, 40, 45, 0]
# ]
# print("Teste 7:")
# tsp_solver(distance_matrix_test_7)
# print()

# # Teste 8: Matriz Grande com Simetria (8 cidades)
# distance_matrix_test_8 = [
#     [0, 2, 3, 4, 5, 6, 7, 8],
#     [2, 0, 2, 3, 4, 5, 6, 7],
#     [3, 2, 0, 2, 3, 4, 5, 6],
#     [4, 3, 2, 0, 2, 3, 4, 5],
#     [5, 4, 3, 2, 0, 2, 3, 4],
#     [6, 5, 4, 3, 2, 0, 2, 3],
#     [7, 6, 5, 4, 3, 2, 0, 2],
#     [8, 7, 6, 5, 4, 3, 2, 0]
# ]
# print("Teste 8:")
# tsp_solver(distance_matrix_test_8)





