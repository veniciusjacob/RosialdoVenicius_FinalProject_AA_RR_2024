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


distance_matrix_test_20 = [
    [0, 24, 16, 32, 10, 25, 38, 43, 18, 27, 14, 41, 35, 22, 39, 47, 15, 30, 42, 19],
    [24, 0, 20, 12, 30, 28, 31, 11, 33, 40, 29, 38, 21, 27, 23, 10, 39, 44, 17, 36],
    [16, 20, 0, 25, 12, 39, 18, 21, 34, 15, 36, 45, 19, 23, 14, 33, 42, 29, 48, 22],
    [32, 12, 25, 0, 45, 17, 22, 30, 19, 28, 24, 41, 15, 14, 40, 27, 26, 13, 44, 32],
    [10, 30, 12, 45, 0, 26, 38, 20, 48, 23, 31, 39, 22, 14, 20, 17, 21, 10, 34, 46],
    [25, 28, 39, 17, 26, 0, 29, 11, 19, 38, 10, 16, 35, 27, 23, 45, 20, 30, 24, 34],
    [38, 31, 18, 22, 38, 29, 0, 42, 10, 45, 36, 24, 22, 30, 11, 40, 20, 48, 39, 23],
    [43, 11, 21, 30, 20, 11, 42, 0, 50, 13, 36, 25, 12, 32, 17, 19, 29, 35, 22, 30],
    [18, 33, 34, 19, 48, 19, 10, 50, 0, 29, 27, 43, 36, 23, 41, 33, 15, 40, 22, 11],
    [27, 40, 15, 28, 23, 38, 45, 13, 29, 0, 20, 14, 35, 30, 19, 11, 16, 32, 28, 43],
    [14, 29, 36, 24, 31, 10, 36, 36, 27, 20, 0, 12, 28, 19, 21, 30, 39, 22, 18, 25],
    [41, 38, 45, 41, 39, 16, 24, 25, 43, 14, 12, 0, 35, 22, 31, 19, 20, 37, 21, 24],
    [35, 21, 19, 15, 22, 35, 22, 12, 36, 35, 28, 35, 0, 30, 48, 42, 25, 38, 16, 30],
    [22, 27, 23, 14, 14, 27, 30, 32, 23, 30, 19, 22, 30, 0, 45, 40, 33, 10, 50, 31],
    [39, 23, 14, 40, 20, 23, 11, 17, 41, 19, 21, 31, 48, 45, 0, 10, 15, 34, 27, 19],
    [47, 10, 33, 27, 17, 45, 40, 19, 33, 11, 30, 19, 42, 40, 10, 0, 20, 29, 44, 38],
    [15, 39, 42, 26, 21, 20, 20, 29, 15, 16, 39, 20, 25, 33, 15, 20, 0, 45, 36, 50],
    [30, 44, 29, 13, 10, 30, 48, 35, 40, 32, 22, 37, 38, 10, 34, 29, 45, 0, 19, 15],
    [42, 17, 48, 44, 34, 24, 39, 22, 22, 28, 18, 21, 16, 50, 27, 44, 36, 19, 0, 12],
    [19, 36, 22, 32, 46, 34, 23, 30, 11, 43, 25, 24, 30, 31, 19, 38, 50, 15, 12, 0]
]
print("Teste 20:")
tsp_solver(distance_matrix_test_20)
