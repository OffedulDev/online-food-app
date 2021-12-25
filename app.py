import random
from flask import Flask, render_template, redirect, url_for, session, request
import time
import json
import os.path

upper = "ABCDEFGHILMNOPQRSTUVZ"
lower = "abcdefhilmnopqrstuvz"
digits = "1234567890"

_all = upper+lower+digits

class LandingPage:
    def __init__(self, _title, _color, _slogan, _isLoggedIn):
        self.title = _title
        self.color = _color
        self.slogan = _slogan
        self.isLoggedIn = _isLoggedIn
    
    def build(self):
        if self.isLoggedIn == True:
            self.isLoggedIn = "Gestisci Account"
        else:
            self.isLoggedIn = "Registrati"

        
        return render_template('landingpage.html', title=self.title, color=self.color, slogan=self.slogan, stato=self.isLoggedIn)

class AccountPage:
    def __init__(self, _name, _password):
        self._name = _name
        self._password = str(_password.decode("utf-32"))
    
    def build(self):
        return render_template('accountpage.html', self._name, self._password)

class PreloadPage:
    def __init__(self, redirect):
        self.redirect = redirect
    
    def build(self):
        return render_template('preload.html', redirect=self.redirect)

class Account:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        self.json = None

    def buildjson(self):
        account = {}

        account['name'] = self.name
        account['password'] = self.password
        account['token'] = str(self.buildtoken(True))

        dumped = json.dumps(account, indent=2)

        self.json = dumped
        return None

    def buildlist(self):
        if self.json == None: return

        with open("profiles/" + self.name + ".kichuseraccount", "w") as f:
            f.seek(0)
            f.write(str(str(self.json).encode('utf-32'), 'utf-32'))
            f.truncate()

    def buildtoken(self, bypass):
        if not bypass == True and self.json == None: return
        
        temp = random.sample(_all, 7)

        temp1 = "".join(temp)

        temp2 = random.sample(_all, 7)

        temp3 = "".join(temp)

        temp4 = random.sample(_all, 7)

        temp5 = "".join(temp)

        token = str(temp1 + temp3 + temp5)

        return token
            
            

app = Flask(__name__)
app.secret_key = 'hghfhghirubruitbyutiyuryuid'

@app.route("/")
def init():
    try:
        token = request.args.get('token')

        with open("profiles/" + session['user'] + ".kichuseraccount", "r") as f:
            loadj = json.loads(f.read())

            print(token, loadj['token'])
            if token == loadj['token']:
                return LandingPage('Kich', 'DarkKhaki', 'Kich', True).build()
            else:
                return LandingPage('Kich', 'DarkKhaki', 'Kich', False).build()
    except:
        return LandingPage('Kich', 'DarkKhaki', 'Kich', False).build()

@app.route("/reset")
def reset():
    session['isLoggedIn'] = False
    return redirect("/")

@app.route("/account")
def account():
    isLoggedIn = None

    try:
        isLoggedIn = session['isLoggedIn']

        if isLoggedIn == True:
            return redirect("/?token=" + session['token'])
        else:
            isLoggedIn = False
    except:
        isLoggedIn = False

    if isLoggedIn != False: return redirect("/?token=" + session['token'])

    return redirect("/preload?redirect=registration&isLoggedIn=False")

@app.route("/preload")
def preload():
    redirectPage = request.args.get('redirect')
    isLoggedIn = request.args.get('isLoggedIn')
    
    return PreloadPage(redirectPage).build()

@app.route("/registration", methods = ['POST', 'GET'])
def registration():
    if request.method == 'GET':
        return render_template('registration.html')
    elif request.method == 'POST':
        username = request.values.get('username')
        password = request.values.get('password')

       # if os.path("./profiles/" + username.encode( 'utf-32') + ".kichuseraccount"): return redirect("/")
        
        if username == " " or password == " ": return

        acc = Account(username, password)
        acc.buildjson()
        acc.buildlist()

        session['isLoggedIn'] = True
        session['user'] = acc.name
        session['token'] = json.loads(acc.json)['token']
        return redirect("/?token=" + session['token'])








if __name__ == "__main__":
    app.run(host='0.0.0.0')
