from flask import Flask
from floww import charger
from datetime import date 
import calendar


app = Flask(__name__)

@app.route("/")
def accueil():
    data = charger()
    total = 0
    for depense in data["depenses"]:
        total += depense["montant"]

    budget_restant = data["revenu"] - data["objectif_epargne"] - total

    aujourdhui = date.today()
    jours_dans_mois = calendar.monthrange(aujourdhui.year, aujourdhui.month)[1]
    jours_restant = jours_dans_mois - aujourdhui.day + 1
    budget_par_jour = budget_restant / jours_restant

    # la liste des dépenses en HTML :
    liste_html = ""
    for depense in data["depenses"]:
        liste_html += f"<li>{depense['nom']} : {depense['montant']} €</li>"    

    return f"""
    <h1>FLOWW 💸</h1>
    <p>Revenu : {data['revenu']} €</p>
    <p>Budget restant : {round(budget_restant, 2)} €</p>
    <p>Tu peux dépenser {round(budget_par_jour, 2)} €/jour pendant {jours_restant} jours</p>
    <h2>Dépenses du mois</h2>
    <ul>{liste_html}</ul>
    """

app.run(debug=True)