import pickle

arq = "entrada3.bin"

with open(arq, "rb") as f:
    dados = pickle.load(f)

print(dados) oi
