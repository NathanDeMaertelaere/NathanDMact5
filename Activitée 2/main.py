# On importe Flask du module Flask
from flask import Flask, render_template, request, abort, session

# CREATION DE L'APP
# On crée une instance de flask qui est donc notre app qu'on stocke dans la variable app
app = Flask("My first WebApp")

HOST_IP = "192.168.1.24" 

@app.before_request
def limit_remote_addr():
    client_ip = request.remote_addr
    if client_ip != HOST_IP:
        abort(403) 

# Route de la page d'accueil
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/scndpage')
def scnd():
    erreur = "403 Acces denied"
    return render_template("scndpage.html", erreur=erreur)

# EXECUTION
# host = 0.0.0.0 -> app accessible par n'importe quelle adresse IP
# port = 81 -> port d'écoute du serveur de l'app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
