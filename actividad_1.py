import socket
import json

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

# esta función sirve para transformar el mensaje en una estrutura fácil de manejar
def parse_HTTP_message(http_message):
    # se crea una lista para almacenar cada línea
    lines = []
    # almacena la linea que estamos leyendo
    current_line = ''
    # para cada character en el mesnaje
    for c in http_message:
        # si es un salto de línea
        if c == '\n':
            # metemos a la lista 
            lines.append(current_line)
            current_line = ''
        else:
            # hacemos el string más largo
            current_line += c

    print(lines)






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

# recibimos el mensaje (en bytes)
message = new_socket.recv(buff_size)

parse_HTTP_message(message.decode())

# se cierra la conexión con el socket
new_socket.close()

