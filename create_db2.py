import sqlite3

# Connexion à la base de données SQLite
connection = sqlite3.connect('database2.db')

# Lecture du fichier SQL pour créer les tables
with open('schema2.sql', 'r') as f:
    connection.executescript(f.read())

# Insertion de données exemple dans la table Livres
cur = connection.cursor()
cur.execute("INSERT INTO Livres (ID_livre, Titre, Auteur, Annee_publication, Quantite) VALUES (?, ?, ?, ?, ?)", (1, 'Emilie', 'Victor', 2024, 10))
cur.execute("INSERT INTO Livres (ID_livre, Titre, Auteur, Annee_publication, Quantite) VALUES (?, ?, ?, ?, ?)", (2, 'Didier', 'Laurent', 2023, 5))

connection.commit()
connection.close()

print("Base de données initialisée avec succès.")
