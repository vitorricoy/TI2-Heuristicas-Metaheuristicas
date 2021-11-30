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

def vizinhosTrocaArestasMaisCaras(custoSolucao, solucao, matrizDistancias):
    numeroVertices = len(matrizDistancias)
    melhora = False
    custosArestas = []
    for i in range(numeroVertices):
        v1 = solucao[i]
        v2 = solucao[i+1]
        custosArestas.append((matrizDistancias[v1][v2], i))
    custosArestas = sorted(custosArestas)
    i1 = custosArestas[-1][1]
    i2 = custosArestas[-2][1]
    i = min(i1, i2)
    j = max(i1, i2)
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
        solucao = novaSolucao
        custoSolucao += mudanca
        melhora = True
    return solucao, custoSolucao, melhora

def vizinhos2Opt(custoSolucao, solucao, matrizDistancias):
    numeroVertices = len(matrizDistancias)
    for i in range(numeroVertices-1):
        for j in range(i+1, numeroVertices):
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
                solucao = novaSolucao
                custoSolucao += mudanca
                assert(solucao[0] == solucao[-1] and len(solucao) == len(matrizDistancias)+1)
                return solucao, custoSolucao, True
    return solucao, custoSolucao, False

def vizinhos2_5Opt(custoSolucao, solucao, matrizDistancias):
    numeroVertices = len(matrizDistancias)
    for i in range(numeroVertices-1):
        for j in range(i+1, numeroVertices):
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
                if melhorMudanca[1] == 1:
                    novaSolucao = solucao[:i+1]
                    novaSolucao.extend(reversed(solucao[i+1:j+1]))
                    novaSolucao.extend(solucao[j+1:])
                    solucao = novaSolucao
                elif melhorMudanca[1] == 2:
                    novaSolucao = solucao[:i+1]
                    novaSolucao.extend(solucao[i+1+1:j+1])
                    novaSolucao.append(i+1)
                    novaSolucao.extend(solucao[j+1:])
                    solucao = novaSolucao
                else:
                    novaSolucao = solucao[:i+1]
                    novaSolucao.append(j)
                    novaSolucao.extend(solucao[i+1:j])
                    novaSolucao.extend(solucao[j+1:])
                    solucao = novaSolucao
                assert(solucao[0] == solucao[-1] and len(solucao) == len(matrizDistancias)+1)
                custoSolucao += melhorMudanca[0]
                return solucao, custoSolucao, True
    return solucao, custoSolucao, False   

def vizinhos3Opt(custoSolucao, solucao, matrizDistancias):
    return None


def calcularHeuristica(coordenadas, att):
    custoSolucao, solucao, matrizDistancias = christofides.calcularHeuristica(coordenadas, att)
    while True:
        solucao, custoSolucao, melhorouUmaVez = vizinhosTrocaArestasMaisCaras(custoSolucao, solucao, matrizDistancias)
        if melhorouUmaVez:
            continue
        solucao, custoSolucao, melhorouUmaVez = vizinhos2Opt(custoSolucao, solucao, matrizDistancias)
        if melhorouUmaVez:
            continue
        solucao, custoSolucao, melhorouUmaVez = vizinhos2_5Opt(custoSolucao, solucao, matrizDistancias)
        if melhorouUmaVez:
            continue
        solucao, custoSolucao, melhorouUmaVez = vizinhos3Opt(custoSolucao, solucao, matrizDistancias)
        if not melhorouUmaVez:
            break
    return custoSolucao
        

lerArquivosDiretorio("ATT/", True)
lerArquivosDiretorio("EUC_2D/")