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

# se abre el json con páginas y palabras prohibidas
forbidden = None
with open("json_actividad_http.json") as file:
    # se manejan los datos
    forbidden = json.load(file)

# tamaño del buffer del server
buff_size = 50

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
client_message = aux.read_full_HTTP_message(new_socket, buff_size)

# transformamos la request del cliente en algo maejable
client_request = aux.parse_HTTP_message(client_message.decode())

# se obtiene el json con los atributos
client_json = client_request[1]

# atributos del json
client_atributes = client_json["atributos"][0]

requested_url = client_atributes["Host"]

# print(client_request[0])

# # conseguimos la linea con la URL deseada
# requested_url = client_request[0]
# # se divide por los espacios en blanco
# requested_url = requested_url.split()
# # elegimos la linea después de get (la URL)
# requested_url = requested_url[1]
# # se "limpia"
# requested_url = requested_url.strip()
# # se elige lo que está después de "http://"
# requested_url = requested_url[7:len(requested_url)]
# # si hay un "/" al final, se borra
# if requested_url[len(requested_url)-1] == "/":
#     requested_url = requested_url[0:len(requested_url)-1]

print(requested_url)

# se crea un nuevo socket para conextarse con la página web
socket_web = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# adress de la página web
adress_web = (requested_url, 80)

# se conecta a la página web
socket_web.connect(adress_web)

# se envia la request del cliente
socket_web.send(client_message)

#respuesta de la página web
#web_response_message = socket_web.recv(4000)
web_response_message = aux.read_full_HTTP_message(socket_web, buff_size)

# se envia la response al cliente
new_socket.send(web_response_message)

# se cierra la conexión con el socket
new_socket.close()