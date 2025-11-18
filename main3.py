import pickle
import time

def calc_pontos(pontos_info, aluno_info, ntipos):
    lista_atividades = aluno_info[1]
    pontos_tipo = [0] * (ntipos + 1)

    for (tipo_id, cod_id, quant) in lista_atividades:
        chave_ponto = (tipo_id, cod_id)
        if chave_ponto in pontos_info:
            pontos_da_atividade = pontos_info[chave_ponto][1] 
            pontos_brutos = quant * pontos_da_atividade
            if tipo_id == 1: pontos_tipo[0] += pontos_brutos
            elif tipo_id == 2: pontos_tipo[1] += pontos_brutos
            elif tipo_id == 3: pontos_tipo[2] += pontos_brutos
            elif tipo_id == 4: pontos_tipo[3] += pontos_brutos

    pontuacao_total = 0
    pontuacao_total += min(pontos_tipo[0], 10)
    pontuacao_total += min(pontos_tipo[1], 10)
    pontuacao_total += min(pontos_tipo[2], 10)
    pontuacao_total += min(pontos_tipo[3], 10)
            
    return min(pontuacao_total, 15)

def compara_atividades(item_a, item_b, alunos, pontos_info, ntipos):

    mat_a, idx_a = item_a
    mat_b, idx_b = item_b

    info_aluno_a = alunos[mat_a]
    info_aluno_b = alunos[mat_b]

    pontos_a = calc_pontos(pontos_info, info_aluno_a, ntipos)
    pontos_b = calc_pontos(pontos_info, info_aluno_b, ntipos)
    
    if pontos_a > pontos_b:
        return True  
    if pontos_a < pontos_b:
        return False

    nome_a = info_aluno_a[0]
    nome_b = info_aluno_b[0]
    
    if nome_a < nome_b:
        return True
    if nome_a > nome_b:
        return False

    if mat_a < mat_b:
        return True
    if mat_a > mat_b:
        return False

    tipo_a = info_aluno_a[1][idx_a][0]
    tipo_b = info_aluno_b[1][idx_b][0]

    if tipo_a < tipo_b:
        return True
    if tipo_a > tipo_b:
        return False

    cod_a = info_aluno_a[1][idx_a][1]
    cod_b = info_aluno_b[1][idx_b][1]

    if cod_a < cod_b:
        return True
    
    return False

def merge(atividades, esq, dir, alunos, pontos_info, ntipos):

    i = 0 
    j = 0 
    
    k = 0 
    
    while i < len(esq) and j < len(dir):

        if compara_atividades(esq[i], dir[j], alunos, pontos_info, ntipos):
            atividades[k] = esq[i]
            i += 1
        else:
            atividades[k] = dir[j]
            j += 1
        k += 1
    
    while i < len(esq):
        atividades[k] = esq[i]
        i += 1
        k += 1
    while j < len(dir):
        atividades[k] = dir[j]
        j += 1
        k += 1

def merge_sort(atividades, alunos, pontos_info, ntipos):
    if len(atividades) > 1:
        meio = len(atividades) // 2
        esq = atividades[:meio]
        dir = atividades[meio:]
        
        merge_sort(esq, alunos, pontos_info, ntipos)
        merge_sort(dir, alunos, pontos_info, ntipos)
        merge(atividades, esq, dir, alunos, pontos_info, ntipos)


def cria_lista(alunos):
    atividades = []
    for matricula in alunos:
        for i in range(len(alunos[matricula][1])):
            atividades.append((matricula, i))
    return atividades

def salvar_saida(atividades_ordenadas, tipos, pontos, alunos, ntipos):
   
    with open("saida.txt", "w", encoding="utf-8") as f:
        matricula_anterior = None
        
        for (mat, idx) in atividades_ordenadas:
            
            if mat != matricula_anterior:
                info_aluno = alunos[mat]
                nome = info_aluno[0]
                pontuacao = calc_pontos(pontos, info_aluno, ntipos)
                
                f.write(f"{nome} ({mat}): {pontuacao} pontos\n")
                matricula_anterior = mat
            
            atividade = alunos[mat][1][idx] 
            tipo_id, cod_id, quant = atividade
            
            chave_ponto = (tipo_id, cod_id)
            
            if chave_ponto not in pontos:
                f.write(f"  {tipo_id}.{cod_id} (ATIVIDADE DESCONHECIDA)\n")
                continue

            info_ponto = pontos[chave_ponto]
            nome_atividade = info_ponto[0]
            pontos_unitarios = info_ponto[1]
            pontos_calculados = quant * pontos_unitarios
            
            f.write(f"  {tipo_id}.{cod_id} {nome_atividade}: {quant}x{pontos_unitarios}={pontos_calculados}\n")

def main():
    t1 = time.perf_counter()
    arq_entrada = "entrada4.bin"
    
    with open(arq_entrada, "rb") as f:
        tipos = pickle.load(f)
        pontos = pickle.load(f)
        alunos = pickle.load(f)
    
    ntipos = len(tipos)

    atividades = cria_lista(alunos)

    merge_sort(atividades, alunos, pontos, ntipos)
    
    salvar_saida(atividades, tipos, pontos, alunos, ntipos)
    t2 = time.perf_counter()
    print("tempo merge: ", t2 - t1)
    print("Arquivo 'saida.txt' gerado com sucesso.")

main()