from lifaw import Lifaw
from json import dumps

a = Lifaw()

def index():
    data = "landing page"
    return a.buildResponse(data)

def hello():
    data = "juan rules!!"
    return a.buildResponse(data)

def jsonTest():
    data = {"test": "si", "numero": 23}
    return a.buildResponse(data, content="application/json")

a.addRoute("/", index)
a.addRoute("/test", hello)
a.addRoute("/json", jsonTest)
a.addRoute("/fake", False)
a.serveApp("localhost", 8080, debug=False)