from lifaw import Lifaw

a = Lifaw()

def buildPlainResponse(data):
    dataLength = len(data)
    h = b"HTTP/1.1 200 OK\n \
          Content-Type: text/plain; charset=UTF-8\n \
          Content-Length: %x \n\n" % dataLength
    return h + data

def index():
    data = b"landing page"
    return buildPlainResponse(data)

def hello():
    data = b"juan rules!!"
    return buildPlainResponse(data)

a.addRoute("/", index)
a.addRoute("/test", hello)
a.serveApp("localhost", 8080, debug=False)