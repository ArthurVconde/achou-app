import requests
import json

# chave da api do google (cuidado pra não divulgar)
API_KEY = "AIzaSyBYcvq1HOxKQomapjPMpwOzvZ6naBleLoY"
busca = "Floricultura em Cataguases"

# busca inicial
url_busca = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={busca}&key={API_KEY}"
resposta_busca = requests.get(url_busca).json()

# pega resultados e ordena pela nota
lugares = resposta_busca.get("results", [])
lugares.sort(key=lambda x: x.get("rating", 0), reverse=True)

lista_final = []

for lugar in lugares:
    id_lugar = lugar["place_id"]
    nota = lugar.get("rating", "Sem avaliação")
    
    # busca detalhes
    url_detalhes = (
        f"https://maps.googleapis.com/maps/api/place/details/json"
        f"?place_id={id_lugar}"
        f"&fields=name,formatted_address,formatted_phone_number,website,opening_hours"
        f"&key={API_KEY}"
    )
    detalhes = requests.get(url_detalhes).json()
    info = detalhes.get("result", {})
    
    # monta os dados
    estabelecimento = {
        "nome": info.get("name"),
        "endereco": info.get("formatted_address"),
        "telefone": info.get("formatted_phone_number"),
        "site": info.get("website"),
        "avaliacao": nota,
        "horario": info.get("opening_hours", {}).get("weekday_text", [])
    }
    
    lista_final.append(estabelecimento)

# salva o json
with open("floriculturas_cataguases.json", "w", encoding="utf-8") as arquivo:
    json.dump(lista_final, arquivo, ensure_ascii=False, indent=4)

print("Pronto! Dados salvos em floriculturas_cataguases.json")