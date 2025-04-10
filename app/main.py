import socket  # noqa: F401
import threading
import os
import sys
import argparse

directory = None


if "-- directory" in sys.argv:
    dir_index = sys.argv.index("--directory") + 1
    if dir_index < len(sys.argv):
        directory = sys.argv[dir_index]
        
def handle_client(contact, directory):
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
        
    elif path.startswith("/files/"):
        filename = path[len("/files/"):]
        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                content = f.read()

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/octet-stream\r\n"
                f"Content-Length: {len(content)}\r\n"
                "\r\n"
            ).encode() + content
        else:
            response = "HTTP/1.1 404 Not Found\r\n\r\n".encode()

        contact.sendall(response)
        contact.close()
        return  # Exit early so we don’t run the rest
                
                
    if path != "/user-agent" and path != "/echo/" and path == '/':
        response = "HTTP/1.1 200 OK\r\n\r\n"
            
    else:
        response = "HTTP/1.1 404 Not Found\r\n\r\n"

    contact.sendall(response.encode())
    contact.close()    

def main():
    import argparse
    import os

    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", required=True)
    args = parser.parse_args()
    directory = args.directory

    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    server_socket.listen(10)

    while True:
        contact, addr = server_socket.accept()
        print(f'New connection from {addr}')
        thread = threading.Thread(target=handle_client, args=(contact, directory))
        thread.start()

if __name__ == "__main__":
    main()
