<!DOCTYPE html>
<html>
<head>
    <title>Liste des Tâches</title>
</head>
<body>
    <h1>Liste des Tâches</h1>

    {% if not tasks %}
        <p>Aucune tâche disponible.</p>
    {% else %}
        <ul>
            {% for task in tasks %}
                <li><strong>{{ task.title }}</strong>: {{ task.description }} (Échéance : {{ task.due_date }}) 
                [<a href="/complete_task/{{ loop.index0 }}">Terminer</a>] 
                [<a href="/delete_task/{{ loop.index0 }}">Supprimer</a>]</li>
            {% endfor %}
        </ul>
    {% endif %}

    <a href="/">Retour à l'accueil</a>
</body>
</html>
