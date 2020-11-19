"""
Lifaw - light and fast web framework
"""
import socket
import types
from json import dumps


class Lifaw:
    """Lifaw"""
    __routes = dict()
    allowedMethods = ("GET", "POST")
    for i in allowedMethods:
        __routes[i] = dict()

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
                continue
            m, r, _= data.decode("utf-8").split("\n")[0].split()
            if m not in self.allowedMethods or r not in self.__routes[m].keys():
                conn.sendall(self.buildErrorResponse("Bad Request", 400))
            elif m in ["POST"]:
                self.handleRequestBody()
            else:
                response = self.__routes[m][r]()
                conn.sendall(response)
            if debug:
                print("REQUEST: \n" + data.decode("utf-8") + "\n")
                print("RESPONSE: \n" + response.decode("utf-8"))
            conn.close()
        s.close()
        return

    def addRoute(self, route, func, method="GET"):
        """addRoute"""
        if not isinstance(func, types.FunctionType):
            func = self.buildErrorResponse
        self.__routes[method].update({route:func})
        return

    def buildErrorResponse(self, msg="Default Error", statusCode=500):
        """buildErrorResponse"""
        msgLength = len(msg)
        h = "HTTP/1.1 %d %s \n \
            Content-Type: text/html \n \
            Content-Length: %d \n\n" % (statusCode, msg, msgLength)
        h = bytes(h, "utf-8")
        msg = bytes(msg, "utf-8")
        return h + msg

    def buildResponse(self, msg, content="text/html"):
        """buildResponse"""
        if isinstance(msg, dict):
            msg = dumps(msg)
        msgLength = len(msg)
        h = "HTTP/1.1 200 OK \n \
            Content-Type: %s \n \
            Content-Length: %x \n\n" % (content, msgLength)
        h = bytes(h, "utf-8")
        msg = bytes(msg, "utf-8")
        return h + msg

    def handleRequestBody(self):
        pass
     

if __name__ == "__main__":
    pass