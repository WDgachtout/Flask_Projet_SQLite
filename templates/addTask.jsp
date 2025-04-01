<!DOCTYPE html>
<html>
<head>
    <title>Ajouter une Tâche</title>
</head>
<body>
    <h1>Ajouter une Tâche</h1>
    <form action="TaskServlet" method="post">
        <label for="title">Titre :</label><br>
        <input type="text" id="title" name="title" required><br><br>

        <label for="description">Description :</label><br>
        <textarea id="description" name="description" required></textarea><br><br>

        <label for="dueDate">Date d'échéance :</label><br>
        <input type="date" id="dueDate" name="dueDate" required><br><br>

        <button type="submit">Ajouter la tâche</button>
    </form>
</body>
</html>

