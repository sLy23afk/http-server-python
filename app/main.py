import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    HOST = "localhost"
    PORT = 4221
 
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f'Server is running on {HOST}:{PORT}')
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f'New connection from {client_address}')
        request = client_socket.recy(1024)
        print(f"Received request: {request.decode()}")
        
        response = "HTTP/1.1 200 OK\r\n\r\n"
        client_socket.send(response.encode())
        client_socket.close()
        

if __name__ == "__main__":
    main()
