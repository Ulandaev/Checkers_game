from my_socket import My_socket
import threading, sys, socket


class Server(My_socket):

    k = 0
    stop = True
    def __init__(self):
        super(Server, self).__init__()

        print("server is listening")

        self.users = []

    def set_up(self):
        #192.168.43.155
        self.bind(("127.0.0.1", 54325))
        self.listen(7)
        self.accept_sockets()
        self.shutdown(socket.SHUT_RDWR)
        self.close()
        

    def send_data(self, data, user):
        user.send(data)

    def listen_socket(self, listened_socket, user):
        print("Listening user")


        while self.stop:
            data = listened_socket.recv(2048)
            print(f"user sent {data}")
            if data == 0:
                break

            self.send_data(data, user)
            if user == self.users[1]:
                self.k += 1
            elif user == self.users[0]:
                self.k -= 1
            print(self.k)

            if self.k > 3 or self.k < -1:

                # self.send_data(self.data_error, self.users[0])
                # self.send_data(self.data_error, self.users[1])

                self.stop = False
                if user == self.users[0]:
                    self.data_error = "0000E"
                    self.data_error = self.data_error.encode("utf-8")
                    self.users[0].send(self.data_error)
                    # self.users[1].send(self.data_error)
                elif user == self.users[1]:
                    self.data_error = "0000E"
                    self.data_error = self.data_error.encode("utf-8")
                    # self.users[0].send(self.data_error)
                    self.users[1].send(self.data_error)
                # self.close()


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

                print(self.users[0])
                print(self.users[1])


                listened_accepted_user_1 = threading.Thread(target=self.listen_socket, args=(self.users[0],self.users[1]))
                listened_accepted_user_1.start()


                listened_accepted_user_2 = threading.Thread(target=self.listen_socket, args=(self.users[1],self.users[0]))
                listened_accepted_user_2.start()
                listened_accepted_user_1.join()
                listened_accepted_user_2.join()
                print("close s")
                break
                # server.close()


if __name__ == "__main__":
    server = Server()
    server.set_up()
    # server.close()
    print("success")
    sys.exit()


