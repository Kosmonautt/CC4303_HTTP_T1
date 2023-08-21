import socket
import json

# esta función divide un string por el primer carácter ":" que encuentra
def divide_by_colon(texto):
    # se divide por el ":"
    texto = texto.split(":")

    # la primera parte del texto antes del :
    texto_1 = texto[0]

    # todos después del primer :
    texto_2 = ''

    for i in range(1, len(texto)):
        texto_2 += texto[i]
        # si no es el ultimo, se agrega el :
        if(i+1 != len(texto)):
            texto_2 += ":"
    
    return texto_1, texto_2

# esta función sirve para transformar el mensaje en una estrutura fácil de manejar
def parse_HTTP_message(http_message):
    # se crea una lista para almacenar cada línea
    lines = []
    # almacena la linea que estamos leyendo
    current_line = ''

    # largo del mensaje HTTP
    mssg_len = len(http_message)

    # mensaje html (si es que tiene)
    html_message = ''

    i = 0

    while i < mssg_len:
        # si se llega a un fin de una línea
        if http_message[i] == '\r':
            # el carácter que viene después es '\n' así 
            # que se salta
            i += 2
            # se agrega a la lista
            lines.append(current_line)
            # se borra la current line
            current_line = ''
            # si hay otra '\r' después de '\n' se está al final del HEAD
            if http_message[i] == '\r':
                # se avanza hasta el \n
                i +=1
                # si se llega al final del string, entonces no hay mensaje HTML
                if i+1 == mssg_len:
                    break
                else:
                    # se salta el \n
                    i+=1
                    # se guarda el mensaje html
                    while i < mssg_len:
                        html_message += http_message[i]
                        i+=1
        else:
            # se agrega el carácter al string
            current_line += http_message[i]
            i += 1
    
    # linea co el GET/POST
    first_line = lines[0]

    # lineas con atributos en formato json 
    info_json = '''{ 
        "atributos": [ 
            { 
    '''

    len_lines = len(lines)

    for i in range(1, len_lines):
        # linea
        line = lines[i]

        # se divide la línea por el primer ":"
        divided_by_colon = divide_by_colon(line)

        # se consigue las dos partes del string
        line_atribute = divided_by_colon[0]
        line_content = divided_by_colon[1].strip()

        # se formatea el mensaje con forma de json
        if(i+1 == len_lines):
            line_string = '"' + line_atribute + '":"' + line_content + '"\n'
        else:
            line_string = '"' + line_atribute + '":"' + line_content + '", \n'
        info_json += line_string
    
    info_json += ''' }
     ]
    } '''

    # se pasa de strings a formato json (diccionario de python)
    info_json = json.loads(info_json)

    # se retorna la primer línea y el json con los atributos
    return (first_line, info_json, html_message) 

# esta función toma la estructura y la retorna como un mensaje HTTP
def create_HTTP_message(sctructure):
    # linea con GET/POST
    first_line = sctructure[0]
    # json con atributos
    json = sctructure[1]
    # mensaje HTML (si es que tiene)
    HTML_message = sctructure[2]
    
    # mensaje HTTP, inicialmente vacío
    HHTP_message = ''

    HHTP_message += first_line + "\r\n"

    # atributos del json
    atributes = json["atributos"][0]

    for key, value in atributes.items():
        HHTP_message += key + ": " + value + "\r\n"
    
    # última linea del HEAD
    HHTP_message += "\r\n"

    # si tiene el atributo de content length
    if 'Content-Length' in atributes.keys():
        # se saca el largo del mensaje en bytes
        len_HTML = len(HTML_message)
        # se recorre el mensaje
        for i in range(0, len_HTML):
            HHTP_message += HTML_message[i]
    return HHTP_message

message = '''GET / HTTP/1.1\r
Host: localhost:8000\r
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0\r
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8\r
Accept-Language: en-US,en;q=0.5\r
Accept-Encoding: gzip, deflate, br\r
Connection: keep-alive\r
Upgrade-Insecure-Requests: 1\r
Sec-Fetch-Dest: document\r
Sec-Fetch-Mode: navigate\r
Sec-Fetch-Site: none\r
Sec-Fetch-User: ?1\r
\r
'''

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

# # tamaño del buffer del server
#buff_size = 1024

# # dirección del socket server
#server_adress = ('localhost', 8001)

# # se crea el server
#server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# # se le hace bind a la dirección especificada 
#server_socket.bind(server_adress)

# # el server puede escuchar solo una request a la vez
#server_socket.listen(1)

# se espera una request, cuando se recibe se 
# crea un nuevo socket 
# new_socket, new_adress = server_socket.accept()

print(message == create_HTTP_message(parse_HTTP_message(message)))

# recibimos el mensaje (en bytes)
#message = new_socket.recv(buff_size)

# guardamos el resultado del mensaje

#print(create_HTTP_message(parse_HTTP_message(message.decode())))



#new_HTTP_message = create_HTTP_message(result)

# print("Mensaje original: \n")
# print(message.decode())

# print("Mensaje parseado: \n")
# print(new_HTTP_message)

# print(len(message.decode()))
# print('\n')
# print(len(new_HTTP_message))

#print(message.decode() == new_HTTP_message)

# se cierra la conexión con el socket
# new_socket.close()