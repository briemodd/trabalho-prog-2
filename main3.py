import pickle
import sys

sys.setrecursionlimit(5000) 

def calc_pontos(pontos_info, aluno_info):
    
    pontos_por_tipo = {} 
    lista_atividades = aluno_info[1]

    # 1. Soma os pontos brutos por tipo
    for (tipo_id, cod_id, quant) in lista_atividades:
        chave_ponto = (tipo_id, cod_id)
        
        if chave_ponto not in pontos_info:
            continue 
            
        pontos_da_atividade = pontos_info[chave_ponto][1] 
        pontos_brutos = quant * pontos_da_atividade
        pontos_por_tipo[tipo_id] = pontos_por_tipo.get(tipo_id, 0) + pontos_brutos

    # 2. Aplica o limite de 10 pontos por tipo e soma
    pontuacao_total = 0
    for tipo_id in pontos_por_tipo:
        pontos_do_tipo = pontos_por_tipo[tipo_id]
        
        if pontos_do_tipo > 10:
            pontuacao_total += 10 
        else:
            pontuacao_total += pontos_do_tipo
            
    # 3. Aplica o limite total de 15 pontos 
    if pontuacao_total > 15:
        return 15
    
    return pontuacao_total

def compara_atividades(item_a, item_b, alunos, pontos_info):
    """
    Função de comparação principal que segue os 5 critérios[cite: 1218, 1222].
    Retorna True se A < B (A vem antes), False caso contrário.
    """
    
    mat_a, idx_a = item_a
    mat_b, idx_b = item_b

    info_aluno_a = alunos[mat_a]
    info_aluno_b = alunos[mat_b]

    # --- Critério 1: Pontuação total (Maior para Menor)
    pontos_a = calc_pontos(pontos_info, info_aluno_a)
    pontos_b = calc_pontos(pontos_info, info_aluno_b)
    
    if pontos_a > pontos_b:
        return True  
    if pontos_a < pontos_b:
        return False

    # --- Critério 2: Nome do aluno (Alfabética)
    nome_a = info_aluno_a[0]
    nome_b = info_aluno_b[0]
    
    if nome_a < nome_b:
        return True
    if nome_a > nome_b:
        return False

    # --- Critério 3: Matrícula (Alfabética)
    if mat_a < mat_b:
        return True
    if mat_a > mat_b:
        return False

    # --- Critério 4: Tipo de Atividade
    tipo_a = info_aluno_a[1][idx_a][0]
    tipo_b = info_aluno_b[1][idx_b][0]

    if tipo_a < tipo_b:
        return True
    if tipo_a > tipo_b:
        return False

    # --- Critério 5: Código da Atividade
    cod_a = info_aluno_a[1][idx_a][1]
    cod_b = info_aluno_b[1][idx_b][1]

    if cod_a < cod_b:
        return True
    
    return False

# --- Implementação do Merge Sort ---

def merge(atividades, esq, dir, alunos, pontos_info):
    
    # Índices iniciais para as duas sublistas
    i = 0 
    j = 0 
    
    # Índice inicial para a lista mesclada (resultado na lista 'atividades')
    k = 0 
    
    while i < len(esq) and j < len(dir):

        if compara_atividades(esq[i], dir[j], alunos, pontos_info):
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

def merge_sort(atividades, alunos, pontos_info):
    if len(atividades) > 1:
        meio = len(atividades) // 2
        esq = atividades[:meio]
        dir = atividades[meio:]
        
        merge_sort(esq, alunos, pontos_info)
        merge_sort(dir, alunos, pontos_info)
        merge(atividades, esq, dir, alunos, pontos_info)


# --- Funções de Preparação e Saída ---

def cria_lista(alunos):
    """Cria a lista de tuplas (matrícula, índice_atividade) para ordenação.""" 
    atividades = []
    for matricula in alunos:
        for i in range(len(alunos[matricula][1])):
            atividades.append((matricula, i))
    return atividades

def salvar_saida(atividades_ordenadas, tipos, pontos, alunos):
   
    with open("saida.txt", "w", encoding="utf-8") as f:
        matricula_anterior = None
        
        for (mat, idx) in atividades_ordenadas:
            
            # Se a matrícula mudou, imprime o cabeçalho do aluno [cite: 1242]
            if mat != matricula_anterior:
                info_aluno = alunos[mat]
                nome = info_aluno[0]
                pontuacao = calc_pontos(pontos, info_aluno)
                
                # Formato: "Nome (Matricula): X pontos" [cite: 1244]
                f.write(f"{nome} ({mat}): {pontuacao} pontos\n")
                matricula_anterior = mat
            
            # Pega os dados da atividade específica
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
            
            # Formato: "  T.C Nome Atividade: QxP=Total" [cite: 1245, 1247]
            f.write(f"  {tipo_id}.{cod_id} {nome_atividade}: {quant}x{pontos_unitarios}={pontos_calculados}\n")

def main():

    arq_entrada = "entrada1.bin"
    
    # Leitura do arquivo binário [cite: 1223]
    with open(arq_entrada, "rb") as f:
        tipos = pickle.load(f)
        pontos = pickle.load(f)
        alunos = pickle.load(f)
    

    atividades = cria_lista(alunos)
    
    # Chama o Merge Sort
    merge_sort(atividades, alunos, pontos)
    
    salvar_saida(atividades, tipos, pontos, alunos)
    
    print("Arquivo 'saida.txt' gerado com sucesso.")

main()