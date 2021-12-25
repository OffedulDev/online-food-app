from flask import Flask, render_template, redirect, url_for, session, request
import time

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

app = Flask(__name__)
app.secret_key = 'hghfhghirubruitbyutiyuryuid'

@app.route("/")
def init():
    try:
        if session['isLoggedIn'] == True:
            return LandingPage('Kich', 'DarkKhaki', 'Kich', True).build()
    except:
        return LandingPage('Kich', 'DarkKhaki', 'Kich', False).build()
        

@app.route("/account")
def account():
    isLoggedIn = None

    try:
        isLoggedIn = session['isLoggedIn']

        if isLoggedIn == True:
            return redirect("/")
        else:
            isLoggedIn = True
    except:
        isLoggedIn = True
    
    if isLoggedIn != True: return redirect("/")

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
        pass





if __name__ == "__main__":
    app.run(host='0.0.0.0')
