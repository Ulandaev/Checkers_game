from my_socket import My_socket
import threading


class Server(My_socket):
    def __init__(self):
        super(Server, self).__init__()

        print("server is listening")

        self.users = []

    def set_up(self):
        server.bind(("192.168.43.155", 54312))
        self.listen(7)
        self.accept_sockets()

    def send_data(self, data, user):
        user.send(data)

    def listen_socket(self, listened_socket, user):
        print("Listening user")

        while True:
            data = listened_socket.recv(2048)
            print(f"user sent {data}")
            if data == 0:
                break

            self.send_data(data, user)

    def accept_sockets(self):
        self.step = 0
        while True:
            user_socket, adress = self.accept()
            print(f"user <{adress[0]}> connected")
            print("it is ", user_socket)

            self.users.append(user_socket)
            print(len(self.users))
            if len(self.users) == 2 :
                for user in self.users:
                    user.send(f"{self.step}R".encode("utf-8"))
                    self.step += 1

                listened_accepted_user_1 = threading.Thread(target=self.listen_socket, args=(self.users[0],self.users[1]))
                listened_accepted_user_1.start()

                listened_accepted_user_2 = threading.Thread(target=self.listen_socket, args=(self.users[1],self.users[0]))
                listened_accepted_user_2.start()


if __name__ == "__main__":
    server = Server()
    server.set_up()























#
# import sys
# import socket
# import threading
# import time
#
# server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# server.bind(("127.0.0.1", 1234))
#
# server.listen(4)send
# print("server is listening")
#
# users = []
# def send_all(data):
#     for user in users:
#          user.send(data)
#
# def listen_user(user):
#     print("listening user")
#     while True:
#         data = user.recv(2048)
#         print(f"User sent {data}")
#         send_all(data)
#
# def start_server():
#     while True:
#
#         user_socket , adress = server.accept()
#         print(f"user {adress[0]} connected!")
#         users.append(user_socket)
#         listen_accepted_user = threading.Thread(target=listen_user, args=(user_socket,))
#         listen_accepted_user.start()
#         a = input()
#         print(a)
#
#
#
# if __name__ == '__main__':
#     start_server()
#
#
#
#
#
#
