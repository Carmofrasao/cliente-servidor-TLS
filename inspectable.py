# Código externo utilizado para alterar byte enviado por SSL 
# 
# Fonte: 
# https://gitlab.com/fer22f/leilaloes/-/blob/main/inspectable/inspectable.py

from ssl import MemoryBIO, SSLEOFError, SSLWantReadError, SSLWantWriteError
from socket import SHUT_RDWR
import time

def hexdump(b):
    n = 0
    while n < len(b):
        # Hex string
        s1 = " ".join(f"{i:02x}" for i in b[n : n + 16])
        # Extra space between groups of 8 hex values
        s1 = s1[0:23] + " " + s1[23:]
        # ASCII string, when not in range, output "."
        s2 = "".join(chr(i) if 32 <= i <= 127 else "." for i in b[n : n + 16])

        print(f"{n:08x}: {s1:<48}  {s2}")
        n += 16


class InspectableListenerSocket:
    def __init__(self, listener_socket, context, **kwargs):
        self.listener_socket = listener_socket
        self.context = context
        self.kwargs = kwargs

    def accept(self):
        socket, address = self.listener_socket.accept()
        socket = InspectableSocket(socket, self.context, **self.kwargs)
        socket.do_handshake()
        return socket, address

    def close(self):
        self.listener_socket.close()

    def shutdown(self, how: int):
        self.listener_socket.shutdown(how)


class InspectableSocket:
    def __init__(self, socket, context, allow_editing=False, **kwargs):
        self.socket = socket
        # In the handshake, we need to read before writing, for reasons
        # that are explained further below. However, if the socket was blocking,
        # we would potentially get stuck, waiting for a message that never arrives.
        # So instead of that, we work with non-blocking sockets and their issues.
        self.socket.setblocking(False)
        self.context = context
        self.allow_editing = allow_editing
        self.incoming = MemoryBIO()
        self.outgoing = MemoryBIO()
        self.ssl_object = self.context.wrap_bio(self.incoming, self.outgoing, **kwargs)

    def handle_incoming(self, n_bytes=1024):
        try:
            data = self.socket.recv(n_bytes)
        except BlockingIOError:
            # Avoids a busy loop that consumes 100% of CPU resources
            time.sleep(0.01)
            return 0

        if len(data) == 0:
            # When recv returns an empty string, the socket has been closed
            return -1
        return self.incoming.write(data)

    def handle_outgoing(self):
        data = self.outgoing.read()
        if len(data) == 0:
            return
        print("========== send:  ssl ==========")
        hexdump(data)
        # We use sendall instead of send to make sure all data is sent
        self.socket.sendall(self.edit_data(data))

    def edit_data(self, original_data):
        if not self.allow_editing:
            return original_data
        answer = input("Do you want to edit this message? [y/N] ")
        if answer[:1].lower() == "y":
            index = int(input("Enter the index in hexadecimal: "), 16)
            byte = int(input("Enter the byte in hexadecimal: "), 16)
            data = original_data[:index] + bytes([byte]) + original_data[index + 1 :]
            print("========= send: edited =========")
            hexdump(data)
            return data
        return original_data

    def do_handshake(self):
        # The do_handshake method should be repeatedly called until
        # the handshake is complete. When it needs to write or read,
        # it raises their respective Errors. As per documentation,
        # before writing, we should check if there is something to read,
        # and before reading, we should check if there is something to write.
        while True:
            try:
                self.ssl_object.do_handshake()
                break
            except SSLWantWriteError:
                if self.handle_incoming() == -1:
                    raise SSLEOFError()
                self.handle_outgoing()
            except SSLWantReadError:
                self.handle_outgoing()
                if self.handle_incoming() == -1:
                    raise SSLEOFError()
        # Important to make sure that the handshake is completed
        self.handle_outgoing()
        print(f"Cipher: {self.ssl_object.cipher()}")

    def recv(self, n_bytes):
        while True:
            try:
                data = self.ssl_object.read(n_bytes)
                return data
            except SSLWantReadError:
                # This may happen if the SSL message has been chunked
                if self.handle_incoming() == -1:
                    return b""

    def send(self, data):
        print("======== send: original ========")
        hexdump(data)
        # There is no loop to send here; since TLS writes into a buffer
        # that resizes automatically, it is never expected to fail.
        self.ssl_object.write(data)
        self.handle_outgoing()

    def close(self):
        self.socket.close()
