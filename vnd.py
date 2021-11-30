import math
import time
import os
import christofides
import itertools

# Lê os arquivos do diretório indicado, executa a heurística para cada um deles e imprime o resultado
def lerArquivosDiretorio(diretorio, att = False):
    for filename in os.listdir(diretorio):
        coordenadas = []
        cont = 0
        with open(diretorio+filename) as file:
            for line in file:
                line = line.strip()
                if line == 'EOF':
                    break
                if cont < 6:
                    cont+=1
                else:
                    partes = line.split()
                    x = float(partes[1])
                    y = float(partes[2])
                    coordenadas.append((x, y))
        
        inicio = time.time()
        resultado = calcularHeuristica(coordenadas, att)
        tempoGasto = time.time() - inicio
        print("Resultado encontrado para o arquivo", filename, ":", resultado)
        print("Tempo gasto para o arquivo", filename, ":", tempoGasto*1000.0, "ms")
        print()


# Implementa a função de vizinhança que troca as arestas mais caras
def vizinhosTrocaArestasMaisCaras(custoSolucao, solucao, matrizDistancias):
    numeroVertices = len(matrizDistancias)
    melhora = False
    custosArestas = []
    for i in range(numeroVertices):
        v1 = solucao[i]
        v2 = solucao[i+1]
        custosArestas.append((matrizDistancias[v1][v2], i))
    # Busca as arestas com os dois maiores custos
    custosArestas = sorted(custosArestas)
    i1 = custosArestas[-1][1]
    i2 = custosArestas[-2][1]
    i = min(i1, i2)
    j = max(i1, i2)
    v1 = solucao[i]
    v2 = solucao[i+1]
    u1 = solucao[j]
    u2 = solucao[j+1]
    # Faz o algoritmo de troca do 2-Opt para as duas arestas de maior custo
    mudanca = matrizDistancias[v1][u1] + matrizDistancias[v2][u2] - matrizDistancias[v1][v2] - matrizDistancias[u1][u2]
    if mudanca < 0:
        # Achou aprimorante
        novaSolucao = solucao[:i+1]
        novaSolucao.extend(reversed(solucao[i+1:j+1]))
        novaSolucao.extend(solucao[j+1:])
        solucao = novaSolucao
        custoSolucao += mudanca
        melhora = True
    return solucao, custoSolucao, melhora

# Implementa a função de vizinhança de 2-Opt
def vizinhos2Opt(custoSolucao, solucao, matrizDistancias):
    combinacoes = list(itertools.combinations(range(0, len(matrizDistancias)), 2))
    for i, j in combinacoes:
        v1 = solucao[i]
        v2 = solucao[i+1]
        u1 = solucao[j]
        u2 = solucao[j+1]

        mudanca = matrizDistancias[v1][u1] + matrizDistancias[v2][u2] - matrizDistancias[v1][v2] - matrizDistancias[u1][u2]
        if mudanca < 0:
            # Achou aprimorante
            novaSolucao = solucao[:i+1]
            novaSolucao.extend(reversed(solucao[i+1:j+1]))
            novaSolucao.extend(solucao[j+1:])
            custoSolucao += mudanca
            return novaSolucao, custoSolucao, True
    return solucao, custoSolucao, False

# Implementa a função de vizinhança de 2.5-Opt
def vizinhos2_5Opt(custoSolucao, solucao, matrizDistancias):
    combinacoes = list(itertools.combinations(range(0, len(matrizDistancias)), 2))
    for i, j in combinacoes:
        v1 = solucao[i]
        v2 = solucao[i+1]
        v3 = solucao[i+2]
        u0 = solucao[j-1]
        u1 = solucao[j]
        u2 = solucao[j+1]

        mudanca1 = matrizDistancias[v1][u1] + matrizDistancias[v2][u2] - matrizDistancias[v1][v2] - matrizDistancias[u1][u2]
        mudanca2 = matrizDistancias[u1][v2] + matrizDistancias[v2][u2] + matrizDistancias[v1][v3] - matrizDistancias[v1][v2] - matrizDistancias[u1][u2] - matrizDistancias[v2][v3]
        mudanca3 = matrizDistancias[v1][u1] + matrizDistancias[u1][v2] + matrizDistancias[u2][u0] - matrizDistancias[v1][v2] - matrizDistancias[u1][u2] - matrizDistancias[u1][u0]
        
        melhorMudanca = max((mudanca1, 1), (mudanca2, 2), (mudanca3, 3))
        if melhorMudanca[0] < 0:
            # Achou aprimorante
            if melhorMudanca[1] == 1: # É do tipo igual ao 2-Opt
                novaSolucao = solucao[:i+1]
                novaSolucao.extend(reversed(solucao[i+1:j+1]))
                novaSolucao.extend(solucao[j+1:])
                solucao = novaSolucao
            elif melhorMudanca[1] == 2: # É uma das trocas do 2.5-Opt
                novaSolucao = solucao[:i+1]
                novaSolucao.extend(solucao[i+1+1:j+1])
                novaSolucao.append(i+1)
                novaSolucao.extend(solucao[j+1:])
                solucao = novaSolucao
            else: # É o outro tipo de troca do 2.5-Opt
                novaSolucao = solucao[:i+1]
                novaSolucao.append(j)
                novaSolucao.extend(solucao[i+1:j])
                novaSolucao.extend(solucao[j+1:])
                solucao = novaSolucao
            custoSolucao += melhorMudanca[0]
            return solucao, custoSolucao, True
    return solucao, custoSolucao, False   

# Calcula o custo de uma solução definida pela lista com a ordem de visitação dos vértices
def calcularCustoSolucao(solucao, matrizDistancias):
    custo = 0
    for i in range(len(solucao)-1):
        custo += matrizDistancias[solucao[i]][solucao[i+1]]
    return custo

# Implementa a função de vizinhança das três trocas
def vizinhos3Trocas(custoSolucao, solucao, matrizDistancias):
    combinacoes = list(itertools.combinations(range(0, len(matrizDistancias)), 3))
    for i, j, k in combinacoes:
        permutacoes = list(itertools.permutations([solucao[i], solucao[j], solucao[k]]))
        for v, u, t in permutacoes:
            # Para cada troca possível da ordem de visitação de três vértices calcula a nova solução após a troca e seu valor
            novaSolucao = solucao.copy()
            novaSolucao[i] = v
            novaSolucao[j] = u
            novaSolucao[k] = t

            if i == 0:
                novaSolucao[-1] = v

            if j == 0:
                novaSolucao[-1] = u

            if k == 0:
                novaSolucao[-1] = t

            novoCustoSolucao = calcularCustoSolucao(novaSolucao, matrizDistancias)

            if novoCustoSolucao < custoSolucao:
                return novaSolucao, novoCustoSolucao, True

    return solucao, custoSolucao, False

# Implementação da heurística de VND
def calcularHeuristica(coordenadas, att):
    # Calcula a solução inicial por meio do algoritmo de christofides
    custoSolucao, solucao, matrizDistancias = christofides.calcularHeuristica(coordenadas, att)
    # Executa o algoritmo de VND
    while True:
        # Busca o ótimo local da primeira função de vizinhança
        solucao, custoSolucao, _ = vizinhosTrocaArestasMaisCaras(custoSolucao, solucao, matrizDistancias)
        # Busca um vizinho aprimorante da segunda função de vizinhança
        solucao, custoSolucao, melhorouUmaVez = vizinhos2Opt(custoSolucao, solucao, matrizDistancias)
        if melhorouUmaVez: # Se existe o vizinho aprimorante reeinicia a execução das funções de vizinhança
            continue
        # Busca um vizinho aprimorante da terceira função de vizinhança
        solucao, custoSolucao, melhorouUmaVez = vizinhos2_5Opt(custoSolucao, solucao, matrizDistancias)
        if melhorouUmaVez: # Se existe o vizinho aprimorante reeinicia a execução das funções de vizinhança
            continue
        # Busca um vizinho aprimorante da quarta função de vizinhança
        solucao, custoSolucao, melhorouUmaVez = vizinhos3Trocas(custoSolucao, solucao, matrizDistancias)
        if not melhorouUmaVez:  # Se não existir o vizinho aprimorante encerra a execução do algoritmo
            break
    return custoSolucao
        

lerArquivosDiretorio("ATT/", True)
lerArquivosDiretorio("EUC_2D/")