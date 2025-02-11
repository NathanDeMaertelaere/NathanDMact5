# On importe Flask du module Flask
from flask import Flask, render_template, request, abort, session

#Import de os
import os

from questions import questions

# CREATION DE L'APP
# On crée une instance de flask qui est donc notre app qu'on stocke dans la variable app
app = Flask("My first WebApp")
app.secret_key = os.urandom(24)

HOST_IP = "192.168.1.24" 

@app.before_request
def limit_remote_addr():
    client_ip = request.remote_addr
    if client_ip != HOST_IP:
        abort(403) 

# Route de la page d'accueil
@app.route('/')
def index():
    session["numero_question"]= 0
    session["score"] =  {"Link" : 0, "Sheik" : 0, "Zelda" : 0, "Tingle" : 0}
    return render_template("index.html")

@app.route('/question')
def question():
    global questions

    numero = session["numero_question"]

    if numero < len(questions):
        #On recup l'énoncé
        question = questions[numero]["enonce"]
        #On fait une copie du dictionnaire de nos questions
        questions_copy = questions[numero].copy()
        #On suppr l'énoncé
        questions_copy.pop("enonce")
        #On recupere les reponses sous forme de list
        reponses = list(questions_copy.values())
        #On recupere les clefs = personnages sous forme du listes
        clefs = list(questions_copy.keys())

        session["clefs"] = clefs
        return render_template("question.html", question = question, reponses = reponses)


# EXECUTION
# host = 0.0.0.0 -> app accessible par n'importe quelle adresse IP
# port = 81 -> port d'écoute du serveur de l'app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81)
