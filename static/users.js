// Функция для загрузки пользователей с сервера
function fetchUsers() {
    return fetch('/auth/all_users') // URL API для получения списка пользователей
        .then(response => response.json()) // Преобразуем ответ в JSON
        .catch(error => {
            console.error('Ошибка при загрузке пользователей:', error);
            alert('Не удалось загрузить пользователей');
            return [];
        });
}

// Функция для добавления пользователей в список
function loadUsers() {
    const userList = document.getElementById("user-list");
    userList.innerHTML = '';  // Очищаем список перед загрузкой
    fetchUsers()
        .then(users => {
            users.forEach(user => {

        const li = document.createElement("li");

        li.innerHTML = `
            <div class="user-info2">
                <span>Оператор: ${user.phone_number}</span>
                <p>Руководитель: ${user.phone_teamleader}</p>
            </div>
            <div class="role-checkboxes">
                <label>
                    <input type="checkbox" value="Оператор" ${user.is_operator ? "checked" : ""}>
                    Оператор
                </label>
                <label>
                    <input type="checkbox" value="Контроллер" ${user.is_controller ? "checked" : ""}>
                    Контроллер
                </label>
                <label>
                    <input type="checkbox" value="Руководитель" ${user.is_teamlead ? "checked" : ""}>
                    Руководитель
                </label>
                <button onclick="updateRoles(${user.phone_number})">Обновить роли</button>
            </div>
        `;
        userList.appendChild(li);
    });
    })
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
            const response = fetch('http://localhost:8000/update-roles', {
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
    const phoneFilter = document.getElementById("filter-phone").value.toLowerCase();

    // Загружаем список пользователей с сервера
    fetchUsers()
        .then(users => {
            // Фильтруем пользователей по номеру телефона
            const filteredUsers = users.filter(user => {
                const matchesPhone = user.phone.toLowerCase().includes(phoneFilter);
                return matchesPhone;
            });

            // Очищаем и перерисовываем список с отфильтрованными пользователями
            const userList = document.getElementById("user-list");
            userList.innerHTML = '';
            filteredUsers.forEach(user => {
                const li = document.createElement("li");

                li.innerHTML = `
                    <div class="user-info2">
                        <span>${user.phone_number}</span>
                        <p>Телефон: ${user.phone_teamleader}</p>
                    </div>
                    <div class="role-checkboxes">
                        <label>
                    <input type="checkbox" value="Оператор" ${user.is_operator ? "checked" : ""}>
                    Оператор
                    </label>
                    <label>
                        <input type="checkbox" value="Контроллер" ${user.is_controller ? "checked" : ""}>
                        Контроллер
                    </label>
                    <label>
                        <input type="checkbox" value="Руководитель" ${user.is_teamlead ? "checked" : ""}>
                        Руководитель
                    </label>
                        <button onclick="updateRoles(${user.id})">Обновить роли</button>
                    </div>
                `;
                userList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Ошибка загрузки пользователей:', error);
            alert('Не удалось загрузить пользователей');
        });
}

// Добавляем обработчики событий на поля фильтрации
document.getElementById("filter-phone").addEventListener("input", filterUsers);

// Загружаем пользователей при загрузке страницы
window.onload = loadUsers;
