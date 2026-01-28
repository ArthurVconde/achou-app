import json
import os
import re

def arrumar_json(arquivo_entrada, arquivo_saida=None):
    """Tenta arrumar problemas comuns em arquivos JSON"""
    
    if arquivo_saida is None:
        arquivo_saida = arquivo_entrada
    
    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as f:
            conteudo = f.read()
        
        # tira vírgulas sobrando antes de chaves/colchetes
        conteudo = re.sub(r',\s*}', '}', conteudo)
        conteudo = re.sub(r',\s*]', ']', conteudo)
        
        # se não começar com colchete, tenta arrumar
        if not conteudo.strip().startswith('['):
            objetos = re.findall(r'\{[^}]*\}(?=\s*\{|$)', conteudo, re.DOTALL)
            if objetos:
                novo_conteudo = '[\n'
                for i, obj in enumerate(objetos):
                    if i > 0:
                        novo_conteudo += ',\n'
                    novo_conteudo += obj
                novo_conteudo += '\n]'
                conteudo = novo_conteudo
        
        # arruma falta de vírgula entre objetos
        conteudo = re.sub(r'}\s*{', '},\n{', conteudo)
        
        # tira linhas em excesso
        conteudo = re.sub(r'\n\s*\n', '\n', conteudo)
        
        # tenta carregar pra ver se tá certo
        try:
            dados = json.loads(conteudo)
            
            with open(arquivo_saida, 'w', encoding='utf-8') as f:
                json.dump(dados, f, indent=4, ensure_ascii=False)
            
            print(f"Arquivo arrumado: {arquivo_entrada}")
            return True
            
        except json.JSONDecodeError as e:
            print(f"Não consegui arrumar {arquivo_entrada}: {e}")
            return False
            
    except Exception as e:
        print(f"Erro ao abrir {arquivo_entrada}: {e}")
        return False

def arrumar_todos_jsons(pasta='.'):
    """Arruma todos os JSONs na pasta"""
    arquivos_json = [f for f in os.listdir(pasta) if f.endswith('.json')]
    
    if not arquivos_json:
        print("Nenhum arquivo JSON aqui")
        return
    
    print(f"Encontrei {len(arquivos_json)} arquivos JSON")
    
    for arquivo in arquivos_json:
        caminho = os.path.join(pasta, arquivo)
        arrumar_json(caminho)

def criar_exemplo():
    """Faz um arquivo de exemplo pra comparar"""
    exemplo = {
        "empresas": [
            {
                "nome": "Loja Exemplo",
                "endereco": "Rua Teste, 123 - Centro",
                "telefone": "(32) 99999-9999",
                "site": None,
                "avaliacao": 5.0,
                "horario": "08:00 às 18:00",
                "whatsapp": "5532999999999",
                "aprovado": True
            }
        ]
    }
    
    with open('modelo_correto.json', 'w', encoding='utf-8') as f:
        json.dump(exemplo, f, indent=4, ensure_ascii=False)
    
    print("Exemplo criado: modelo_correto.json")

# programa principal
if __name__ == "__main__":
    print("Arrumador de JSON")
    print("-" * 20)
    
    while True:
        print("\nO que você quer fazer?")
        print("1 - Arrumar todos os JSONs da pasta")
        print("2 - Arrumar um arquivo específico")
        print("3 - Criar arquivo de exemplo")
        print("4 - Sair")
        
        escolha = input("Digite o número: ").strip()
        
        if escolha == '1':
            arrumar_todos_jsons()
            
        elif escolha == '2':
            nome_arquivo = input("Nome do arquivo JSON: ").strip()
            if os.path.exists(nome_arquivo):
                arrumar_json(nome_arquivo)
            else:
                print("Esse arquivo não existe!")
                
        elif escolha == '3':
            criar_exemplo()
            
        elif escolha == '4':
            print("Até mais!")
            break
            
        else:
            print("Escolha inválida!")