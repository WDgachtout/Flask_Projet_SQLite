from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour vérifier si l'utilisateur est authentifié
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Fonction pour vérifier si l'utilisateur est administrateur
def est_admin():
    return session.get('role') == 'admin'

@app.route('/admin_only')
def admin_only():
    if not est_admin():
        return "Accès refusé : Administrateurs uniquement", 403

    return "Bienvenue, administrateur !"

@app.route('/lecture')
def lecture():
    if not est_authentifie():
        # Rediriger vers la page d'authentification si l'utilisateur n'est pas authentifié
        return redirect(url_for('authentification'))

    # Si l'utilisateur est authentifié
    return "<h2>Bravo, vous êtes authentifié</h2>"

@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            # Connexion à la base de données
            conn = sqlite3.connect('database2.db')
            cursor = conn.cursor()

            # Vérifier si l'utilisateur existe
            cursor.execute('SELECT ID_utilisateur, role FROM Utilisateurs WHERE username = ? AND password = ?', (username, password))
            user = cursor.fetchone()
            conn.close()

            if user:
                # Stocker les informations utilisateur dans la session
                session['authentifie'] = True
                session['user_id'] = user[0]
                session['role'] = user[1]

                return redirect(url_for('lecture'))
            else:
                # Identifiants incorrects
                return render_template('formulaire_authentification.html', error="Nom d'utilisateur ou mot de passe incorrect")

        except Exception as e:
            # Gestion des erreurs SQL ou autres exceptions
            return f"Une erreur est survenue : {e}", 500

    return render_template('formulaire_authentification.html', error=False)

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        titre = request.form['title']
        auteur = request.form['author']
        annee_publication = int(request.form['year'])
        quantite = int(request.form['stock'])

        try:
            conn = sqlite3.connect('database2.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Livres (ID_livre, Titre, Auteur, Annee_publication, Quantite) VALUES (NULL, ?, ?, ?, ?)',
                           (titre, auteur, annee_publication, quantite))
            conn.commit()
            conn.close()
        except Exception as e:
            return f"Erreur lors de l'ajout du livre : {e}", 500

        return redirect('/books')

    return render_template('add_book.html')

@app.route('/books')
def list_books():
    try:
        conn = sqlite3.connect('database2.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM Livres WHERE Quantite > 0')
        books = cursor.fetchall()
        conn.close()
    except Exception as e:
        return f"Erreur lors de la récupération des livres : {e}", 500

    return render_template('list_books.html', books=books)

@app.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    if not est_authentifie():
        return redirect(url_for('authentification'))

    user_id = session.get('user_id')

    try:
        conn = sqlite3.connect('database2.db')
        cursor = conn.cursor()

        # Vérifier si le livre est disponible
        cursor.execute('SELECT Quantite FROM Livres WHERE ID_livre = ?', (book_id,))
        book = cursor.fetchone()

        if book and book[0] > 0:
            # Insérer l'emprunt et mettre à jour le stock
            cursor.execute('INSERT INTO Emprunts (ID_utilisateur, ID_livre, Date_emprunt) VALUES (?, ?, DATE("now"))',
                           (user_id, book_id))
            cursor.execute('UPDATE Livres SET Quantite = Quantite - 1 WHERE ID_livre = ?', (book_id,))
            conn.commit()
        else:
            return "Livre non disponible", 400

        conn.close()
    except Exception as e:
        return f"Erreur lors de l'emprunt : {e}", 500

    return redirect('/books')

@app.route('/my_borrows')
def my_borrows():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    user_id = session.get('user_id')

    try:
        conn = sqlite3.connect('database2.db')
        cursor = conn.cursor()
        cursor.execute("""
            SELECT Emprunts.ID_emprunt, Livres.Titre, Livres.Auteur, Emprunts.Date_emprunt 
            FROM Emprunts 
            JOIN Livres ON Emprunts.ID_livre = Livres.ID_livre 
            WHERE Emprunts.ID_utilisateur = ?
        """, (user_id,))
        borrows = cursor.fetchall()
        conn.close()
    except Exception as e:
        return f"Erreur lors de la récupération des emprunts : {e}", 500

    return render_template('my_borrows.html', borrows=borrows)

if __name__ == "__main__":
    app.run(debug=True)
    
