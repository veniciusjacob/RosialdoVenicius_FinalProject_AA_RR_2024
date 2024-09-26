from z3 import *
import time

def tsp_solver(distance_matrix):
    n = len(distance_matrix)  # número de cidades
    print(f"Número de cidades: {n} \n")

    x = []  # inicializa a lista x que armazenará as variáveis booleanas x[i][j]

    # Criar as variáveis de decisão booleanas x[i][j]
    for i in range(n):
        row = []
        for j in range(n):
            var = Bool(f'x[{i}][{j}]')
            row.append(var)
        x.append(row)

    solver = Optimize()

    # Restrições para x[i][j]
    for i in range(n):
        for j in range(n):
            if i == j:
                solver.add(x[i][j] == False)  # Não há arestas de um nó para ele mesmo

    # Restrição de entrada e saída única
    for i in range(n):
        sum_saida = 0
        sum_entrada = 0
        for j in range(n):
            sum_saida += If(x[i][j], 1, 0)
            sum_entrada += If(x[j][i], 1, 0)
        solver.add(sum_saida == 1)
        solver.add(sum_entrada == 1)

    # Variáveis auxiliares para evitar subciclos
    u = [Int(f'u[{i}]') for i in range(n)]  # Inclui todas as cidades, incluindo a cidade 0

    # Definir u[0] = 0
    solver.add(u[0] == 0)

    # Restringir u[i] para i != 0
    for i in range(1, n):
        solver.add(u[i] >= 1)
        solver.add(u[i] <= n - 1)

    # Restrições MTZ para eliminar subciclos
    for i in range(n):
        for j in range(n):
            if i != j and i != 0 and j != 0:
                solver.add(u[i] - u[j] + n * If(x[i][j], 1, 0) <= n - 1)

    # Função objetivo
    total_distance = 0
    for i in range(n):
        for j in range(n):
            total_distance += distance_matrix[i][j] * If(x[i][j], 1, 0)
    solver.minimize(total_distance)

    # Verificando o tempo de execução
    start_time = time.time()  # Captura o tempo inicial
    if solver.check() == sat:
        model = solver.model()
        print("Solução encontrada:")
        caminho = []
        cidade_atual = 0  # Começando da cidade 0
        caminho.append(cidade_atual)

        for _ in range(n - 1):  # Precisamos de n-1 movimentos para completar o ciclo
            for j in range(n):
                if model.evaluate(x[cidade_atual][j]):
                    caminho.append(j)
                    cidade_atual = j
                    break
        caminho.append(0)  # Retorna à cidade inicial
        print(f"Caminho completo: {caminho}")
    else:
        print('Nenhuma solução encontrada.')

    # Calculando e exibindo o tempo de execução
    end_time = time.time()  # Captura o tempo final
    execution_time = end_time - start_time
    hours, rem = divmod(execution_time, 3600)
    minutes, seconds = divmod(rem, 60)
    print(f"Tempo total de execução: {int(hours)} horas, {int(minutes)} minutos, {int(seconds)} segundos.")

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