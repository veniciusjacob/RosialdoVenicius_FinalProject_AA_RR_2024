from z3 import *  # Importa todos os módulos da biblioteca Z3

def tsp_solver(distance_matrix):
    """
    Função para resolver o problema do Caixeiro Viajante usando Z3 Optimize.
    :param distance_matrix: Lista de listas representando a matriz de distâncias entre cidades.
    """

    n = len(distance_matrix)  # Número de cidades (tamanho da matriz)

    # Inicializa uma lista vazia para armazenar as listas de variáveis
    x = []

    # Loop para as linhas
    for i in range(n):
        # Inicializa uma lista para armazenar as variáveis da linha atual
        row = []
        # Loop interno para as colunas
        for j in range(n):
            # Cria a variável inteira usando Z3 com um nome único baseado nos índices i e j
            var = Int(f'x_{i}_{j}')
            row.append(var)
        # Adiciona a lista da linha atual à matriz x
        x.append(row)

    # Inicializando o objeto Optimize
    solver = Optimize()  # Substitui Solver() por Optimize()

    # Restrições de variáveis: cada variável deve ser 0 ou 1
    for i in range(n):
        for j in range(n):
            solver.add(Or(x[i][j] == 0, x[i][j] == 1))  # Restrição: x[i][j] deve ser 0 ou 1

    # Restrições para garantir que cada cidade seja visitada uma vez
    for i in range(n):
        # Listas para armazenar as variáveis de saída e entrada para a cidade 'i'
        saidas = []
        entradas = []
        
        # Loop para coletar as variáveis de saída e entrada para a cidade 'i'
        for j in range(n):
            # Variável que representa a cidade 'i' saindo para a cidade 'j'
            saidas.append(x[i][j])
            
            # Variável que representa a cidade 'j' entrando na cidade 'i'
            entradas.append(x[j][i])
        
        # Adiciona a restrição de que a cidade 'i' deve sair exatamente uma vez
        solver.add(Sum(saidas) == 1)
        
        # Adiciona a restrição de que a cidade 'i' deve ser entrada exatamente uma vez
        solver.add(Sum(entradas) == 1)

    # Função objetivo: minimizar a distância total percorrida
    objective = Sum([distance_matrix[i][j] * x[i][j] for i in range(n) for j in range(n)])
    solver.minimize(objective)  # Configura o solver para minimizar a função objetivo

    # Resolvendo o problema com o solver
    if solver.check() == sat:  # Verifica se existe uma solução que é satisfatível
        model = solver.model()  # Obtém o modelo da solução
        print("Solução encontrada:")
        for i in range(n):
            for j in range(n):
                if model.evaluate(x[i][j]) == 1:  # Verifica se o caminho i->j faz parte da solução
                    print(f'Caminho de {i} para {j}')  # Imprime o caminho incluído na solução
    else:
        print("Nenhuma solução encontrada.")  # Caso o solver não encontre uma solução



# Exemplo de uso da função tsp_solver com a matriz de distância fornecida
distance_matrix = [
    [0, 10, 15, 20],
    [10, 0, 35, 25],
    [15, 35, 0, 30],
    [20, 25, 30, 0]
]

# Chama a função com a matriz de distância definida
tsp_solver(distance_matrix)
