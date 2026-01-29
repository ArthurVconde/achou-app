import os
import json
import re

# lista dos arquivos que vou checar
arquivos_json = [
    "acougue.json", "bares.json", "escola.json", "padarias.json", "psicologo.json", 
    "salao_de_beleza.json", "advogados.json", "farmacia.json", "mercados.json", 
    "pedreiro.json", "pintor.json", "restaurantes.json", "Sorveteria.json", 
    "bombeiro_hidraulico.json", "lanches.json", "lava_jato.json", "mecanica_motos.json", 
    "otica.json", "pizzarias.json"
]

def limpar_numero(numero, whatsapp=False):
    """Tenta limpar o número de telefone, adicionando DDD se necessário"""
    if not numero:
        return None
    
    # tira tudo que não for número
    numero_limpo = re.sub(r'\D', '', str(numero))
    
    tamanho = len(numero_limpo)

    # se for whatsapp (já tem DDD)
    if whatsapp:
        if 10 <= tamanho <= 11:
            return numero_limpo
    
    # se for telefone normal
    else:
        # se tiver 8 ou 9 dígitos, bota o DDD 32 na frente
        if tamanho == 8 or tamanho == 9:
            return '32' + numero_limpo
        # se já tiver 10 ou 11, deixa como tá
        elif 10 <= tamanho <= 11:
            return numero_limpo
    
    return None

def encontrar_duplicados():
    """Procura registros repetidos nos arquivos JSON usando telefone/whatsapp"""
    print("--- Procurando números duplicados ---")
    
    todos_numeros = {}
    total_registros = 0
    
    # só pega os arquivos que realmente existem
    arquivos_existentes = []
    for arq in arquivos_json:
        if os.path.exists(arq):
            arquivos_existentes.append(arq)
        else:
            print(f"Arquivo não encontrado: {arq}")

    for nome_arquivo in arquivos_existentes:
        try:
            with open(nome_arquivo, 'r', encoding='utf-8') as f:
                conteudo = json.load(f)
        except Exception as e:
            print(f"Erro ao abrir {nome_arquivo}: {e}")
            continue

        if not isinstance(conteudo, list):
            continue

        for registro in conteudo:
            total_registros += 1
            
            # tenta pegar o whatsapp primeiro
            whatsapp = limpar_numero(registro.get('whatsapp'), whatsapp=True)
            # se não tiver, pega o telefone
            telefone = limpar_numero(registro.get('telefone'))
            
            # usa o que tiver disponível
            numero_principal = whatsapp if whatsapp else telefone
            
            if not numero_principal:
                continue

            # monta a informação do registro
            info = {
                'arquivo': nome_arquivo,
                'nome': registro.get('nome', 'Sem nome')
            }
            
            # guarda no dicionário
            if numero_principal in todos_numeros:
                # evita contar o mesmo arquivo duas vezes
                if not any(item['arquivo'] == nome_arquivo for item in todos_numeros[numero_principal]):
                    todos_numeros[numero_principal].append(info)
            else:
                todos_numeros[numero_principal] = [info]

    # mostra os resultados
    print("\n" + "-" * 60)
    print("RESULTADO DA BUSCA")
    print("-" * 60)
    print(f"Arquivos verificados: {len(arquivos_existentes)}")
    print(f"Registros no total: {total_registros}")
    print(f"Números diferentes encontrados: {len(todos_numeros)}")
    
    # pega só os que aparecem mais de uma vez
    duplicados = {num: ocorrencias for num, ocorrencias in todos_numeros.items() if len(ocorrencias) > 1}
    
    print(f"Números duplicados: {len(duplicados)}")
    print("-" * 60)

    if not duplicados:
        print("\nNenhum número duplicado encontrado!")
        return

    print("\nDetalhes dos números que aparecem em mais de um arquivo:")
    
    for numero, ocorrencias in duplicados.items():
        print(f"\nNúmero: {numero}")
        for ocor in ocorrencias:
            print(f"  - {ocor['nome']} (em {ocor['arquivo']})")
    
    print("\n" + "-" * 60)
    print("Dica: Revise esses registros nos arquivos listados acima.")

# só roda se chamar o script diretamente
if __name__ == "__main__":
    encontrar_duplicados()