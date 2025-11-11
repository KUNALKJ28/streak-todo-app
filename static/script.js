document.addEventListener('DOMContentLoaded', () => {
    const taskList = document.getElementById('task-list');
    const addTaskForm = document.getElementById('add-task-form');

    // Load tasks on page load
    loadTasks();

    // Add task
    addTaskForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const taskName = document.getElementById('task-name').value;
        await fetch('/api/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: taskName })
        });
        document.getElementById('task-name').value = '';
        loadTasks();
    });

    async function loadTasks() {
        const response = await fetch('/api/tasks');
        const tasks = await response.json();
        taskList.innerHTML = '';
        tasks.forEach(task => {
            const li = document.createElement('li');
            li.innerHTML = `
                <span>${task.name}</span>
                <span class="streak">Streak: ${task.streak}</span>
                <button onclick="completeTask(${task.id})">Complete</button>
                <button class="delete-btn" onclick="deleteTask(${task.id})">Delete</button>
            `;
            taskList.appendChild(li);
        });
    }

    window.completeTask = async (id) => {
        await fetch(`/api/tasks/${id}/complete`, { method: 'POST' });
        loadTasks(); // Reload to show updated streak
    };

    window.deleteTask = async (id) => {
        if (confirm('Are you sure you want to delete this task?')) {
            await fetch(`/api/tasks/${id}`, { method: 'DELETE' });
            loadTasks(); // Reload list
        }
    };
});