import socket
import json

SV_HOST = "127.0.0.1"
SV_PORT = 5000


def send_task(client_socket, task):
    message = json.dumps(task) + "\n"
    client_socket.sendall(message.encode("utf-8"))
    buffer = ""

    while "\n" not in buffer:
        data = client_socket.recv(4096)

        if not data:
            raise ConnectionError("Servidor apagado")

        buffer += data.decode("utf-8")

    response, _ = buffer.split("\n", 1)
    return json.loads(response)


def client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((SV_HOST, SV_PORT))

        while True:
            description = input("\nEscribir descripcion o 'salir': ")

            if description.lower() == "salir":
                break

            task = {"id": 1, "descripcion": description}

            result = send_task(client_socket, task)

            print("Resultado:")
            print(json.dumps(result, indent=4, ensure_ascii=False))

    except ConnectionError as error:
        print(f"Error de la conexión: {error}")

    finally:
        client_socket.close()
        print("Conexión cerrada.")


if __name__ == "__main__":
    client()
