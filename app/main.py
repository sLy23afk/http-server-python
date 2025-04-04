import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
  
  
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(5)
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f'New connection from {client_address}')
        request = client_socket.recv(1024).decode()
        print(f"Received request: \n {request}")
        
        lines = request.split("\r\n")
        request_line = lines[0]
        method, path, _ = request_line.split()
        
        
        if path.startswith("/echo/"):
            echo_text = path[len("/echo/"):]  # Get the part after "/echo/"
            content_length = len(echo_text)

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {content_length}\r\n"
                "\r\n"
                f"{echo_text}"
                 )
            
        elif path == "/user-agent":
            user_agent = ""
            for line in lines:
                if line.lower().startswith("user-agent:"):
                    user_agent = line[len("User-Agent:"):].strip()
                    break

            content_length = len(user_agent)
            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: text/plain\r\n"
                f"Content-Length: {content_length}\r\n"
                "\r\n"
                f"{user_agent}"
            )
        elif path == 2:
            response = "HTTP/1.1 200 OK\r\n\r\n"
        
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n"

        client_socket.sendall(response.encode())
        client_socket.close()
        

if __name__ == "__main__":
    main()
