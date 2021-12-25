from flask import Flask, render_template, redirect, url_for


class LandingPage:
    def __init__(self, _title, _color, _slogan):
        self.title = _title
        self.color = _color
        self.slogan = _slogan
    
    def build(self):
        return render_template('landingpage.html', title=self.title, color=self.color, slogan=self.slogan)

app = Flask(__name__)


@app.route("/")
def init():
    return LandingPage('LandTst', 'DarkKhaki', 'test').build()