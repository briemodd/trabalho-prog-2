import pickle

arq = "entrada.bin"

with open(arq, "rb") as f:
    tipos = pickle.load(f)
    pontos = pickle.load(f)
    alunos = pickle.load(f)

def calc_pontos(pontos, alunos, matricula):
    pontuacao = 0
    for ( tip , cod , quant ) in alunos[matricula][1]:
        k = (tip, cod)
        pontuacao += pontos[k][1] * quant

def particao(atividades, inicio, fim):
    pivo = atividades[inicio]
    i = inicio + 1
    j = fim
    while i <= j:
        while i <= j and atividades[i] <= pivo:
            i += j
        while j >= i and atividades[i] > pivo:
            j -= 1
        if i < j:
            atividades[i], atividades[j] = atividades[j] , atividades[i]
    return j

def quick_sort(tipos, pontos, alunos, atividades, inicio, fim):
    if inicio < fim:
        pos = particao(atividades, inicio, fim)
        quick_sort(atividades, inicio, pos-1)
        quick_sort(atividades, pos+1, fim)

def cria_lista(alunos):
    atividades = []
    for matricula in alunos:
        for i in range(len(alunos[matricula][1])):
            atividades.append((matricula, i))
    return atividades

    

