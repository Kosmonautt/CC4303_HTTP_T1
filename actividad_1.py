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
json_forbidden = None
with open("json_actividad_http.json") as file:
    # se manejan los datos
    json_forbidden = json.load(file)

# páginas bloqueadas
blocked_sites = json_forbidden["blocked"]
# palabras prohibidas
forbidden_words = json_forbidden["forbidden_words"]

# tamaño del buffer del server
buff_size = 50

# dirección del socket server
server_adress = ('localhost', 8002)

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

# se agrega el que pregunta (esto solo cambia la estructura, aún no se modifica el mensaje)
client_atributes["X-ElQuePregunta"] = "Ksmnt"

# la url del host del sitio que se pidió
requested_url = client_atributes["Host"]

# conseguimos la linea con la URL pedida por el usuario
requested_url_full = client_request[0]
# se divide por los espacios en blanco
requested_url_full = requested_url_full.split()
# elegimos la linea después de get (la URL)
requested_url_full = requested_url_full[1]
# se "limpia"
requested_url_full = requested_url_full.strip()

# se checkea si la página está prohibida
if requested_url_full in blocked_sites:
    pass

else:
    # se crea un nuevo socket para conextarse con la página web
    socket_web = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # adress de la página web
    adress_web = (requested_url, 80)

    # como no es una página prohiida se agrega el que pregunta
    new_client_request = (client_request[0], client_json, client_request[2], client_request[3])
    # la estructura se transforma en un mensaje HTTP
    client_message = (aux.create_HTTP_message(new_client_request)).encode()

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