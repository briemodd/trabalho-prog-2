import pickle

arq = "entrada1.bin"

with open(arq, "rb") as f:
    tipos = pickle.load(f)
    pontos = pickle.load(f)
    alunos = pickle.load(f)

def cria_lista(alunos):
    atividades = []
    for matricula in alunos:
        for i in range(len(alunos[matricula][1])):
            atividades.append((matricula, i))
    print(atividades)

cria_lista(alunos)

