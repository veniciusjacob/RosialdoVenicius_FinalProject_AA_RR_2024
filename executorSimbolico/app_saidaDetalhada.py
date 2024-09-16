from z3 import *
from itertools import permutations

def tsp_solver(distance_matrix):
    n = len(distance_matrix)
    print(f"Número de cidades: {n} \n")

    x = []
    for i in range(n):
        row = []
        for j in range(n):
            var = Int(f'x[{i}][{j}]')
            row.append(var)
        x.append(row)

    solver = Optimize()

    # Variáveis de decisão x[i][j] binárias (0 ou 1)
    for i in range(n):
        for j in range(n):
            if i != j:
                solver.add(Or(x[i][j] == 0, x[i][j] == 1))
            else:
                solver.add(x[i][j] == 0)

    # Restrições de entrada e saída (uma entrada e uma saída por cidade)
    for i in range(n):
        sum_saida = 0
        sum_entrada = 0
        for j in range(n):
            sum_saida += x[i][j]
            sum_entrada += x[j][i]
        solver.add(sum_saida == 1)  # uma saída
        solver.add(sum_entrada == 1)  # uma entrada

    # Variáveis auxiliares para evitar subciclos
    u = [Int(f'u[{i}]') for i in range(n)]
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

        # Exibir detalhes do caminho sugerido
        exibir_resultado(distance_matrix, caminho)

    else:
        print('Nenhuma solução encontrada.')

def calcular_distancia_total(caminho, matriz_distancias):
    distancia_total = 0
    for i in range(len(caminho) - 1):
        distancia_total += matriz_distancias[caminho[i]][caminho[i+1]]
    return distancia_total

def exibir_detalhes_caminho(caminho, matriz_distancias):
    detalhes = []
    soma_total = 0
    for i in range(len(caminho) - 1):
        origem = caminho[i]
        destino = caminho[i+1]
        distancia = matriz_distancias[origem][destino]
        detalhes.append(f"{origem} → {destino}: {distancia}")
        soma_total += distancia
    detalhes.append(f"Soma total: {soma_total}")
    return detalhes, soma_total

def verificar_outros_caminhos(matriz_distancias, caminho_sugerido):
    num_cidades = len(matriz_distancias)
    todas_permutacoes = list(permutations(range(1, num_cidades)))
    
    detalhes = []
    melhor_caminho = caminho_sugerido
    menor_distancia = calcular_distancia_total(caminho_sugerido, matriz_distancias)

    for permutacao in todas_permutacoes:
        caminho = [0] + list(permutacao) + [0]
        distancia = calcular_distancia_total(caminho, matriz_distancias)
        if distancia < menor_distancia:
            menor_distancia = distancia
            melhor_caminho = caminho
        detalhes_caminho, soma = exibir_detalhes_caminho(caminho, matriz_distancias)
        detalhes_caminho_str = ' + '.join([str(matriz_distancias[caminho[i]][caminho[i+1]]) for i in range(len(caminho)-1)])
        detalhes.append(f"{caminho}: {detalhes_caminho_str} = {distancia}")
    
    return melhor_caminho, menor_distancia, detalhes

def exibir_resultado(matriz_distancias, caminho_sugerido):
    print("Caminho sugerido:", caminho_sugerido)
    detalhes_caminho, soma_total = exibir_detalhes_caminho(caminho_sugerido, matriz_distancias)
    print("Cálculo da soma das distâncias:")
    for detalhe in detalhes_caminho[:-1]:
        print(detalhe)
    detalhes_soma_total = ' + '.join([str(matriz_distancias[caminho_sugerido[i]][caminho_sugerido[i+1]]) for i in range(len(caminho_sugerido)-1)])
    print(f"Soma total: {detalhes_soma_total} = {soma_total}")
    
    print("Verificação de outros caminhos possíveis:")
    melhor_caminho, menor_distancia, detalhes_outros = verificar_outros_caminhos(matriz_distancias, caminho_sugerido)
    for detalhe in detalhes_outros:
        print(detalhe)
    
    if soma_total == menor_distancia:
        print(f"O caminho sugerido de custo {soma_total} é de fato o menor. Solução correta.")
    else:
        print(f"Existe um caminho melhor: {melhor_caminho} com custo {menor_distancia}.")


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
