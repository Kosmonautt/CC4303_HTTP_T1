import socket
import json
import sys
import aux_functions as aux

# dirección del archivo json sacado desde la terminal
dir = sys.argv[1]

# se abre el json con páginas y palabras prohibidas
json_forbidden = None
with open(dir) as file:
    # se manejan los datos
    json_forbidden = json.load(file)

# páginas bloqueadas
blocked_sites = json_forbidden["blocked"]
# palabras prohibidas
forbidden_words = json_forbidden["forbidden_words"]
# correo del ususario
user_email = json_forbidden["user"]

# tamaño del buffer del server
buff_size = 50

# puerto donde se crea el server
port = 8000

# dirección del socket server
server_adress = ('localhost', port)

# se crea el server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# se le hace bind a la dirección especificada 
server_socket.bind(server_adress)

print("Server creado!")
print("Conectar en localhost en el puerto: " + str(port))

# el server puede escuchar solo una request a la vez
server_socket.listen(1)

while True:
    print("Esperando cliente...")

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
    client_atributes["X-ElQuePregunta"] = user_email

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

    print("Sitio pedido: " + requested_url_full)

    # se checkea si la página está prohibida
    if requested_url_full in blocked_sites:
        # HTML de error 
        HTML_error = '''<!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>ERROR 403</title>
    </head>
    <body>
        <h1>Je ne sais pas!</h1>
    </body>
    </html>'''

        # mensaje con el mensaje HTTP con error
        error_HTTP = aux.create_HTML_HTTP(HTML_error)


        # mensaje de error
        error_message = "HTTP/1.1 403 \r\n\r\n"
        
        # se envia la response al cliente
        new_socket.send(error_HTTP.encode())

        # se cierra la conexión con el socket
        new_socket.close()

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
        web_response_message = aux.read_full_HTTP_message(socket_web, buff_size)

        # se transoforma el mensaje en una estrcutura
        structure_response_message = aux.parse_HTTP_message(web_response_message.decode())
        # se obtiene su HTML asociado
        web_HTML = structure_response_message[2]
        # se reemplazan las palabras prohibidas
        for t in forbidden_words:
            for key, value in t.items():
                if key in web_HTML:
                    web_HTML = web_HTML.replace(key,value)
        
        # se obtiene el json con los atributos
        web_response_message_json = structure_response_message[1]
        # atributos del json
        web_response_message_atributes = web_response_message_json["atributos"][0]
        # se cambia el largo del mensaje para que se pueda leer entero
        web_response_message_atributes["Content-Length"] = str(len(web_HTML.encode()))

        # se crea una nueva estructra HTTP con el HTML censurado y el nuevo largo
        new_structure_response_message = (structure_response_message[0],web_response_message_json,web_HTML,structure_response_message[2],structure_response_message[3])
        
        # se transforma de estrcutrua a mensaje 
        web_response_message = (aux.create_HTTP_message(new_structure_response_message)).encode()

        # se envia la response al cliente
        new_socket.send(web_response_message)

        # se cierra la conexión con el socket
        new_socket.close()
        socket_web.close()