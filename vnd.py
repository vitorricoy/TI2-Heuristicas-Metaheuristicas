import math
import time
import os
import christofides

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

def vizinhos2Opt(solucao, matrizDistancias):


def vizinhosOrOpt(solucao, matrizDistancias):
    

def vizinhos25Opt(solucao, matrizDistancias):
    

def vizinhos3Opt(solucao, matrizDistancias):
    


def calcularHeuristica(coordenadas, att):
    solucao, valor, matrizDistancias = christofides.calcularHeuristica(coordenadas, att)


lerArquivosDiretorio("ATT/", True)
lerArquivosDiretorio("EUC_2D/")