import socket


class ReplicaManager:

    def __init__(self):

        self.replicas = []

    def add_replica(self, host, port):

        replica = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        replica.connect(
            (host, port)
        )

        self.replicas.append(
            replica
        )

    def broadcast(self, data):

        dead_replicas = []

        for replica in self.replicas:

            try:

                replica.sendall(data)

            except (
                BrokenPipeError,
                ConnectionResetError
            ):

                dead_replicas.append(
                    replica
                )

        for replica in dead_replicas:

            self.replicas.remove(
                replica
            )

            replica.close()

    def close(self):

        for replica in self.replicas:

            replica.close()

        self.replicas.clear()