import socket  # noqa: F401
import threading

def handle_client(contact):
    request = contact.recv(1024).decode()
    print(f"Received request:\n{request}")
    
    lines = request.split("\r\n")
    if not lines or len(lines[0].split()) < 3:
        contact.close()
        return

    request_line = lines[0]
    method, path, _ = request_line.split()

    response = ''

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

    elif path != "/user-agent" and path != "/echo/" and path == '/':
        response = "HTTP/1.1 200 OK\r\n\r\n"

    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"

    contact.sendall(response.encode())
    contact.close()    

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(10)

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'New connection from {client_address}')
        thread = threading.Thread(target=handle_client, args=(client_socket,))
        thread.start()

if __name__ == "__main__":
    main()
