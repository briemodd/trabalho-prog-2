import pickle
import sys

sys.setrecursionlimit(5000) 

def calc_pontos(pontos_info, aluno_info):
    
    pontos_por_tipo = {} # Dicionário temporário para somar pontos por tipo
    lista_atividades = aluno_info[1]

    # 1. Soma os pontos brutos por tipo
    for (tipo_id, cod_id, quant) in lista_atividades:
        chave_ponto = (tipo_id, cod_id)
        
        # Se a chave não existir (arquivo de entrada inconsistente), ignora
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
            pontuacao_total += 10 # Limite de 10 por tipo 
        else:
            pontuacao_total += pontos_do_tipo
            
    # 3. Aplica o limite total de 15 pontos
    if pontuacao_total > 15:
        return 15 # Limite total de 15 
    
    return pontuacao_total

def compara_atividades(item_a, item_b, alunos, pontos_info):
    """
    Função de comparação principal que segue os 5 critérios .
    item_a e item_b sao tuplas: (matricula, indice_atividade)
    Retorna True se A < B (A vem antes), False caso contrário.
    """
    
    mat_a, idx_a = item_a
    mat_b, idx_b = item_b

    info_aluno_a = alunos[mat_a]
    info_aluno_b = alunos[mat_b]

    # --- Critério 1: Pontuação total (Maior para Menor) ---
    # Nota: O cálculo é refeito aqui, como pedido [cite: 78]
    pontos_a = calc_pontos(pontos_info, info_aluno_a)
    pontos_b = calc_pontos(pontos_info, info_aluno_b)
    
    if pontos_a > pontos_b:
        return True  # A vem antes (pontuação maior)
    if pontos_a < pontos_b:
        return False # B vem antes

    # --- Critério 2: Nome do aluno (Alfabética) ---
    nome_a = info_aluno_a[0]
    nome_b = info_aluno_b[0]
    
    if nome_a < nome_b:
        return True  # A vem antes (nome)
    if nome_a > nome_b:
        return False # B vem antes

    # --- Critério 3: Matrícula (Alfabética) ---
    if mat_a < mat_b:
        return True
    if mat_a > mat_b:
        return False

    # --- Critério 4: Tipo de Atividade ---
    tipo_a = info_aluno_a[1][idx_a][0]
    tipo_b = info_aluno_b[1][idx_b][0]

    if tipo_a < tipo_b:
        return True
    if tipo_a > tipo_b:
        return False

    # --- Critério 5: Código da Atividade ---
    cod_a = info_aluno_a[1][idx_a][1]
    cod_b = info_aluno_b[1][idx_b][1]

    if cod_a < cod_b:
        return True
    
    return False

def particao(atividades, inicio, fim, alunos, pontos_info):
    
    pivo = atividades[fim]
    i = inicio - 1

    for j in range(inicio, fim):
        # Compara o item atual com o pivô
        if compara_atividades(atividades[j], pivo, alunos, pontos_info):
            i += 1
            atividades[i], atividades[j] = atividades[j], atividades[i]

    # Coloca o pivô no lugar certo
    atividades[i + 1], atividades[fim] = atividades[fim], atividades[i + 1]
    return i + 1

def quick_sort(atividades, inicio, fim, alunos, pontos_info):
    if inicio < fim:
        pos_pivo = particao(atividades, inicio, fim, alunos, pontos_info)
        quick_sort(atividades, inicio, pos_pivo - 1, alunos, pontos_info)
        quick_sort(atividades, pos_pivo + 1, fim, alunos, pontos_info)

def cria_lista(alunos):
    atividades = []
    for matricula in alunos:
        for i in range(len(alunos[matricula][1])):
            atividades.append((matricula, i))
    return atividades

def salvar_saida(atividades_ordenadas, tipos, pontos, alunos):
   
    with open("saida.txt", "w", encoding="utf-8") as f:
        matricula_anterior = None
        
        for (mat, idx) in atividades_ordenadas:
            
            # Se a matrícula mudou, imprime o cabeçalho do aluno
            if mat != matricula_anterior:
                info_aluno = alunos[mat]
                nome = info_aluno[0]
                pontuacao = calc_pontos(pontos, info_aluno)
                
                # Formato: "Nome (Matricula): X pontos" [cite: 85, 87]
                f.write(f"{nome} ({mat}): {pontuacao} pontos\n")
                matricula_anterior = mat
            
            # Pega os dados da atividade específica
            atividade = alunos[mat][1][idx] 
            tipo_id, cod_id, quant = atividade
            
            chave_ponto = (tipo_id, cod_id)
            
            # Se a atividade não existe no dict de pontos, pula
            if chave_ponto not in pontos:
                f.write(f"  {tipo_id}.{cod_id} (ATIVIDADE DESCONHECIDA)\n")
                continue

            info_ponto = pontos[chave_ponto]
            nome_atividade = info_ponto[0]
            pontos_unitarios = info_ponto[1]
            pontos_calculados = quant * pontos_unitarios
            
            # Formato: "  T.C Nome Atividade: QxP=Total" [cite: 86, 88-91]
            f.write(f"  {tipo_id}.{cod_id} {nome_atividade}: {quant}x{pontos_unitarios}={pontos_calculados}\n")

def main():

    arq_entrada = "entrada1.bin"
    
    with open(arq_entrada, "rb") as f:
        tipos = pickle.load(f)
        pontos = pickle.load(f)
        alunos = pickle.load(f)
    

    atividades = cria_lista(alunos)
    
    quick_sort(atividades, 0, len(atividades) - 1, alunos, pontos)
    
    salvar_saida(atividades, tipos, pontos, alunos)
    
    print("Arquivo 'saida.txt' gerado com sucesso.")

main()