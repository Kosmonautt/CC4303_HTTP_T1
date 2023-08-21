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

# tamaño del buffer del server
buff_size = 1024

# dirección del socket server
server_adress = ('localhost', 8000)

# se crea el server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# se le hace bind a la dirección especificada 
server_socket.bind(server_adress)

# el server puede escuchar solo una request a la vez
server_socket.listen(1)

# se espera una request, cuando se recibe se 
# crea un nuevo socket 
new_socket, new_adress = server_socket.accept()

# recibimos la request (en bytes)
client_message = new_socket.recv(buff_size)

# transformamos la rquest del cliente en algo maejable
client_request = aux.parse_HTTP_message(client_message.decode())

# conseguimos la linea con la URL deseada
requested_url = client_request[0]
# se divide por los espacios en blanco
requested_url = requested_url.split()
# elegimos la linea después de get (la URL)
requested_url = requested_url[1]
# se "limpia"
requested_url = requested_url.strip()

# se crea un nuevo socket para conextarse con la página web
socket_web = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print(requested_url)

# adress de la página web
adress_web = ('example.com', 80)

# se conecta a la página web
socket_web.connect(adress_web)

# se envia la request del cliente
socket_web.send(client_message)

# respuesta de la página web
web_response_message = socket_web.recv(buff_size*2)

# se envia la response al cliente
new_socket.send(web_response_message)

# se cierra la conexión con el socket
new_socket.close()