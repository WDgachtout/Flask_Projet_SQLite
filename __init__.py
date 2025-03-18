from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, session
from flask import render_template
from flask import json
from urllib.request import urlopen
from werkzeug.utils import secure_filename
import sqlite3
 
app = Flask(__name__)                                                                                                                  
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour créer une clé "authentifie" dans la session utilisateur
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')

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
            conn = sqlite3.connect('database.db')
            cursor = conn.cursor()

            # Vérifier si l'utilisateur existe
            cursor.execute('SELECT id, role FROM users WHERE username = ? AND password = ?', (username, password))
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



@app.route('/fiche_client/<int:post_id>')
def Readfiche(post_id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients WHERE id = ?', (post_id,))
    data = cursor.fetchall()
    conn.close()
    # Rendre le template HTML et transmettre les données
    return render_template('read_data.html', data=data)

@app.route('/consultation/')
def ReadBDD():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM clients;')
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

@app.route('/enregistrer_client', methods=['GET'])
def formulaire_client():
    return render_template('formulaire.html')  # afficher le formulaire

@app.route('/enregistrer_client', methods=['POST'])
def enregistrer_client():
    nom = request.form['nom']
    prenom = request.form['prenom']

    # Connexion à la base de données
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Exécution de la requête SQL pour insérer un nouveau client
    cursor.execute('INSERT INTO clients (created, nom, prenom, adresse) VALUES (?, ?, ?, ?)', (1002938, nom, prenom, "ICI"))
    conn.commit()
    conn.close()
    return redirect('/consultation/')  # Rediriger vers la page d'accueil après l'enregistrement

@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        genre = request.form['genre']
        stock = int(request.form['stock'])

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO books (title, author, genre, stock) VALUES (?, ?, ?, ?)',
                       (title, author, genre, stock))
        conn.commit()
        conn.close()

        return redirect('/books')

    return render_template('add_book.html')

@app.route('/books')
def list_books():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    conn.close()

    return render_template('list_books.html', books=books)
@app.route('/borrow/<int:book_id>', methods=['POST'])
def borrow_book(book_id):
    if not est_authentifie():
        return redirect(url_for('authentification'))

    user_id = session.get('user_id')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Vérifier si le livre est disponible
    cursor.execute('SELECT stock FROM books WHERE id = ?', (book_id,))
    book = cursor.fetchone()
    
    if book and book[0] > 0:
        # Insérer l'emprunt et mettre à jour le stock
        cursor.execute('INSERT INTO borrows (user_id, book_id) VALUES (?, ?)', (user_id, book_id))
        cursor.execute('UPDATE books SET stock = stock - 1 WHERE id = ?', (book_id,))
        conn.commit()

    conn.close()
    
    return redirect('/books')


if __name__ == "__main__":
  app.run(debug=True)
