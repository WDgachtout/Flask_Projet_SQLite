<%@ page import="java.util.ArrayList, com.example.taskmanager.Task" %>
<%
ArrayList<Task> tasks = (ArrayList<Task>) session.getAttribute("tasks");
if (tasks == null) {
    tasks = new ArrayList<>();
}
%>

<!DOCTYPE html>
<html>
<head>
    <title>Liste des Tâches</title>
</head>
<body>
    <h1>Liste des Tâches</h1>

    <% if (tasks.isEmpty()) { %>
        <p>Aucune tâche disponible.</p>
    <% } else { %>
        <ul>
            <% for (Task task : tasks) { %>
                <li><strong><%= task.getTitle() %></strong>: <%= task.getDescription() %> - Échéance : <%= task.getDueDate() %></li>
            <% } %>
        </ul>
    <% } %>

    <a href="addTask.jsp">Ajouter une nouvelle tâche</a>
</body>
</html>
