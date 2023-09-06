import socket
import json
import sys
import aux_functions as aux

# dirección del archivo json sacado desde la terminal
dir = sys.argv[1]

# se abre el archivo con el nombre
with open(dir) as file:
    # se manejan los datos
    data = json.load(file)
    # se obtiene el nombre
    name = data['name']

# mensaje que se mostrará en el navegador
HTML_message = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Página de prueba</title>
</head>
<body>
    <h1>Hola, esta es una prueba de página para requests con sockets!</h1>
</body>
</html>'''

# tamaño del buffer del server
buff_size = 1024

# dirección del socket server
server_adress = ('localhost', 8001)

# se crea el server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# se le hace bind a la dirección especificada 
server_socket.bind(server_adress)

# el server puede escuchar solo una request a la vez
server_socket.listen(1)

# se espera una request, cuando se recibe se 
# crea un nuevo socket 
new_socket, new_adress = server_socket.accept()

# recibimos el mensaje (en bytes)
message = new_socket.recv(buff_size)

# guardamos el la request del buscador
result = aux.parse_HTTP_message(message.decode())

# se crea el mensaje que se enviará al neavegador
new_HTTP_message = aux.create_HTML_HTTP(HTML_message, name)

# se envía el mensaje al navegador
new_socket.send(new_HTTP_message.encode())

# se cierra la conexión con el socket
new_socket.close()

