import math

# Calcula a distância de acordo com a formula correta do arquivo
def distancia(p1, p2, att):
    if att:
        xd = p1[0]-p2[0]
        yd = p1[1]-p2[1]
        r = math.sqrt((xd*xd + yd*yd)/10.0)
        t = int(round(r))
        if t < r:
            return t+1
        else:
            return t 
    else:
        xd = p1[0]-p2[0]
        yd = p1[1]-p2[1]
        return int(round(math.sqrt(xd*xd + yd*yd)))

# Função de busca do union find (usado pelo Kruskal)
def unionFindBusca(pai, i):
    if pai[i] == i:
        return i
    return unionFindBusca(pai, pai[i])
 
 # Função de união do union find (usado pelo Kruskal)
def unionFindUne(pai, rank, x, y):
    raizX = unionFindBusca(pai, x)
    raizY = unionFindBusca(pai, y)
    if rank[raizX] < rank[raizY]:
        pai[raizX] = raizY
    elif rank[raizX] > rank[raizY]:
        pai[raizY] = raizX
    else:
        pai[raizY] = raizX
        rank[raizX] += 1
        
# Algoritmo de kruskal para calcular a MST do grafo com base na lista de arestas
def kruskalMst(listaArestas, numeroVertices):
    resultado = []
    it = 0
    # Ordena a lista de arestas de forma crescente pelo peso da aresta
    listaArestas = sorted(listaArestas, key=lambda item: item[2])
    pai = []
    rank = []
    for no in range(numeroVertices):
        pai.append(no)
        rank.append(0)
    while len(resultado) < numeroVertices-1:
        x, y, peso = listaArestas[it]
        it+= 1
        conjuntoX = unionFindBusca(pai, x)
        conjuntoY = unionFindBusca(pai, y)
        if conjuntoX != conjuntoY:
            resultado.append([x, y, peso])
            unionFindUne(pai, rank, conjuntoX, conjuntoY)
    return resultado

def matchingMinimo(matrizDistancia, verticesImpares):
    # Usa a biblioteca networkx para encontrar o matching mínimo no subgrafo
    import networkx as nx
    # Constrói o grafo no formato da biblioteca
    G = nx.Graph()
    for v in verticesImpares:
        for j in verticesImpares:
            if v != j:
                G.add_edge(v, j, weight=matrizDistancia[v][j])
    # Executa o matching
    # Procura o matching de cardinalidade máxima
    return nx.algorithms.matching.min_weight_matching(G, True)
    

# Encontra um ciclo euleriano no multigrafo
def encontraCicloEuleriano(arestasCombinacao, matrizDistancia):
    # Usa a biblioteca networkx para encontrar o ciclo euleriano no multigrafo
    import networkx as nx
    # Constrói o multigrafo no formato da biblioteca
    G = nx.MultiGraph()
    for v1, v2, peso in arestasCombinacao:
        G.add_edge(v1, v2, weight=peso)
    arestasCiclo = list(nx.eulerian_circuit(G))
    # Cria a lista dos vértices visitados
    verticesVisitados = [arestasCiclo[0][0]]
    for v1, v2 in arestasCiclo:
        verticesVisitados.append(v2)
    return verticesVisitados

# Encontra os vértices de grau impar na mst
def encontrarVerticesGrauImpar(mst, numeroVertices):
    grauVertices = [0]*numeroVertices
    verticesImpares = []
    for aresta in mst:
        grauVertices[aresta[0]] += 1
        grauVertices[aresta[1]] += 1

    for vertice in range(numeroVertices):
        if grauVertices[vertice] % 2 == 1:
            verticesImpares.append(vertice)

    return verticesImpares

def calcularHeuristica(coordenadas, att):
    # Calcula a matriz de distâncias do grafo e a lista de arestas
    matrizDistancias = []
    listaArestas = []
    for i in range(len(coordenadas)):
        temp = []
        for j in range(len(coordenadas)):
            if i == j:
                temp.append(0)
            else:
                temp.append(distancia(coordenadas[i], coordenadas[j], att))
            if j > i:
                listaArestas.append((i, j, distancia(coordenadas[i], coordenadas[j], att)))
        matrizDistancias.append(temp)
    
    # Calcula a MST
    mst = kruskalMst(listaArestas, len(coordenadas))
    # Calcula os vértices de grau impar
    verticesImpares = encontrarVerticesGrauImpar(mst, len(coordenadas))
    # Calcula o matching minimo no subgrafo dos vértices de grau ímpar
    matching = matchingMinimo(matrizDistancias, verticesImpares)
    # Adiciona as arestas do matching na MST
    arestasCombinacao = mst
    for (u, v) in matching:
        arestasCombinacao.append((u, v, matrizDistancias[u][v]))
    # Calcula o ciclo euleriano no multigrafo da união do matching minimo e da MST
    cicloEuleriano = encontraCicloEuleriano(arestasCombinacao, matrizDistancias)
    # Remove os vértices repetidos do ciclo
    cicloEulerianoComAtalhos = []
    pegos = set()
    for vertice in cicloEuleriano:
        if vertice not in pegos:
            cicloEulerianoComAtalhos.append(vertice)
            pegos.add(vertice)
    # Adiciona novamente o vértice que fecha o ciclo
    cicloEulerianoComAtalhos.append(cicloEuleriano[-1])
    # Calcula o custo da solução
    tamanho = 0
    verticeAtual = cicloEulerianoComAtalhos[0]
    ciclo = [verticeAtual]
    for proximoVertice in cicloEulerianoComAtalhos[1:]:
        tamanho += matrizDistancias[verticeAtual][proximoVertice]
        verticeAtual = proximoVertice
        ciclo.append(verticeAtual)
    return tamanho, ciclo, matrizDistancias