import aux_functions as aux


message2 = '''HTTP/1.1 200 OK\r
Server: nginx/1.17.0\r
Date: Mon, 21 Aug 2023 16:50:39 GMT\r
Content-Type: text/html; charset=utf-8\r
Content-Length: 237\r
Connection: keep-alive\r
Access-Control-Allow-Origin: *\r
\r
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>CC4303</title>
</head>
<body>
    <h1>Bienvenide ... oh? no puedo ver tu nombre :c!</h1>
    <h3><a href="replace">¿Qué es un proxy?</a></h3>
</body>
</html>'''

structure = aux.parse_HTTP_message(message2)

old_HTTP = aux.create_HTTP_message(structure)

# json con atributos
json = structure[1]
# atributos del json
atributes = json["atributos"][0]

#print(atributes)

atributes["X-ElQuePregunta"] = "CONCHETUMARE CULAIO"

new_structure = (structure[0], json, structure[2], structure[3])

new_HTTP = aux.create_HTTP_message(new_structure)

print(old_HTTP)
print("////////")
print(new_HTTP)
