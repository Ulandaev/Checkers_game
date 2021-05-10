import socket

class My_socket(socket.socket):
    def __init__(self):
        super(My_socket, self).__init__(socket.AF_INET, socket.SOCK_STREAM)
    def send_data(self, data):
        raise NotImplementedError()

    def listen_socket(self, listened_socket = None):
        raise NotImplementedError()

    def set_up(self):
        raise NotImplementedError()