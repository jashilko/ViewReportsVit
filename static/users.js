// Массив с данными пользователей для примера
const users = [
    { id: 1, name: "Иван Иванов", phone: "+7 999 123-45-67", avatar: "https://robohash.org/ivan-1", roles: ["Оператор"] },
    { id: 2, name: "Мария Смирнова", phone: "+7 999 234-56-78", avatar: "https://robohash.org/maria-2", roles: ["Контроллер"] },
    { id: 3, name: "Петр Петров", phone: "+7 999 345-67-89", avatar: "https://robohash.org/petr-3", roles: ["Руководитель"] },
    { id: 4, name: "Ольга Кузнецова", phone: "+7 999 456-78-90", avatar: "https://robohash.org/olga-4", roles: ["Оператор", "Контроллер"] }
];

// Функция для добавления пользователей в список
function loadUsers() {
    const userList = document.getElementById("user-list");
    userList.innerHTML = '';  // Очищаем список перед загрузкой

    users.forEach(user => {
        const li = document.createElement("li");

        li.innerHTML = `
            <div class="user-info2">
                <span>${user.name}</span>
                <p>Телефон: ${user.phone}</p>
            </div>
            <div class="role-checkboxes">
                <label>
                    <input type="checkbox" value="Оператор" ${user.roles.includes("Оператор") ? "checked" : ""}>
                    Оператор
                </label>
                <label>
                    <input type="checkbox" value="Контроллер" ${user.roles.includes("Контроллер") ? "checked" : ""}>
                    Контроллер
                </label>
                <label>
                    <input type="checkbox" value="Руководитель" ${user.roles.includes("Руководитель") ? "checked" : ""}>
                    Руководитель
                </label>
                <button onclick="updateRoles(${user.id})">Обновить роли</button>
            </div>
        `;
        userList.appendChild(li);
    });
}

// Функция для обновления ролей пользователя
async function updateRoles(userId) {
    const userCheckboxes = Array.from(document.querySelectorAll(`#user-list li:nth-child(${userId}) .role-checkboxes input[type="checkbox"]`));
    const selectedRoles = userCheckboxes.filter(checkbox => checkbox.checked).map(checkbox => checkbox.value);

    // Находим пользователя по ID и обновляем его роли
    const user = users.find(user => user.id === userId);
    if (user) {
        user.roles = selectedRoles;

        // Отправляем POST-запрос на сервер FastAPI
        try {
            const response = await fetch('http://localhost:8000/update-roles', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_id: user.id,
                    roles: selectedRoles
                })
            });

            if (response.ok) {
                alert(`Роли пользователя ${user.name} обновлены: ${selectedRoles.join(", ")}`);
            } else {
                alert('Ошибка при отправке запроса');
            }
        } catch (error) {
            alert('Ошибка соединения с сервером');
        }
    }
}

// Функция для фильтрации пользователей
function filterUsers() {
    const nameFilter = document.getElementById("filter-name").value.toLowerCase();
    const phoneFilter = document.getElementById("filter-phone").value.toLowerCase();
    const roleFilter = document.getElementById("filter-role").value;

    const filteredUsers = users.filter(user => {
        const matchesName = user.name.toLowerCase().includes(nameFilter);
        const matchesPhone = user.phone.toLowerCase().includes(phoneFilter);
        const matchesRole = roleFilter === "" || user.roles.includes(roleFilter);
        return matchesName && matchesPhone && matchesRole;
    });

    // Очищаем и перерисовываем список с отфильтрованными пользователями
    const userList = document.getElementById("user-list");
    userList.innerHTML = '';
    filteredUsers.forEach(user => {
        const li = document.createElement("li");

        li.innerHTML = `
            <div class="user-info2">
                <span>${user.name}</span>
                <p>Телефон: ${user.phone}</p>
            </div>
            <div class="role-checkboxes">
                <label>
                    <input type="checkbox" value="Оператор" ${user.roles.includes("Оператор") ? "checked" : ""}>
                    Оператор
                </label>
                <label>
                    <input type="checkbox" value="Контроллер" ${user.roles.includes("Контроллер") ? "checked" : ""}>
                    Контроллер
                </label>
                <label>
                    <input type="checkbox" value="Руководитель" ${user.roles.includes("Руководитель") ? "checked" : ""}>
                    Руководитель
                </label>
                <button onclick="updateRoles(${user.id})">Обновить роли</button>
            </div>
        `;
        userList.appendChild(li);
    });
}

// Добавляем обработчики событий на поля фильтрации
document.getElementById("filter-name").addEventListener("input", filterUsers);
document.getElementById("filter-phone").addEventListener("input", filterUsers);
document.getElementById("filter-role").addEventListener("change", filterUsers);

// Загружаем пользователей при загрузке страницы
window.onload = loadUsers;
