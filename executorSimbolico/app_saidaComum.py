from z3 import *

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

