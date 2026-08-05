import json
from datetime import date
import calendar
import matplotlib.pyplot as plt

def sauvegarder(data):
    with open("floww.json", "w") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def charger():
    try:
        with open("floww.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"mois": f"{date.today().year}-{date.today().month:02d}", "revenu": 0, "objectif_epargne": 0, "depenses": [], "historique": {}}

data = charger()



if "mois" not in data:
    data["mois"] = "2026-07"
if "historique" not in data:
    data["historique"] = {} 


mois_actuel = f"{date.today().year}-{date.today().month:02d}"
if data["mois"] != mois_actuel:
    total = 0
    for depense in data["depenses"]:
      total += depense["montant"]
    epargne = data["revenu"] - total      
    data["historique"][data["mois"]] = {"total_depenses": total, "epargne": epargne}
    data["depenses"] = []
    data["mois"] = mois_actuel
    sauvegarder(data)
    print(f"Nouveau mois ! {data['mois']} commence, l'ancien est archivé.")



# Premier lancement : si le revenu est à 0, on demande la config
if data["revenu"] == 0:
    data["revenu"] = float(input("Ton revenu mensuel : "))
    data["objectif_epargne"] = float(input("Ton objectif d'épargne : "))
    sauvegarder(data)

while True:
    print("\n--- FLOWW ---")
    print("1. Ajouter une dépense")
    print("2. Voir mon budget")
    print("3. Voir mes dépenses")
    print("4. Voir l'historique")
    print("5. Voir le graphique d'épargne")
    print("6. Voir le graphique des dépenses")
    print("7. Quitter")
    choix = input("Ton choix : ")

    if choix == "1":
        #  demander nom et montant, puis ajouter
        try:
          data["depenses"].append({"nom":input("Nom de la dépense : "), "montant": float(input("Montant de la dépense : "))})
          sauvegarder(data)
        except ValueError:
            print("Montant invalide, réessaie.")
          # {"nom": .E.., "montant": ...} à la liste data["depenses"] 
        
    elif choix == "2": 
       #  calculer le total des dépenses,
        total = 0
        for depense in data["depenses"]:
            total += depense["montant"]
        print(f"Total des depenses : {total}\n")

        #   afficher : revenu - objectif_epargne - total = budget restant
        budget_restant = data["revenu"] - data["objectif_epargne"] - total
        print(f"Budget restant : {budget_restant}")

        # calculer le nombre de jours restant dans le mois
        aujourdhui = date.today()
        jours_dans_mois = calendar.monthrange(aujourdhui.year, aujourdhui.month)[1]
        jours_restant = jours_dans_mois - aujourdhui.day + 1
        budget_par_jour = budget_restant / jours_restant
        #   afficher le budget restant, le nombre de jours restant et le budget par jour
        print(f"Il te reste {round(budget_restant, 2)}€ pour {jours_restant} jours soit {round(budget_par_jour, 2)}€/jour max")

        rythme = total / aujourdhui.day
        depense_projetees = rythme * jours_dans_mois
        epargne_projetee = data["revenu"] - depense_projetees
        #   afficher le rythme de dépense, les dépenses projetées et l'épargne projetée
        print(f"Rythme de depense : {round(rythme, 2)}€/jour, si tu continues à ce rythme, tu devrais dépenser {round(depense_projetees, 2)}€ ce mois ci et épargner {round(epargne_projetee, 2)}€")
        #  afficher le rythme de dépense, les dépenses projetées et l'épargne projetée
        if epargne_projetee >= data["objectif_epargne"]:
            print(f"Tu es donc dans les clous ! Tu devrais epargner {round(epargne_projetee, 2)} € ce mois-ci")
        else:
            print(f"Attention ! Tu devrais epargner {round(epargne_projetee, 2)} € ce mois-ci, soit moins que ton objectif de {data['objectif_epargne']} €")

    elif choix == "3":
        chaque_depense = ''
        for depense in data["depenses"]:
            chaque_depense += f"{depense['nom']} : {depense['montant']}\n"
        print(chaque_depense)

    elif choix == "4":
        if data["historique"] == {}:
                    print("Aucun historique pour le moment.")
        else:            
            for mois, bilan in data["historique"].items():
                print(f"{mois}: depensé {bilan["total_depenses"]}, epargné: {bilan["epargne"]}")

    elif choix == "5":
        mois_liste = []
        epargne_liste = []
        for mois, bilan in data["historique"].items():
            mois_liste.append(mois)
            epargne_liste.append(bilan["epargne"])
        total = 0
        for depense in data["depenses"]:
            total += depense["montant"]
        epargne_liste.append(data["revenu"] - total)
        mois_liste.append(mois_actuel)
        plt.bar(mois_liste,epargne_liste)
        plt.title("Épargne mensuelle")
        plt.ylabel("€")
        plt.show()

    elif choix == "6":
        if not data["depenses"]:
            print("Aucune dépense pour le moment.")
        else:
            noms_liste = []
            montants_liste = []
            for depense in data["depenses"]:
                noms_liste.append(depense["nom"])
                montants_liste.append(depense["montant"])

            plt.pie(montants_liste, labels=noms_liste, autopct="%1.1f%%")
            plt.title(f"Dépenses de {data['mois']}")
            plt.show()


    elif choix == "7":
        break
