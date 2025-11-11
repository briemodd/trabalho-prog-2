import pickle

arq = "entrada3.bin"

with open(arq, "rb") as f:
    x1 = pickle.load(f)
    x2 = pickle.load(f)
    x3 = pickle.load(f)


