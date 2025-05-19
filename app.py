from flask import Flask, render_template, session, request, redirect
from classes.designers import Designers
from classes.userlogin import Userlogin
import subs.index_subs as indexSubs
import subs.index_userlogin as indexUserlogin  # Novo ficheiro para Userlogin

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'

# Caminho para os ficheiros de dados
path = 'data/'
Designers.read(path + 'FashionDesigners.db')
Userlogin.read(path + 'Userlogin.db')

# Página inicial (home)
@app.route("/")
def main():
    return render_template("home.html", ulogin=session.get("user"))

# Página de login
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]

        # >>> IGNORA verificação e aceita qualquer login <<<
        session["user"] = user
        return redirect("/")

    return render_template("login.html", msg=msg)

# Logout
@app.route("/logoff")
def logoff():
    session.clear()
    return redirect("/")

# Página de gestão de designers
@app.route("/designers", methods=["POST", "GET"])
def designers():
    return indexSubs.index(path)

# Página de gestão de utilizadores
@app.route("/Userlogin", methods=["POST", "GET"])
def userlogin():
    return indexUserlogin.index(path)  # Igual ao index_subs, mas para Userlogin

if __name__ == "__main__":
    app.run(debug=True)
