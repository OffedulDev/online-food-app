import random
from flask import Flask, render_template, redirect, url_for, session, request
import time
import json
import os
import sys



class LandingPage:
    def __init__(self, _title, _isLoggedIn, _accName=None):
        self.title = _title
        self.isLoggedIn = _isLoggedIn
        self.accName = _accName

    def build(self):
        if self.isLoggedIn == True:
            self.isLoggedIn = "Gestisci Account"
        else:
            self.isLoggedIn = "Registrati"

        return render_template('index.html', title=self.title, stato=self.isLoggedIn, accname=self.accName)

class AccountPage:
    def __init__(self, _name, _password, _delivery_address):
        self._name = _name
        self._password = _password
        self._delivery_address = _delivery_address
    
    def build(self):
        return render_template('Account-Managment.html', name=self._name, indirizzo=self._delivery_address)

class PreloadPage:
    def __init__(self, redirect, token=None):
        self.redirect = redirect
        self.token = token
    
    def build(self):
        return render_template('preload.html', redirect=self.redirect, token=self.token)

class RegistrationPage:
    def __init__(self):
        self.v = None
    
    def build(self):
        return render_template('Registrati.html')

class LoginPage:
    def __init__(self):
        self.v = None
    
    def build(self):
        return render_template('Accedi.html')

class Account:
    def __init__(self, name, password, delivery_address):
        self.name = name
        self.password = password
        self.delivery_address = delivery_address
        self.json = None

    def build(self):
        data = createUserData(self.name, self.password, self.delivery_address, str(self.createToken()))
        
        self.json = data

        with open("profiles/" + self.name + ".kichuseraccount", "w") as f:
            f.seek(0)
            f.write(str(str(self.json).encode('utf-32'), 'utf-32'))
            f.truncate()
            f.close()

        return None

    def createToken(self):
        upper = "ABCDEFGHILMNOPQRSTUVZ"
        lower = "abcdefhilmnopqrstuvz"
        digits = "1234567890"

        _all = upper+lower+digits
        
        temp = random.sample(_all, 7)

        temp1 = "".join(temp)

        temp2 = random.sample(_all, 7)

        temp3 = "".join(temp)

        temp4 = random.sample(_all, 7)

        temp5 = "".join(temp)

        token = str(temp1 + temp3 + temp5)

        return token
              
# Utility Functions

def getUserData(username):
    if username == None or username == " ": return None

    with open("profiles/" + username + ".kichuseraccount", "r") as f:
        loadj = json.loads(f.read())

        return loadj

def sessionElementExist(element_name):
    exist = False

    try:
        if session[element_name] and session[element_name] != None:
            return session[element_name]
        else:
            Exception('failed')
    except:
        exist = False

    return exist

def checkUserData(username):
    if not os.path.exists("profiles/" + username + ".kichuseraccount"): return False

def updateUserData(new_data, user):
    with open("profiles/" + user + ".kichuseraccount", "r+") as f:
        f.seek(0)
        f.write(new_data)
        f.truncate()
        f.close()
    
    return None

def createUserData(username, password, delivery_address, token):
    data = {}
    data['name'] = username
    data['password'] = password
    data['delivery_address'] = delivery_address
    data['token'] = token

    return json.dumps(data, indent=2)

app = Flask(__name__)
app.secret_key = 'hghfhghirubruitbyutiyuryuid'

@app.route("/")
def init():
    token = sessionElementExist('token')

    if token == False or token == None:
        return LandingPage('Kich', False).build()

    given = request.args.get('token')

    if given == None and token != False: return redirect("/?token=" + token)

    userdata = getUserData(session['user'])
    if token == userdata['token']:

        return LandingPage('Kich', True, userdata['name']).build()
    else:
        return LandingPage('Kich', False).build()


@app.route("/reset")
def reset():
    session['isLoggedIn'] = False
    session['token'] = None
    session['user'] = None
    return redirect("/")

@app.route('/manageaccount', methods=['GET', 'POST'])
def manageaccount():
    if request.method == 'GET':
        if sessionElementExist('user') != False:
            userdata = getUserData(session['user'])

            return AccountPage(userdata['name'], userdata['password'], userdata['delivery_address']).build()
        else:
            return redirect("/")
    elif request.method == 'POST':
        if 'delivery_address' in request.form and sessionElementExist('user') != False:

            print("got post1")
            userdata = getUserData(session['user'])
            new_address = request.values.get('delivery_address')

            if new_address == " ": return redirect("/")
            
            new_data = createUserData(userdata['name'], userdata['password'], new_address, userdata['token'])
            updateUserData(new_data, session['user'])
            
            return redirect("/manageaccount")
        elif 'username' in request.form and sessionElementExist('user') != False:

            userdata = getUserData(session['user'])
            new_username = request.values.get('username')

            if new_username == " " or len(new_username) > 15 or len(new_username) < 2: return redirect("/")

            new_data = createUserData(new_username, userdata['password'], userdata['delivery_address'], userdata['token'])
            updateUserData(new_data, session['user'])

            os.chdir(r'profiles/')

            os.rename(session['user'] + ".kichuseraccount", new_username + ".kichuseraccount")
            session['user'] = new_username

            os.chdir("..")



            return redirect("/manageaccount")
        elif 'password' in request.form and sessionElementExist('user') != False:

            print("got post3")
            userdata = getUserData(session['user'])
            new_password = request.values.get('password')

            if new_password == " ": return redirect("/")
            
            new_data = createUserData(userdata['name'], new_password, userdata['delivery_address'], userdata['token'])
            updateUserData(new_data, session['user'])
            
            return redirect("/manageaccount")
        else:
            return "None"
            

 
@app.route("/account")
def account():
    isLoggedIn = sessionElementExist('isLoggedIn')

    if not (isLoggedIn == False): return redirect("/manageaccount")

    return redirect("/preload?redirect=registration&isLoggedIn=False")

@app.route("/preload")
def preload():
    redirectPage = request.args.get('redirect')
    isLoggedIn = request.args.get('isLoggedIn')
    
    return PreloadPage(redirectPage).build()

@app.route("/registration", methods = ['POST', 'GET'])
def registration():
    if request.method == 'GET':
        return RegistrationPage().build()
    elif request.method == 'POST':
        username = request.values.get('username')
        delivery_address = request.values.get('delivery_address')
        password = request.values.get('password')
        
        if username == " " or password == " ": return
        if len(username) > 15 or len(username) < 2: return redirect("/registration")

        acc = Account(username, password, delivery_address)
        acc.build()

        session['isLoggedIn'] = True
        session['user'] = acc.name
        session['token'] = getUserData(acc.name)['token']
        return redirect("/")

@app.route('/home')
def loadhome():
    return redirect('/')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return LoginPage().build()
    elif request.method == 'POST':
        sessionToken = sessionElementExist('sessionToken')
        sessionUser = sessionElementExist('user')
        
        if sessionToken != False: return redirect('/preload?redirect=home&isLoggedIn=false')
    

        # starts account log

        username = request.values.get("username")
        password = request.values.get("password")
        if checkUserData(username) == False: return redirect('/preload?redirect=home&isLoggedIn=false')

        if username == " " or password == " ": return redirect('/preload?redirect=home&isLoggedIn=false')
    
        userdata = getUserData(username)
        
        if password == userdata['password']:
            accObject = Account(userdata['name'], userdata['password'], userdata['delivery_address'])
            accObject.build()
            token = accObject.createToken()

            data = createUserData(userdata['name'], userdata['password'], userdata['delivery_address'], token)
    
            updateUserData(data, username)
            session['token'] = token
            session['isLoggedIn'] = True
            session['user'] = userdata['name']
        
        return redirect("/")






if __name__ == "__main__":
    app.run(host='0.0.0.0')
