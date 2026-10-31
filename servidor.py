import socket
import json
import threading
from concurrent.futures import ThreadPoolExecutor
from threading import Lock

HOST = "127.0.0.1"
PORT = 5000
WORKERS = 4

worker_pool = ThreadPoolExecutor(max_workers=WORKERS)
print_lock = Lock()


def process_task(task):
    task_id = task.get("id")
    description = task.get("descripcion", "")

    with print_lock:
        print(f"Procesando tarea {task_id}: {description}")

    result = description.upper()

    return {"id": task_id, "resultado": result, "estado": "completada"}


def handle_client(client_socket):
    try:
        buffer = ""

        while True:
            # Explicado en el TP2
            data = client_socket.recv(4096)
            if not data:
                break

            buffer += data.decode("utf-8")

            # Acomoda el input para ser usado (deserialización).
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)

                if not line.strip():
                    continue

                task = json.loads(line)
                print(f"Tarea recibida: {task}")

                # https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Executor.submit
                # Agrega la función a ejecutar en la pool de workers y devuelve un objeto Future (https://docs.python.org/3/library/concurrent.futures.html#concurrent.futures.Future)
                # Se le pasa el handler y la tarea como parametros.
                future = worker_pool.submit(process_task, task)
                result = future.result()

                # Explicado en el TP2
                response = json.dumps(result) + "\n"
                client_socket.sendall(response.encode("utf-8"))

    except (ConnectionError, json.JSONDecodeError) as error:
        print(f"Error del cliente: {error}")

    finally:
        client_socket.close()


def server():
    # Explicado en el TP2
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Agregado por la devolución del TP1
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print(f"Servidor escuchando en el puerto {PORT}")
    print(f"Cantidad de workers: {WORKERS}")

    try:
        while True:
            client_socket, address = server_socket.accept()

            # Crea un hilo para cada conexión y lo manda a handle_client
            # https://docs.python.org/3/library/threading.html#threading.Thread
            # Cada hilo se marca como Daemon para que el servidor se pueda cerrar aunque queden hilos vivos.
            threading.Thread(
                target=handle_client, args=(client_socket,), daemon=True
            ).start()

    except KeyboardInterrupt:
        print("\nSaliendo...")

    finally:
        server_socket.close()
        worker_pool.shutdown(wait=True)


if __name__ == "__main__":
    server()
