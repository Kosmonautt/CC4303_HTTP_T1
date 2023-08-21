import json

# esta función se encarga de recibir el mensaje completo desde el cliente
# en caso de que el mensaje sea más grande que el tamaño del buffer 'buff_size', esta función va esperar a que
# llegue el resto. Para saber si el mensaje ya llegó por completo, se busca el caracter de fin de mensaje (parte de nuestro protocolo inventado)

def receive_full_mesage(connection_socket, buff_size, end_sequence):
    # recibimos la primera parte del mensaje
    recv_message = connection_socket.recv(buff_size)
    full_message = recv_message

    # verificamos si llegó el mensaje completo o si aún faltan partes del mensaje
    is_end_of_message = contains_end_of_message(full_message.decode(), end_sequence)

    # entramos a un while para recibir el resto y seguimos esperando información
    # mientras el buffer no contenga secuencia de fin de mensaje
    while not is_end_of_message:
        # recibimos un nuevo trozo del mensaje
        recv_message = connection_socket.recv(buff_size)

        # lo añadimos al mensaje "completo"
        full_message += recv_message

        # verificamos si es la última parte del mensaje
        is_end_of_message = contains_end_of_message(full_message.decode(), end_sequence)

    # removemos la secuencia de fin de mensaje, esto entrega un mensaje en string
    full_message = remove_end_of_message(full_message.decode(), end_sequence)

    # finalmente retornamos el mensaje
    return full_message


def contains_end_of_message(message, end_sequence):
    return message.endswith(end_sequence)


def remove_end_of_message(full_message, end_sequence):
    index = full_message.rfind(end_sequence)
    return full_message[:index]

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

# esta función toma un texto HTML y crea un mensaje HTTP adecuado 
def create_HTML_HTTP(HTML_message, name=None):
    # linea con POST
    first_line = 'HTTP/1.1 200 OK'

    # se saca el largo del HTML
    len_HTML = str(len(HTML_message.encode()))

    # json con los atributos
    info_json = '''{
        "atributos": [
            {
                "Server":" localhost",
                "Date": " Sun, 20 Aug 2023 21:04:28 GMT",
                "Content-Type": " text/html; charset=utf-8",
                "Content-Length": " '''
    
    info_json += len_HTML
    
    if name:
        info_json += '''",
                    "Connection": " keep-alive",
                    "Access-Control-Allow-Origin": " *",
                    "X-ElQuePregunta": "'''

        info_json += name
        
        info_json+='''"
                }
            ]
        }'''
    else:
        info_json += '''",
            "Connection": " keep-alive",
            "Access-Control-Allow-Origin": " *"
                }
            ]
        }'''


    # se pasa de strings a formato json (diccionario de python)
    info_json = json.loads(info_json)

    # se crea la estrucutra
    strcuture = (first_line, info_json, HTML_message)
    

    # se retorna el mensaje ya creado
    return create_HTTP_message(strcuture)