from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'  # Clé secrète pour les sessions

# Fonction pour vérifier si l'utilisateur est authentifié
def est_authentifie():
    return session.get('authentifie')

@app.route('/')
def hello_world():
    return render_template('hello.html')  # Page d'accueil existante

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

# Gestionnaire de tâches collaboratif

# Initialisation des tâches en session
@app.before_request
def init_session():
    if 'tasks' not in session:
        session['tasks'] = []

# Ajouter une tâche
@app.route('/add_task', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        due_date = request.form['due_date']
        
        # Créer une tâche sous forme de dictionnaire
        task = {
            'title': title,
            'description': description,
            'due_date': due_date,
            'is_completed': False
        }
        
        # Ajouter la tâche à la liste en session
        tasks = session['tasks']
        tasks.append(task)
        session['tasks'] = tasks
        
        return redirect(url_for('list_tasks'))
    
    return render_template('add_task.html')

# Afficher les tâches
@app.route('/tasks')
def list_tasks():
    tasks = session.get('tasks', [])
    return render_template('list_tasks.html', tasks=tasks)

# Marquer une tâche comme terminée
@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    tasks = session.get('tasks', [])
    if 0 <= task_id < len(tasks):
        tasks[task_id]['is_completed'] = True
        session['tasks'] = tasks
    
    return redirect(url_for('list_tasks'))

# Supprimer une tâche
@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    tasks = session.get('tasks', [])
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        session['tasks'] = tasks
    
    return redirect(url_for('list_tasks'))

if __name__ == "__main__":
    app.run(debug=True)
