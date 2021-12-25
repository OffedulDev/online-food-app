from flask import Flask, render_template, redirect

class HtmlObject:
    def __init__(self, _object):
        self.object = _object

    def getObject(self):
        return self.object

class LandingPage:
    def __init__(self, _title, _color, _slogan):
        self.title = _title
        self.color = _color
        self.slogan = _slogan
    
    def build(self):
        obj = HtmlObject('<html><head><title>' + self.title + '</title></head><body style="background-color: ' + self.color + '"><h1 style="text-align: center; font-family: Arial, Helvetica, sans-serif">' + self.title + '</h1></body></html>')

        return obj.getObject()  
1
app = Flask(__name__)


@app.route("/")
def init():
    return LandingPage('LandTst', 'DarkKhaki', 'test').build()