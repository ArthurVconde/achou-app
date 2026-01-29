import requests
import json

API_KEY = "AIzaSyBYcvq1HOxKQomapjPMpwOzvZ6naBleLoY"
busca = "Advogado em Cataguases"

# faz a busca inicial
url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={busca}&key={API_KEY}"
resposta = requests.get(url).json()

# pega os resultados e ordena pela avaliação
resultados = resposta.get("results", [])
resultados.sort(key=lambda x: x.get("rating", 0), reverse=True)

advogados = []

for lugar in resultados:
    id_lugar = lugar["place_id"]
    nota = lugar.get("rating", 0)
    
    # busca mais detalhes
    url_detalhes = (
        f"https://maps.googleapis.com/maps/api/place/details/json"
        f"?place_id={id_lugar}"
        f"&fields=name,formatted_address,formatted_phone_number,website,opening_hours"
        f"&key={API_KEY}"
    )
    detalhes = requests.get(url_detalhes).json()
    info = detalhes.get("result", {})
    
    # monta o dicionário no formato que o sistema precisa
    escritorio = {
        "name": info.get("name"),
        "address": info.get("formatted_address"),
        "phone": info.get("formatted_phone_number"),
        "website": info.get("website"),
        "rating": nota,
        "hours": info.get("opening_hours", {}).get("weekday_text", [])
    }
    
    advogados.append(escritorio)

# salva os dados
with open("advogados_cataguases.json", "w", encoding="utf-8") as arquivo:
    json.dump(advogados, arquivo, ensure_ascii=False, indent=4)

print("Lista de advogados salva com sucesso!")