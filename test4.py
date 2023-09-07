import json

# se abre el json con páginas y palabras prohibidas
json_forbidden = None
with open("json_actividad_http.json") as file:
    # se manejan los datos
    json_forbidden = json.load(file)

# páginas bloqueadas
blocked_sites = json_forbidden["blocked"]
# palabras prohibidas
forbidden_words = json_forbidden["forbidden_words"]

print(type(blocked_sites))
print(type(forbidden_words))