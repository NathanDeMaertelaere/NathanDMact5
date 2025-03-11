# On importe Flask du module flask
from flask import Flask, render_template, session, redirect, abort, request

# Importation de os
import os

# On importe la liste de dictionnaires (question + réponses) de notre fichiers questions.py
from questions import questions

# On importe les descriptions pour le resultats
from resultats import resultats

# CREATION DE l'APP
# On crée une instance de Flask qui est donc notre app qu'on stocke dans la variable app
app = Flask("Mon Super Quizz")
app.secret_key = os.urandom(24)

HOST_IP = "192.168.1.61" 

@app.before_request
def limit_remote_addr():
    client_ip = request.remote_addr
    if client_ip != HOST_IP:
        abort(403) 

# Route de notre page d'accueil qui est donc à la racine de notre app
@app.route("/")
def index():
    session["numero_question"] = 0
    session["score"] =  {"Link" : 0, "Sheik" : 0, "Zelda" : 0, "Tingle" : 0}
    return render_template("index.html")

# Route seconde Page
@app.route("/question")
def question():
    # On accède à la variable globale questions
    global questions
    # On récupère le numéro de la question
    numero = session["numero_question"]
    # On vérifie que nous en sommes pas à la dernière
    if numero < len(questions):
        # On récupère l'énoncé de la question
        question = questions[numero]["enonce"]
        # On crée une copie du dictionnaire de notre question
        questions_copy = questions[numero].copy()
        # On supprime l'énoncé pour n'avoir que les questions
        questions_copy.pop("enonce")
        # On récupère nos réponses sous forme de liste
        reponses = list(questions_copy.values())
        # On récupère les clefs = personnages sous forme de liste pour comptage des scores
        clefs = list(questions_copy.keys())
        # On stocke l'ordre dans un cookie pour le comptage des scores
        session["clefs"] = clefs
        # On affiche la question et les réponses possibles
        return render_template("question.html", question = question, reponses = reponses)
    else :
        # On récupère la variable globale résultats
        global resultats
        # On transforme nos score en liste décroissante
        scores_tries = sorted(session["score"], key = session["score"].get, reverse = True)
        # On récupère le nom du personnage gagnant =
        vainqueur = scores_tries[0]
        # On récupère la description liée au personnage
        description = resultats[vainqueur]
        # On affiche notre page de resultat en injectant le nom du vainqueur et la description
        return render_template("resultats.html", vainqueur = vainqueur, description = description  )



# Route permettant de compter les réponses de l'utilisateur
@app.route("/reponse/<numero>")
def reponse(numero):
    # On incrémente numero_question pour passer à la question suivante
    session["numero_question"] += 1
    # On récupère le nom du vainqueur = le nom du personnage dont la réponse est associée
    personnage = session["clefs"][int(numero)]
    # On incrémente le score du personnage dont la réponse est associée
    session["score"][personnage] += 1
    # On redirige vers le route question afin d'afficher la question suivante
    return redirect("/question")


# EXECUTION
# host = "0.0.0.0" -> app accessible par n'importe quelle adresse
# port = 81 -> port d'écoute du serveur de l'app
app.run(host = "0.0.0.0", port = 81)