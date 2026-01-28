import os
import json
import re
from datetime import datetime
from unidecode import unidecode # Biblioteca para remover acentos

# --- PARTE 1: CONFIGURAÇÃO DE NOMES E MAPEAMENTO ---

# Mapeamento do nome atual do arquivo (Chave) para o nome padronizado do Base44 (Valor).
# Isso corrige erros de leitura causados por espaços, acentos e letras maiúsculas.
MAPPING_RENAME = {
    # Arquivos da Imagem 1 (com maiúsculas, acentos ou espaços)
    "Barbearia.json": "barbearia.json",
    "Bares.json": "bares.json", # Padronizando para minúscula
    "Bombeiro Hidraulico.json": "bombeiro_hidraulico.json",
    "Borracharia.json": "borracharia.json",
    "Clinica Médica.json": "clinica_medica.json",
    "Clinica Veterinária.json": "clinica_veterinaria.json",
    "Comida Japonesa.json": "comida_japonesa.json",
    "Contador.json": "contador.json",
    "Dentista.json": "dentista.json",
    "Designer gráfico.json": "designer_grafico.json",
    "Distribuidora de bebidas.json": "distribuidora_bebidas.json",
    "Escola.json": "escola.json",
    "Floricultura.json": "floricultura.json",
    "Fotógrafo.json": "fotografo.json",
    "Gás e Água.json": "gas_e_agua.json",
    "Informática.json": "informatica.json",
    "Lanterna e pintura.json": "lanterna_e_pintura.json",
    "Lava Jato.json": "lava_jato.json",
    "Manicure e pedicuri.json": "manicure_pedicure.json",
    "Mecanico Carro.json": "mecanica_carros.json",
    "Mecanico moto.json": "mecanica_motos.json",
    "Moda feminina.json": "moda_feminina.json",
    "Moda infantil.json": "moda_infantil.json",
    "Moda Masculina.json": "moda_masculina.json",
    "Moto Taxi.json": "mototaxi.json",
    "Oficina.json": "oficina.json",
    "Ótica.json": "otica.json",
    "Papelaria.json": "papelaria.json",
    "Petshop.json": "pet_shop.json",
    "Podólogo.json": "podologo.json",
    "Posto de combustível.json": "posto_combustivel.json",
    "Psicólogo.json": "psicologo.json",
    "Restaurantes.json": "restaurantes.json",
    "Salão de Beleza.json": "salao_de_beleza.json",
    "Sorveteria.json": "sorveteria.json",
    "Taxi.json": "taxi.json",
    "Vidraçaria.json": "vidracaria.json",
    
    # Arquivos da Imagem 2 (com acentos)
    "açougue.json": "acougue.json",
    "Farmácia.json": "farmacia.json",
    
    # Outros arquivos da lista de categorias Base44 (se ainda estiverem em maiúsculas/mistos)
    "Hospital.json": "hospital.json", 
    "Advogado.json": "advogado.json",
    "Ar Condicionado.json": "ar_condicionado.json",
    "Auto Eletrica.json": "auto_eletrica.json",
    "Lanches.json": "lanches.json",
    "Pizzarias.json": "pizzarias.json",
    "Padarias.json": "padarias.json",
    "Mercados.json": "mercados.json",
    "Eletricista.json": "eletricista.json",
    "Encanador.json": "encanador.json",
    "Pintor.json": "pintor.json",
    "Pedreiro.json": "pedreiro.json",
    # Certifique-se de que todos os seus arquivos estão listados aqui
}

# Lista Mestra de TODOS os nomes de arquivos APÓS a renomeação (para processamento de conteúdo)
NOMES_DOS_ARQUIVOS_MESTRE = list(set(MAPPING_RENAME.values()))
NOMES_DOS_ARQUIVOS_MESTRE = [nome.replace(".json", "") for nome in NOMES_DOS_ARQUIVOS_MESTRE]

# --- PARTE 2: FUNÇÕES DE RENOMEAÇÃO ---

def renomear_arquivos(mapping):
    """Executa a renomeação dos arquivos JSON com base no mapeamento."""
    print("--- 1/2: INICIANDO A RENOMEAÇÃO DOS ARQUIVOS (CORREÇÃO DE NOME) ---")
    arquivos_renomeados = 0
    
    for old_name, new_name in mapping.items():
        if os.path.exists(old_name):
            try:
                os.rename(old_name, new_name)
                print(f"✅ Renomeado: '{old_name}' -> '{new_name}'")
                arquivos_renomeados += 1
            except Exception as e:
                print(f"❌ Erro ao renomear '{old_name}' para '{new_name}': {e}")
        else:
            if not os.path.exists(new_name):
                 print(f"⚠️ Arquivo '{old_name}' não encontrado. Foi pulado ou já foi renomeado.")

    print(f"\n✅ Renomeação concluída. {arquivos_renomeados} arquivos padronizados.")


# --- PARTE 3: FUNÇÕES DE CORREÇÃO DE CONTEÚDO ---

KEY_MAPPING = {
    'name': 'nome',
    'address': 'endereco',
    'phone': 'telefone',
    'website': 'site',
    'rating': 'avaliacao',
    'hours': 'horario'
}

def formatar_intervalo(intervalo_str):
    if 'Closed' in intervalo_str or 'Fechado' in intervalo_str:
        return "Fechado"
    partes = re.split(r'\s*[–-]\s*', intervalo_str)
    if len(partes) == 2:
        try:
            # Tenta converter para 24h, tratando AM/PM
            hora_inicio_str = partes[0].replace('\u202f', ' ').strip(' ')
            hora_fim_str = partes[1].replace('\u202f', ' ').strip(' ')
            
            # Tenta formatos I:M P (9:00 AM) e I:M (1:00)
            def converter_para_24h(h_str):
                try: # Tenta I:M P (ex: 9:00 AM)
                    return datetime.strptime(h_str, '%I:%M %p').strftime('%H:%M')
                except ValueError:
                    try: # Tenta I:M (ex: 1:00, mas com 1 dígito na hora)
                        dt = datetime.strptime(h_str, '%H:%M')
                        return dt.strftime('%H:%M')
                    except ValueError:
                        try: # Tenta I:M (ex: 1:00) e garante 2 dígitos na hora
                             parts = h_str.split(':')
                             return f"{parts[0].zfill(2)}:{parts[1]}"
                        except:
                            return h_str

            hora_inicio = converter_para_24h(hora_inicio_str)
            hora_fim = converter_para_24h(hora_fim_str)
            
            return f"{hora_inicio} as {hora_fim}"
        except:
            return intervalo_str.strip()
    return intervalo_str.strip()

def formatar_horario_google(lista_horarios):
    if not lista_horarios:
        return "Não Informado"
    for linha in lista_horarios:
        match = re.match(r'(\w+):\s*(.*)', linha)
        if match:
            intervalos_str = match.group(2)
            if 'Closed' in intervalos_str:
                continue
            intervalos_lista = [s.strip() for s in intervalos_str.split(',')]
            horarios_do_dia = []
            for intervalo in intervalos_lista:
                horario_formatado = formatar_intervalo(intervalo)
                if horario_formatado != "Fechado":
                    horarios_do_dia.append(horario_formatado)
            if horarios_do_dia:
                return " e ".join(horarios_do_dia)
    return "Fechado"

def padronizar_horario_string(horario_str):
    """Adiciona zeros à esquerda em strings de horário (ex: '1:30' -> '01:30')."""
    if not horario_str or horario_str in ["Não Informado", "Fechado"]:
        return horario_str

    def pad_time(match):
        time_str = match.group(0)
        # Se for um formato H:MM (ex: 1:30), adiciona o zero
        parts = time_str.split(':')
        return f"{parts[0].zfill(2)}:{parts[1]}"

    # Encontra e padroniza o formato H:MM (1 ou 2 dígitos)
    horario_padronizado = re.sub(r'\b\d{1,2}:\d{2}\b', pad_time, horario_str)
    
    return horario_padronizado

def processar_arquivo(nome_base):
    """Abre, limpa e salva o conteúdo de um único arquivo JSON."""
    nome_arquivo = f"{nome_base}.json"
    
    if not os.path.exists(nome_arquivo):
        print(f"⚠️  Arquivo '{nome_arquivo}' não encontrado após renomeação. Pulando...")
        return

    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            dados = json.load(f)
    except Exception as e:
        print(f"❌  Erro ao ler '{nome_arquivo}': {e}. Pulando...")
        return

    if not isinstance(dados, list):
        return

    novos_dados = []
    houve_alteracoes = False
    registros_excluidos = 0

    for item in dados:
        if not isinstance(item, dict):
            continue
        
        novo_item = item.copy()
        item_foi_alterado_individualmente = False
        
        # 1. Mapeamento de Chaves (Inglês -> Português)
        for old_key, new_key in KEY_MAPPING.items():
            if old_key in novo_item:
                novo_item[new_key] = novo_item.pop(old_key)
                item_foi_alterado_individualmente = True
        
        # 2. VALIDAÇÃO E FILTRO (Remove unknown/Nome não informado)
        nome_para_validar = novo_item.get('nome')
        if nome_para_validar is None or \
           str(nome_para_validar).strip().lower() == "unknown" or \
           str(nome_para_validar).strip().lower() == "nome não informado":
            registros_excluidos += 1
            houve_alteracoes = True
            continue 
        
        # 3. Adiciona o campo de Aprovação
        if 'aprovado' not in novo_item:
            novo_item['aprovado'] = True
            item_foi_alterado_individualmente = True
        
        # 4. Formatação de Horário (Lista para String e Padronização H:MM -> HH:MM)
        horario_atual = novo_item.get('horario')
        
        if isinstance(horario_atual, list):
            novo_horario = formatar_horario_google(horario_atual)
            novo_item['horario'] = padronizar_horario_string(novo_horario)
            item_foi_alterado_individualmente = True
            
        elif isinstance(horario_atual, str):
            horario_padronizado = padronizar_horario_string(horario_atual)
            if horario_padronizado != horario_atual:
                novo_item['horario'] = horario_padronizado
                item_foi_alterado_individualmente = True
                
        elif horario_atual is None:
             novo_item['horario'] = "Não Informado"
             item_foi_alterado_individualmente = True

        # 5. Formatação de Telefone e WhatsApp (Remoção de DDD no 'telefone' local)
        telefone_original = novo_item.get('telefone')
        
        if telefone_original and str(telefone_original).strip():
            # Remove caracteres não numéricos
            numeros_limpos = re.sub(r'\D', '', str(telefone_original))
            
            if numeros_limpos:
                numero_whatsapp = numeros_limpos
                numero_local = numeros_limpos
                
                # Assume que 10 ou 11 dígitos incluem DDD
                if len(numero_local) >= 10: 
                    ddd = numero_local[:2]
                    numero_local = numero_local[2:] 
                
                # Se o número local resultante tiver 8 ou 9 dígitos, é válido
                if 8 <= len(numero_local) <= 9:
                    novo_item['telefone'] = f"({numero_local})"
                else:
                    # Se não for um número local padrão, deixa o telefone como o número completo
                    novo_item['telefone'] = f"({numeros_limpos})"

                # Garante que o 'whatsapp' tenha o DDD (completo)
                if len(numero_whatsapp) <= 9: # 8 ou 9 dígitos (local)
                    # Assumindo DDD 32 para números locais
                    novo_item['whatsapp'] = '32' + numero_whatsapp
                else:
                    novo_item['whatsapp'] = numero_whatsapp
                    
                item_foi_alterado_individualmente = True
            else:
                novo_item['telefone'] = None
                novo_item['whatsapp'] = None
        else:
            novo_item['telefone'] = None
            novo_item['whatsapp'] = None

        novos_dados.append(novo_item)
        
        if item_foi_alterado_individualmente:
            houve_alteracoes = True

    # 6. Salva o arquivo
    if houve_alteracoes or registros_excluidos > 0:
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                json.dump(novos_dados, f, indent=4, ensure_ascii=False)
            msg_exclusao = f" ({registros_excluidos} registros corrompidos removidos)" if registros_excluidos > 0 else ""
            print(f"✅ CONTEÚDO CORRIGIDO: '{nome_arquivo}' padronizado e limpo!{msg_exclusao}")
        except Exception as e:
            print(f"❌ Erro ao salvar '{nome_arquivo}': {e}")
    else:
        print(f"ℹ️  Conteúdo de '{nome_arquivo}' já estava limpo e padronizado.")

def processar_arquivos_mestre(lista_nomes):
    """Chama a função de processamento para cada arquivo na lista."""
    print("\n--- 2/2: INICIANDO A LIMPEZA E PADRONIZAÇÃO DO CONTEÚDO ---")
    print("Objetivo: Remover 'unknown', padronizar horários (HH:MM) e telefones.")
    print("----------------------------------------------------------")
    
    for nome_base in lista_nomes:
        processar_arquivo(nome_base)
        
    print("----------------------------------------------------------")
    print("✅ Processo de limpeza e padronização concluído!")


# --- EXECUÇÃO PRINCIPAL ---

if __name__ == "__main__":
    
    # 0. Verifica se a biblioteca necessária está instalada
    try:
        from unidecode import unidecode
    except ImportError:
        print("----------------------------------------------------------")
        print("ERRO: A biblioteca 'unidecode' não está instalada.")
        print("Por favor, instale-a usando o comando:")
        print("pip install Unidecode")
        print("E execute o script novamente.")
        print("----------------------------------------------------------")
        exit()

    # 1. Renomeia todos os arquivos (Corrige o problema de leitura do Base44)
    renomear_arquivos(MAPPING_RENAME)
    
    # 2. Processa o conteúdo de todos os arquivos renomeados (Limpa os dados corrompidos)
    processar_arquivos_mestre(NOMES_DOS_ARQUIVOS_MESTRE)

    print("\n🎉 Processamento Total Concluído! Seus arquivos estão prontos para o Base44.")