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

    """
        Por que estamos criando a lista u[]?
        Esse é um truque que ajuda a resolver o problema de forma correta. O problema do Caixeiro Viajante tem que garantir que o vendedor faça apenas um grande ciclo, ou seja, visite todas as cidades uma vez e retorne ao ponto de origem, sem formar ciclos menores no caminho (os subciclos).

        As variáveis u[i] são usadas como rótulos numéricos para as cidades (exceto a primeira cidade) que nos ajudam a verificar se estamos evitando esses subciclos.
    """
    for i in range(1, n): # Esse loop começa da segunda cidade (i = 1) e vai até a última cidade (n - 1). Estamos ignorando a cidade 0 (a primeira), porque essa cidade é o ponto de partida e o ponto final, e não precisamos de um rótulo numérico para ela.

        solver.add(u[i] >= 1) # Aqui, estamos adicionando uma restrição ao solver: para todas as cidades (exceto a cidade inicial i = 0), o valor de u[i] deve ser maior ou igual a 1.

        solver.add(u[i] <= (n - 1)) # Essa linha adiciona outra restrição ao solver: para todas as cidades (exceto a cidade inicial i = 0), o valor de u[i] deve ser menor ou igual a n - 1. Isso limita os valores de u[i] para garantir que uma numeração válida, sem ultrapassar o número de cidades.

        #Esse conjunto de restrições (usando u[i]) ajuda a garantir que o solver evite subciclos. Vamos entender por que:

        '''
            Como as variáveis u[i] evitam subciclos:

            as variáveis u[i] são um truque para evitar esses subciclos

            O vendedor sai da cidade A com um "rótulo" que não é numérico, porque ele sempre começa na cidade inicial.
            Quando ele vai para a cidade B, a variável u[B] recebe o valor 1. Isso representa a "primeira parada".
            Quando ele vai para a cidade C, a variável u[C] recebe o valor 2. Isso significa que ele está progredindo na viagem.
            Se o vendedor tentasse voltar para a cidade A (fechando um ciclo parcial), isso implicaria que ele estaria diminuindo os rótulos (de 2 para 0), o que não é permitido.
            As variáveis u[i] garantem que o vendedor só pode seguir em uma ordem crescente de rótulos, ou seja, ele sempre "progride" para a próxima cidade. Isso impede que ele feche pequenos ciclos sem visitar todas as cidades.
        '''

    # for i in range(1, n): e for j in range(1, n):
    # Esses dois loops percorrem todas as cidades i e j, exceto a cidade inicial (cidade 0). Isso porque a cidade inicial não precisa das mesmas restrições de rótulo numérico que usamos nas outras cidades. 
    for i in range(1, n):
        for j in range(1, n):
            if i != j: # esse if garante que não estamos tentando adicionar uma restrição para a mesma cidade. Por exemplo, não faz sentido forçar que a cidade i vá para ela mesma (x[i][i]), então pulamos essa situação.

                solver.add(Implies(x[i][j] == 1, u[i] + 1 == u[j])) # Aqui, estamos adicionando uma restrição ao solver que diz:

                # Se x[i][j] == 1, ou seja, se existe uma rota do ponto i para o ponto j,
                # Então u[j] deve ser igual a u[i] + 1

            """
                O que isso significa:

                As variáveis u[i] e u[j] são rótulos numéricos que representam a ordem em que o vendedor visita as cidades.

                u[i] + 1 == u[j] garante que, se o vendedor vai de uma cidade i para a cidade j, então o número de rótulo da cidade j (ou seja, o rótulo de onde ele vai) será um a mais do que o da cidade i.

                isso significa que, para cada cidade que o vendedor visita, o rótulo aumenta de maneira progressiva. Assim, se ele começa em uma cidade i, a próxima cidade j que ele visita terá o rótulo imediatamente maior, garantindo que ele está avançando no percurso sem voltar para cidades já visitadas.

                Exemplo:
                Suponha que temos 3 cidades: A, B e C. O vendedor segue o seguinte caminho:

                Ele vai de A para B: x[0][1] == 1
                Isso significa que u[1] = u[0] + 1. Se u[A] = 0, então u[B] = 1.
                Depois ele vai de B para C: x[1][2] == 1
                Isso significa que u[2] = u[1] + 1, ou seja, se u[B] = 1, então u[C] = 2.
            """

    #restrição para garantir que não haja subciclos

    #esses dois loops percorrem todas as cidades i e j, exceto a cidade inicial
    for i in range(1, n):
        for j in range(1, n): 
            if i != j: # Esse if garante que estamos verificando apenas pares de cidades diferentes, para evitar cidades que "saem" e "chegam" nelas mesmas.
                solver.add(Implies(x[i][j] == 1, u[i] != u[j])) # adicionando outra restrição ao solver que diz:
                # Se x[i][j] == 1, ou seja, se existe uma rota do ponto i para o ponto j,
                # Então u[i] deve ser diferente de u[j].

                """ 
                    O que isso significa:
                    Essa linha de código garante que as variáveis de rótulo u[i] e u[j] nunca podem ser iguais, o que significa que o vendedor não pode voltar para a mesma cidade com o mesmo rótulo.

                    Se u[i] == u[j], isso indicaria que o vendedor está fazendo um ciclo interno (subciclo), porque ele está visitando i e j de tal forma que ele volta ao mesmo estado anterior. Ao forçar que os rótulos sejam diferentes, garantimos que o vendedor continue avançando no caminho e não forme subciclos.

                    Exemplo

                    Suponha que o vendedor siga o seguinte caminho:

                    A → B → A

                    Se não adicionássemos a restrição u[i] != u[j], o solver poderia permitir que o vendedor fosse de A para B e depois voltasse para A sem visitar mais nenhuma cidade, formando um ciclo menor e ignorando as outras cidades.

                    Com essa restrição, o solver vai impedir esse comportamento porque, se x[0][1] == 1 e depois x[1][0] == 1, ele verificaria que u[0] == u[1], o que é inválido. Dessa forma, o solver evita subciclos.

                """
    # Função objetivo: A função objetivo define o que estamos tentando minimizar no problema. No caso do Caixeiro Viajante, o objetivo é minimizar a soma das distâncias percorridas ao visitar todas as cidades.
    objective = Int('objective') #  cria uma variável chamada objective, que será usada para armazenar o valor total da função objetivo — ou seja, o total das distâncias percorridas no caminho.
    objective_expr = 0 # Iniciamos a expressão da função objetivo com valor 0. Este valor vai aumentar à medida que somamos as distâncias entre as cidades.
    for i in range(n): #Esses dois loops percorrem todas as cidades possíveis i e j (todas as combinações de ida de uma cidade para outra).
        for j in range(n):
            objective_expr += distance_matrix[i][j] * x[i][j] # Aqui, estamos somando as distâncias percorridas no caminho.

            """
                distance_matrix[i][j] contém a distância entre a cidade i e a cidade j.

                x[i][j] é a variável de decisão que indica se o vendedor vai de i para j. Se x[i][j] == 1, significa que o vendedor realmente fez essa viagem.

                Portanto, para cada par de cidades, multiplicamos a distância entre elas (distance_matrix[i][j]) pelo valor de x[i][j]. Isso só adiciona a distância à soma total se o vendedor de fato foi de i para j (ou seja, se x[i][j] == 1).
            """
    solver.add(objective == objective_expr) # Aqui, estamos informando ao solver que a variável objective é igual à soma total das distâncias percorridas, que foi acumulada em objective_expr.
    solver.minimize(objective) # Essa linha instrui o solver a minimizar o valor da variável objective. Em outras palavras, estamos pedindo ao solver para encontrar o caminho que minimize a distância total percorrida.

    #Verificando a Solução
    if solver.check() == sat: # ssa linha verifica se o solver encontrou uma solução satisfatória
        model = solver.model() # Se uma solução foi encontrada, essa linha extrai o modelo da solução, que contém os valores de todas as variáveis que satisfazem as restrições. Ou seja, ele nos dá as rotas x[i][j] que o vendedor deve seguir para minimizar a distância.

        print("Solução encontrada:")
        caminho = []
        cidade_atual = 0  # Começando da cidade 0
        caminho.append(cidade_atual)

        for i in range(n - 1):  # Precisamos de n-1 movimentos para completar o ciclo
            for j in range(n):
                if model.evaluate(x[cidade_atual][j]) == 1: # Aqui, verificamos se no modelo de solução gerado pelo solver, x[cidade_atual][j] == 1. Isso significa que o vendedor foi da cidade cidade_atual para a cidade j. Se sim:

                

                    caminho.append(j) #Adicionamos a cidade j ao caminho
                    cidade_atual = j # Atualizamos a variável cidade_atual para j, para continuar o processo a partir da nova cidade.
                    break # para sair do loop, porque já encontramos a próxima cidade.
        caminho.append(0)  # Depois de visitar todas as cidades, o vendedor deve voltar para a cidade inicial. Essa linha adiciona a cidade 0 novamente ao caminho, completando o ciclo.
        print(f"Caminho completo: {caminho}")
    else:
        print('Nenhuma solução encontrada.')

# Teste com diferentes matrizes de distâncias

# Teste 1: Caso Simples (3 cidades)
distance_matrix_test_1 = [
    [0, 1, 1],
    [1, 0, 1],
    [1, 1, 0]
]
print("Teste 1:")
tsp_solver(distance_matrix_test_1)
print()

# Teste 2: Distâncias Variadas (4 cidades)
distance_matrix_test_2 = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]
print("Teste 2:")
tsp_solver(distance_matrix_test_2)
print()

# Teste 3: Assimetrias no Caminho (4 cidades)
distance_matrix_test_3 = [
    [0, 2, 9, 10],
    [1, 0, 6, 4],
    [15, 7, 0, 8],
    [6, 3, 12, 0]
]
print("Teste 3:")
tsp_solver(distance_matrix_test_3)
print()

# Teste 4: Caminhos Longos e Curtos (4 cidades)
distance_matrix_test_4 = [
    [0, 100, 150, 200],
    [100, 0, 120, 80],
    [150, 120, 0, 90],
    [200, 80, 90, 0]
]
print("Teste 4:")
tsp_solver(distance_matrix_test_4)
print()

# Teste 5: Matriz com Cidades Muito Próximas (5 cidades)
distance_matrix_test_5 = [
    [0, 2, 3, 4, 5],
    [2, 0, 2, 3, 4],
    [3, 2, 0, 2, 3],
    [4, 3, 2, 0, 2],
    [5, 4, 3, 2, 0]
]
print("Teste 5:")
tsp_solver(distance_matrix_test_5)
print()

# Teste 6: Grande Desigualdade nas Distâncias (5 cidades)
distance_matrix_test_6 = [
    [0, 5, 100, 100, 100],
    [5, 0, 10, 10, 10],
    [100, 10, 0, 5, 5],
    [100, 10, 5, 0, 1],
    [100, 10, 5, 1, 0]
]
print("Teste 6:")
tsp_solver(distance_matrix_test_6)
print()

# Teste 7: Distâncias Aleatórias (6 cidades)
distance_matrix_test_7 = [
    [0, 10, 15, 20, 5, 25],
    [10, 0, 35, 25, 30, 20],
    [15, 35, 0, 30, 10, 50],
    [20, 25, 30, 0, 15, 40],
    [5, 30, 10, 15, 0, 45],
    [25, 20, 50, 40, 45, 0]
]
print("Teste 7:")
tsp_solver(distance_matrix_test_7)
print()

# Teste 8: Matriz Grande com Simetria (8 cidades)
distance_matrix_test_8 = [
    [0, 2, 3, 4, 5, 6, 7, 8],
    [2, 0, 2, 3, 4, 5, 6, 7],
    [3, 2, 0, 2, 3, 4, 5, 6],
    [4, 3, 2, 0, 2, 3, 4, 5],
    [5, 4, 3, 2, 0, 2, 3, 4],
    [6, 5, 4, 3, 2, 0, 2, 3],
    [7, 6, 5, 4, 3, 2, 0, 2],
    [8, 7, 6, 5, 4, 3, 2, 0]
]
print("Teste 8:")
tsp_solver(distance_matrix_test_8)

