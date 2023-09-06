import socket
import json
import aux_functions as aux

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

# esta función toma la estructura y la retorna como un mensaje HTTP
def create_HTTP_message_HTML(HTML_message):
    # linea con POST
    first_line = 'HTTP/1.1 200 OK'
    # json/diccionario con atributos
    dicc = {}

    dicc['Server'] = ' localhost'
    dicc['Date'] = ' Sun, 20 Aug 2023 21:04:28 GMT'
    dicc['Content-Type'] = ' text/html; charset=utf-8'
    dicc['Content-Length'] = str(len(HTML_message))
    dicc['Connection'] = ' keep-alive'
    dicc['Access-Control-Allow-Origin'] = ' *'
    
    # mensaje HTTP, inicialmente vacío
    HTTP_message = ''

    HTTP_message += first_line + "\r\n"

    for key, value in dicc.items():
        HTTP_message += key + ": " + value + "\r\n"
    
    HTTP_message += "\r\n"

    HTTP_message += HTML_message

    return HTTP_message

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

# guardamos el resultado del mensaje

result = aux.parse_HTTP_message(message.decode())

new_HTTP_message = create_HTTP_message_HTML(HTML_message)

# print("Mensaje original: \n")
# print(message.decode())

# print("Mensaje parseado: \n")
# print(new_HTTP_message)

# print(len(message.decode()))
# print('\n')
# print(len(new_HTTP_message))

#print(message.decode() == new_HTTP_message)

new_socket.send(new_HTTP_message.encode())

# se cierra la conexión con el socket
new_socket.close()

