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

    #O objetivo desta parte do código é criar uma matriz de variáveis de decisão. Essas variáveis representam se há ou não um caminho entre duas cidades
    for i in range(n): #Esse loop externo percorre cada cidade, onde i representa a cidade de origem.
        row = [] #Essa lista armazena as variáveis que representam os possíveis caminhos saindo da cidade i.
        for j in range(n): # percorre todas as cidades de destino, representadas por j. Assim, para cada cidade de origem i, estamos considerando todos os possíveis destinos j.
            var = Int(f'x[{i}][{j}]') #Cria as variáveis inteira simbolicas usando o Z3 com o nome x_i_j, onde i e j representam as cidades de origem e destino. Essa variável representa a existência de um caminho da cidade i para a cidade j.
            #Essas variáveis são do tipo inteiro, mas mais tarde serão restritas para assumir apenas os valores 0 ou 1, representando a decisão de incluir ou não o caminho na solução.
            row.append(var) #Após preencher a lista row com todas as variáveis de decisão para os caminhos saindo da cidade i, essa lista é adicionada à matriz x. Essa matriz x acaba sendo uma lista de listas (ou matriz) onde cada sublista row contém as variáveis para uma cidade específica.
            #print(row)

        #No final do processo, x será uma matriz n x n onde cada elemento x[i][j] é uma variável que indica se o caminho da cidade i para a cidade j é parte da solução. O que temos nessa matriz são variáveis simbólicas, Essas variáveis não têm um valor
        x.append(row)

    print("Matrix X de variáves simbólicas formada: ")
    for matrizX in x:
        print(matrizX)
    
    solver = Optimize() #instancia de optimize,  que é utilizado para resolver problemas de otimização. Ao contrário de um solver simples que busca apenas encontrar uma solução que satisfaça as restrições, o Optimize permite também minimizar ou maximizar uma função objetivo. 

    # Restrição: x[i][j] deve ser 0 ou 1
    #x[i][j] só é um nome, e o Z3 ainda não sabe o valor que ela vai ter.
    for i in range(n):
        for j in range(n):
            if i != j:
                solver.add(Or(x[i][j] == 0, x[i][j] == 1)) #adiciona a restrição ao solver
                #Esse comando está dizendo ao Z3: "A variável x[i][j] só pode assumir dois valores, ou ela será igual a 0, ou ela será igual a 1."
                #Aqui estamos impondo uma restrição. 
                # Ainda não estamos dizendo ao Z3 o valor exato de x[i][j] (se é 0 ou 1), mas estamos limitando as opções a apenas essas duas.
                #Antes da Restrição: Antes dessa linha, x[i][j] é uma variável simbólica que pode ter qualquer valor inteiro.
                #Depois da Restrição: Após adicionar essa restrição, o solver Z3 é informado que x[i][j] deve ser 0 ou 1. Isso limita os valores possíveis para essa variável e ajuda a definir o espaço de busca para encontrar uma solução.
            else:
                solver.add(x[i][j] == 0 ) # x[i][i] deve ser 0

    #O objetivo desse bloco de código é garantir que cada cidade seja visitada exatamente uma vez e que haja exatamente um caminho de saída e um caminho de entrada para cada cidade.
    for i in range(n):
        saidas = [] #Aqui, criamos uma lista vazia chamada saidas. Essa lista será usada para armazenar todas as variáveis x[i][j] que representam caminhos saindo da cidade i para qualquer outra cidade j.
        entradas = [] # De forma semelhante, criamos outra lista vazia chamada entradas. Esta lista será usada para armazenar todas as variáveis x[j][i] que representam caminhos entrando na cidade i a partir de qualquer outra cidade j.

        for j in range(n):  #Esse é um loop interno que percorre todas as cidades j. A variável j representa outra cidade, e o loop considera todas as possíveis cidades de destino para as variáveis de decisão x[i][j] e x[j][i].

            #quando i = 0
            saidas.append(x[i][j]) #x[0][0], x[0][1], x[0][2], x[0][3] -> saindo da cidade 0 para 0, saindo da cidade 0 para 1 ...
            entradas.append(x[j][i]) #x[0][0], x[1][0], x[2][0], x[3],[0] -> saindo da cidade 0 entrando em 0, saindo da cidade 1 entrando em 0, saindo de 2 e entrando em 0

            #Resumo: todas cidades que saem de 0 e todas cidades que entram em 0 
        
        print(f"saidas {i}: {saidas}")
        print(f"entradas {i}: {entradas}")

        solver.add(Sum(saidas) == 1) #adiciona ao solver uma restrição que garante que a soma das variáveis na lista saidas seja igual a 1. Isso significa que a cidade i deve ter exatamente um caminho de saída, ou seja, deve sair exatamente uma vez para outra cidade
        solver.add(Sum(entradas) == 1) #garante que a cidade i seja visitada exatamente uma vez por outra cidade.

    #criação da função objetiva
    objective = 0 #criação da função objetivo que é a soma das distâncias percorridas, começamos com o valor 0. À medida que percorremos as cidades no loop, vamos acumulando as distâncias na variável objective

    # o laço externo que percorre todas as cidades i, que representam as cidades de partida.
    for i in range(n):
        # Para cada cidade i, o código vai verificar a distância para todas as outras cidades j. O laço se repete n vezes, onde n é o número de cidades.
        for j in range(n):
            objective = objective + distance_matrix[i][j] * x[i][j]
            #distance_matrix[i][j]: Pega a distância entre a cidade i e a cidade j da matriz de distâncias fornecida.
            #x[i][j]: Pega a variável binária que indica se o caminho i -> j foi utilizado ou não (1 se foi, 0 se não foi).

            #Como funciona: Se x[i][j] == 1 (ou seja, se o caminho entre as cidades i e j for utilizado), então o termo distance_matrix[i][j] * x[i][j] será a distância real entre i e j, que será adicionada à função objetivo.

            #Se x[i][j] == 0, significa que o caminho i -> j não é utilizado, então distance_matrix[i][j] * 0 será igual a 0, e nada será adicionado à função objetivo.
    solver.minimize(objective) #O método minimize() é uma função do solver Z3 que é usada para especificar que uma determinada expressão (função objetivo) deve ser minimizada. Em outras palavras, você está pedindo ao solver para encontrar uma solução que faça com que o valor da expressão dada seja o menor possível, enquanto satisfazendo todas as restrições impostas.

    #Resultado: Após a busca, o solver retorna uma solução que é, de acordo com as restrições, a que minimiza a função objetivo. Se a função objetivo estiver expressa de forma a representar um custo ou distância, a solução encontrada será a que resulta no menor custo ou distância.

    if solver.check() == sat: #check() verifica se as restrições são satisfazível
        model = solver.model() #retorna um conjunto de valores específicos para as variáveis que satisfazem as restrições

        print("solução encontrada: ")
        # Imprimir os valores das variáveis
        for i in range(n):
            for j in range(n):
                # Avalia o valor da variável x[i][j] no modelo
                value = model.evaluate(x[i][j])
                print(f'Valor de x[{i}][{j}] é: {value}')


        #percorre todas as variáveis x[i][j] que representam se há um caminho entre a cidade i e a cidade j
        print("\nCaminhos incluídos na solução:")
        for i in range(n):
            for j in range(n):
                #Verificação: Se o valor da variável é 1, significa que o caminho entre as cidades i e j faz parte da solução.
                #O método evaluate() é uma função fornecida pelo Z3 que é usada para obter o valor de uma expressão ou variável no modelo de solução encontrado pelo solver.
                #Quando você resolve um problema com o Z3, o solver encontra um modelo de solução que satisfaz todas as restrições definidas. Esse modelo é uma atribuição dos valores das variáveis que resolve o problema.
                #O método evaluate() é utilizado para consultar esse modelo e obter o valor específico de uma variável ou expressão no contexto da solução encontrada.
                #Após chamar solver.check() e verificar que uma solução foi encontrada (ou seja, o resultado foi sat), você pode usar evaluate() para obter os valores das variáveis no modelo que representa a solução.

                if model.evaluate(x[i][j]) == 1: 
                    print(f'Caminho de {i} para {j}')
    else:
        print('Nenhuma solução encontrada.')


distance_matrix = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

distance_matrix_test_1 = [
    [0, 1, 2],
    [1, 0, 1],
    [2, 1, 0]
]

distance_matrix_test_2 = [
    [0, 10, 15],
    [10, 0, 35],
    [15, 35, 0]
]

distance_matrix_test_3 = [
    [0, 2, 9, 10],
    [1, 0, 6, 4],
    [15, 7, 0, 8],
    [6, 3, 12, 0]
]

distance_matrix_test_4 = [
    [0, 100, 150, 200],
    [100, 0, 120, 80],
    [150, 120, 0, 90],
    [200, 80, 90, 0]
]


print("Teste 1:")
tsp_solver(distance_matrix_test_1)

print("\nTeste 2:")
tsp_solver(distance_matrix_test_2)

print("\nTeste 3:")
tsp_solver(distance_matrix_test_3)

print("\nTeste 4:")
tsp_solver(distance_matrix_test_4)

