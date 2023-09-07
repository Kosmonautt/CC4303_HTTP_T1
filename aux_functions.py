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

    # dice si se leyó al menos la HEAD del mensaje HTTP
    head_read = False

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
                # se confirma que que se leyó todo el head
                head_read = True
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

        # caso problemático debido a los "" presentes, no permite hacer el json.dump correctamente
        if(line_atribute=="Etag"):
            continue

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
    return (first_line, info_json, html_message, head_read) 

# esta función toma la estructura y la retorna como un mensaje HTTP
def create_HTTP_message(sctructure):
    # linea con GET/POST
    first_line = sctructure[0]
    # json con atributos
    json = sctructure[1]
    # mensaje HTML (si es que tiene)
    HTML_message = sctructure[2]
    
    # mensaje HTTP, inicialmente vacío
    HTTP_message = ''

    HTTP_message += first_line + "\r\n"

    # atributos del json
    atributes = json["atributos"][0]

    for key, value in atributes.items():
        HTTP_message += key + ": " + value + "\r\n"
    
    # última linea del HEAD
    HTTP_message += "\r\n"

    # si tiene el atributo de content length
    if 'Content-Length' in atributes.keys():
        # se comprueba que el largo sea igual al del mensaje
        assert(int(atributes['Content-Length']) == len((HTML_message).encode()))

        # se concatena el mensaje
        HTTP_message += HTML_message

    # se retorna el mensaje final
    return HTTP_message

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
    strcuture = (first_line, info_json, HTML_message, True)
    
    # se retorna el mensaje ya creado
    return create_HTTP_message(strcuture)

# función que verifica si un mensaje HTTP ha sido leído por completo
# def read_fully(message):
#     try:
#         # se pasa a una escructura
#         structure = parse_HTTP_message(message)
#         # verificamos si llegó el mensaje completo o si aún faltan partes del mensaje

#         if(structure[3]):   # si se ha leaído todo el HEAD
#             # json con atributos
#             json = structure[1]
#             # atributos del json
#             atributes = json["atributos"][0]
#             # si no hay mensaje HTTP
#             if not 'Content-Length' in atributes.keys():
#                 # entonces ya se leyó todo el mensaje
#                 return True
#             # largo que indica el mensaje HTTP (en bytes)
#             largo_HTTP = int(atributes['Content-Length'])
#             # largo del mensaje real (en bytes)
#             largo_real = (structure[2]).encode()
#             # si los largos coinciden
#             if(largo_real >= largo_HTTP):
#                 return True
#         else:
#             return False
#     # si ocurre cualquier tipo de error entonces no tenía la forma apropiada
#     except:
#         return False
def read_fully(message):
    try:
        message = message.decode()
    except:
        return False

    try:
        # se pasa a una escructura
        structure = parse_HTTP_message(message)
        # verificamos si llegó el mensaje completo o si aún faltan partes del mensaje
    except:
        return False

    if(structure[3]):   # si se ha leaído todo el HEAD
        # json con atributos
        json = structure[1]
        # atributos del json
        atributes = json["atributos"][0]
        # si no hay mensaje HTTP
        if not 'Content-Length' in atributes.keys():
            # entonces ya se leyó todo el mensaje
            return True
        # largo que indica el mensaje HTTP (en bytes)
        largo_HTTP = int(atributes['Content-Length'])
        # largo del mensaje real (en bytes)
        largo_real = len((structure[2]).encode())
        # si los largos coinciden
        if(largo_real >= largo_HTTP):
            return True
    else:
        return False


# función que recibe un mensaje HTTP completo
def read_full_HTTP_message(connection_socket, buff_size):
    # recibimos la primera parte del mensaje
    recv_message = connection_socket.recv(buff_size)
    full_message = recv_message

    # verificamos si llegó el mensaje completo o si aún faltan partes del mensaje
    is_end_of_message = read_fully(full_message.decode())

    # entramos a un while para recibir el resto y seguimos esperando información
    # mientras no esté leído por completo
    while not is_end_of_message:
        # recibimos un nuevo trozo del mensaje
        recv_message = connection_socket.recv(buff_size)

        # lo añadimos al mensaje "completo"
        full_message += recv_message

        # verificamos si es la última parte del mensaje
        is_end_of_message = read_fully(full_message)

    # finalmente retornamos el mensaje
    return full_message
    
        
