import pickle

arq = "entrada3.bin"

with open(arq, "rb") as f:
    tipos = pickle.load(f)
    pontos = pickle.load(f)
    alunos = pickle.load(f)


