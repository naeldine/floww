import sqlite3
from datetime import date
import calendar
import matplotlib.pyplot as plt

def connexion():
    return sqlite3.connect("floww.db")

def get_config():
    conn = connexion()
    cur = conn.cursor()
    cur.execute("SELECT revenu, objectif_epargne FROM config")
    resultat = cur.fetchone()
    conn.close()
    return resultat

def assurer_mois(mois):
    conn = connexion()
    cur = conn.cursor()
    cur.execute("SELECT mois FROM mois WHERE mois = ?", (mois,))
    resultat = cur.fetchone()
    if resultat is None:
       revenu, objectif = get_config()
       cur.execute("INSERT INTO mois (mois, revenu, objectif_epargne) VALUES (?, ?, ?)", (mois, revenu, objectif))
       conn.commit()
       pass
    conn.close()

def ajouter_depense(nom, montant, mois):
    conn = connexion()
    cur = conn.cursor()
    cur.execute("INSERT INTO depenses (nom, montant, mois) VALUES (?, ?, ?)", (nom, montant, mois))
    conn.commit()
    conn.close()

def depenses_du_mois(mois):
    conn = connexion()
    cur = conn.cursor()
    cur.execute("SELECT id, nom, montant FROM depenses WHERE mois = ?", (mois,))
    resultat = cur.fetchall()
    conn.close()
    return resultat

def total_du_mois(mois):
    conn = connexion()
    cur = conn.cursor()
    cur.execute("SELECT COALESCE(SUM(montant), 0) FROM depenses WHERE mois = ?", (mois,))
    resultat = cur.fetchall()[0][0]  
    conn.close()
    return resultat

def historique():
    conn = connexion()
    cur = conn.cursor()
    cur.execute("SELECT mois, SUM(montant) FROM depenses GROUP BY mois")
    resultat = cur.fetchall()
    conn.close()
    return resultat

def revenus_precedants(mois):
    conn = connexion()
    cur = conn.cursor()
    cur.execute("SELECT revenu FROM mois WHERE mois = ?", (mois,))
    resultat = cur.fetchone()[0]
    conn.close()
    return resultat

def supprimer_depense(id):
    conn = connexion()
    cur = conn.cursor()
    cur.execute("DELETE FROM depenses WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def modifier_depense(id, nouveau_nom, nouveau_montant):
    conn = connexion()
    cur = conn.cursor()
    cur.execute("UPDATE depenses SET nom = ?, montant = ? WHERE id = ?", (nouveau_nom, nouveau_montant, id))
    conn.commit()
    conn.close()


if __name__ == "__main__":
    mois_actuel = f"{date.today().year}-{date.today().month:02d}"
    assurer_mois(mois_actuel)
    revenu, objectif = get_config()

    while True:
        print("\n--- FLOWW ---")
        print("1. Ajouter une dépense")
        print("2. Voir mon budget")
        print("3. Voir mes dépenses")
        print("4. Voir l'historique")
        print("5. Voir le graphique d'épargne")
        print("6. Voir le graphique des dépenses")
        print("7. Supprimer une dépense")
        print("8. Modifier une dépense")
        print("9. Quitter")
        choix = input("Ton choix : ")

        if choix == "1":
            try:
                nom = input("Nom de la dépense : ")
                montant = float(input("Montant de la dépense : "))
                ajouter_depense(nom, montant, mois_actuel)
            except ValueError:
                print("Montant invalide, réessaie.")

        elif choix == "2":
            total = total_du_mois(mois_actuel)
            print(f"Total des depenses : {total}\n")
            
            
            budget_restant = revenu - objectif - total
            print(f"Budget restant : {budget_restant}")
            
            
            aujourdhui = date.today()
            jours_dans_mois = calendar.monthrange(aujourdhui.year, aujourdhui.month)[1]
            jours_restant = jours_dans_mois - aujourdhui.day + 1
            budget_par_jour = budget_restant / jours_restant

            
            print(f"Il te reste {round(budget_restant, 2)}€ pour {jours_restant} jours soit {round(budget_par_jour, 2)}€/jour max")
            rythme = total / aujourdhui.day
            depense_projetees = rythme * jours_dans_mois
            epargne_projetee = revenu - depense_projetees

            
            print(f"Rythme de depense : {round(rythme, 2)}€/jour, si tu continues à ce rythme, tu devrais dépenser {round(depense_projetees, 2)}€ ce mois ci et épargner {round(epargne_projetee, 2)}€")

            
            if epargne_projetee >= objectif:
                print(f"Tu es donc dans les clous ! Tu devrais epargner {round(epargne_projetee, 2)} € ce mois-ci")
            else:
                print(f"Attention ! Tu devrais epargner {round(epargne_projetee, 2)} € ce mois-ci, soit moins que ton objectif de {objectif} €")

        elif choix == "3":
            for id_depense, nom, montant in depenses_du_mois(mois_actuel):
                print(f"n°{id_depense} : {nom} : {montant}€")

        elif choix == "4":
            for mois, total in historique():
                print(f"{mois} : dépense total : {total}€ epargne : {revenus_precedants(mois) - total}€")

        elif choix == "5":
            mois_liste = []
            epargne_liste = []
            for mois, bilan in historique():
                mois_liste.append(mois)
                epargne_liste.append(revenus_precedants(mois) - bilan)

            plt.bar(mois_liste,epargne_liste)
            plt.title("Épargne mensuelle")
            plt.ylabel("€")
            plt.show()

        elif choix == "6":
            if not depenses_du_mois(mois_actuel):
                print("Aucune dépense pour le moment.")
            else:
                noms_liste = []
                montants_liste = []
                for id_depense, nom, montant in depenses_du_mois(mois_actuel):
                    noms_liste.append(nom)
                    montants_liste.append(montant)
                plt.pie(montants_liste, labels=noms_liste, autopct="%1.1f%%")
                plt.title(f"Dépenses de {mois_actuel}")
                plt.show()


        elif choix == "7":
            for id_depense, nom, montant in depenses_du_mois(mois_actuel):
                print(f"n°{id_depense} : {nom} : {montant}€")
            try:
                id_a_supprimer = int(input("id de la dépense à supprimer : "))
                supprimer_depense(id_a_supprimer)
            except ValueError:
                print("id invalide.")

        elif choix == "8":
            for id_depense, nom, montant in depenses_du_mois(mois_actuel):
                print(f"n°{id_depense} : {nom} : {montant}€")
            try:
                id_a_modifier = int(input("id de la dépense à modifier : "))
                nouveau_nom = input("Nouveau nom : ")
                nouveau_montant = float(input("Nouveau montant : "))
                modifier_depense(id_a_modifier, nouveau_nom, nouveau_montant)
            except ValueError:
                print("Saisie invalide.")

        elif choix == "9":
            break


#             FLOWW
#               │
#       ┌───────┴────────┐
#       ↓                ↓
#    config             mois
#       │                │
# revenu + objectif    2026-08
#                        │
#                        ↓
#                    depenses
#                        │
#          ┌─────────────┼─────────────┐
#          ↓             ↓             ↓
#       chips         ventilo         café
#        2.60€         50€           1.50€


