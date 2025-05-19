from flask import Flask, render_template, session, request, redirect

# Importar todas as classes do projeto
from classes.designers import Designers
from classes.userlogin import Userlogin
from classes.collections import Collections
from classes.fashion_show import FashionShow
from classes.designers_collections import DesignersCollections
from classes.gclass import Gclass

# Importar os ficheiros de gestão (caso uses páginas com POST/GET)
import subs.index_subs as indexSubs
import subs.index_userlogin as indexUserlogin

app = Flask(__name__)
app.secret_key = 'BAD_SECRET_KEY'  # Troca por uma chave forte em produção

# Caminho para os ficheiros de base de dados
path = 'data/'
Designers.read(path + 'FashionDesigners.db')
Userlogin.read(path + 'Userlogin.db')
Collections.read(path + 'Collections.db')
FashionShow.read(path + 'FashionShow.db')
DesignersCollections.read(path + 'DesignersCollections.db')
Gclass.read(path + 'Gclass.db')

# Página inicial
@app.route("/")
def main():
    return render_template("home.html", ulogin=session.get("user"))

# Login (aceita qualquer utilizador e redireciona para dashboard)
@app.route("/login", methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        user = request.form["user"]
        password = request.form["password"]

        # Aceita qualquer username/password
        session["user"] = user
        return redirect("/dashboard")

    return render_template("login.html", msg=msg)

# Logout
@app.route("/logoff")
def logoff():
    session.clear()
    return redirect("/")

# Dashboard com os dados de todas as classes
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/login")

    return render_template(
        "dashboard.html",
        ulogin=session["user"],
        designers=Designers.lista,
        users=Userlogin.lista,
        collections=Collections.lista,
        fashionshows=FashionShow.lista,
        designerscollections=DesignersCollections.lista,
        gclasses=Gclass.lista
    )

# Rotas extras (opcional)
@app.route("/designers", methods=["GET", "POST"])
def designers():
    return indexSubs.index(path)

@app.route("/Userlogin", methods=["GET", "POST"])
def userlogin():
    return indexUserlogin.index(path)

if __name__ == "__main__":
    app.run(debug=True)

