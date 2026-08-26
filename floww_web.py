from flask import Flask, request, redirect
from floww import connexion, get_config, assurer_mois, ajouter_depense, depenses_du_mois, total_du_mois, revenus_precedants
from datetime import date
import calendar


app = Flask(__name__)

@app.route("/")
def accueil():
    mois_actuel = f"{date.today().year}-{date.today().month:02d}"
    assurer_mois(mois_actuel)

    revenu, objectif = get_config()
    total = total_du_mois(mois_actuel)

    budget_restant = revenu - objectif - total
    aujourdhui = date.today()
    jours_dans_mois = calendar.monthrange(aujourdhui.year, aujourdhui.month)[1]
    jours_restant = jours_dans_mois - aujourdhui.day + 1
    budget_par_jour = budget_restant / jours_restant

    liste_html = ""
    for nom, montant in depenses_du_mois(mois_actuel):
        liste_html += f"<li>{nom} : {montant} €</li>"

    return f"""
    <h1>FLOWW 💸</h1>
    <p>Revenu : {revenu} €</p>
    <p>Budget restant : {round(budget_restant, 2)} €</p>
    <p>Tu peux dépenser {round(budget_par_jour, 2)} €/jour pendant {jours_restant} jours</p>
    <h2>Dépenses du mois</h2>
    <ul>{liste_html}</ul>
    <form method="post" action="/ajouter">
    <input name="nom" placeholder="Nom de la dépense">
    <input name="montant" placeholder="Montant" type="number" step="0.01">
    <button type="submit">Ajouter</button>
    </form>
    """

@app.route("/ajouter", methods=["POST"])
def ajouter():
    mois_actuel = f"{date.today().year}-{date.today().month:02d}"
    try:        
        montant = float(request.form["montant"])
    except ValueError:
        return redirect("/")
    nom = request.form["nom"]
    revenu, objectif = get_config()
    ajouter_depense(nom, montant, mois_actuel)
    return redirect("/")

app.run(debug=True)
