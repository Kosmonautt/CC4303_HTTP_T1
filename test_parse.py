import socket
import json
import aux_functions as aux

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

print(message == message)

print(message2 == message2)


print(message == aux.create_HTTP_message(aux.parse_HTTP_message(message)))

print(message2 == aux.create_HTTP_message(aux.parse_HTTP_message(message2)))


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