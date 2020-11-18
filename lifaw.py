"""
Lifaw - light and fast web framework
"""
import socket


class Lifaw:
    """Lifaw"""
    __routes = dict()
    __routes["GET"] = dict()
    __routes["POST"] = dict()

    def serveApp(self, host, port, debug=False):
        """serveApp"""
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()
        while True:
            conn, addr = s.accept()
            print('Connection received:', addr)
            data = conn.recv(1024)
            if not data:
                return
            m, r, _= data.decode("utf-8").split("\n")[0].split()
            if m in self.__routes.keys() and r in self.__routes[m].keys():
                response = self.__routes[m][r]()
                conn.sendall(response)
            else:
                conn.sendall(self.returnError())
            if debug:
                print("REQUEST: \n" + data.decode("utf-8") + "\n")
                print("RESPONSE: \n" + response.decode("utf-8"))
            conn.close()
        s.close()
        return

    def addRoute(self, route, func, method="GET"):
        """addRoute"""
        self.__routes[method].update({route:func})
        return

    def returnError(self):
        msg = b"ERROR"
        dataLength = len(msg)
        h = b"HTTP/1.1 500 An Error has occurred\n \
            Content-Type: text/html; charset=UTF-8\n \
            Content-Length: %x \n\n" % dataLength
        return h + msg


if __name__ == "__main__":
    pass