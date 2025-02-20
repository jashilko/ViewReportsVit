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

// Функция для загрузки руководителей с сервера
function fetchLeaders() {
    return fetch('/auth/all_teamleaders') // URL API для получения списка руководителей
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
    userList.innerHTML = ''; // Очищаем список перед загрузкой

    // Загружаем список руководителей
    fetchLeaders()
        .then(leaders => {
            fetchUsers()
                .then(users => {
                    users.forEach(user => {
                        const li = document.createElement("li");
                         li.setAttribute("data-phone", user.phone_number); // Уникальный атрибут
                        // Создаём элемент списка пользователей
                        li.innerHTML = `
                            <div class="user-info2">
                                <span>Оператор: ${user.phone_number}</span>
                                <p>${user.oper_name || ''}</p>
                            </div>
                            <div class="form-group">
                                <label for="group_leader_${user.phone_number}">Ваш руководитель</label>
                                <div style="display: flex; align-items: center; gap: 10px;">
                                    <select id="group_leader_${user.phone_number}" name="group_leader">
                                        <option value="">-- Выберите руководителя --</option>
                                        ${Object.entries(leaders).map(([key, value]) => `
                                            <option value="${key}" ${String(key) === String(user.phone_teamleader) ? 'selected' : ''}>
                                                ${key} - ${value}
                                            </option>
                                        `).join('')}
                                    </select>
                                    <button onclick="changeLeader('${user.phone_number}')">Сменить его</button>
                                </div>
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
                                <button onclick="updateRoles('${user.phone_number}')">Обновить роли</button>
                                <button onclick="setNewPass('${user.phone_number}')">Новый пароль</button>
                            </div>
                        `;
                        userList.appendChild(li);
                    });
                })
                .catch(error => {
                    console.error('Ошибка загрузки пользователей:', error);
                    alert('Не удалось загрузить пользователей');
                });
        })
        .catch(error => {
            console.error('Ошибка загрузки руководителей:', error);
            alert('Не удалось загрузить руководителей');
        });
}

// Функция для смены руководителя
function changeLeader(phoneNumber) {
    const selectElement = document.getElementById(`group_leader_${phoneNumber}`);
    const newLeader = selectElement.value;

    if (!newLeader) {
        alert('Пожалуйста, выберите нового руководителя.');
        return;
    }

    fetch('/auth/change-leader', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ phone_number: phoneNumber, new_leader: newLeader })
    })
        .then(response => {
            if (response.ok) {
                alert('Руководитель успешно изменен!');
                loadUsers();
            } else {
                alert('Ошибка при смене руководителя.');
            }
        })
        .catch(error => {
            console.error('Ошибка:', error);
            alert('Не удалось соединиться с сервером.');
        });
}

// Функция для обновления ролей пользователя
function updateRoles(phoneNumber) {
    // Получаем все чекбоксы для данного пользователя
    const userCheckboxes = Array.from(
        document.querySelectorAll(`#user-list li[data-phone="${phoneNumber}"] .role-checkboxes input[type="checkbox"]`)
    );
    const selectedRoles = userCheckboxes.filter(checkbox => checkbox.checked).map(checkbox => checkbox.value);

    // Отправляем POST-запрос на сервер FastAPI
    fetch('/auth/change-roles', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            phone_number: phoneNumber,
            roles: selectedRoles
        })
    })
        .then(response => {
            if (!response.ok) {
                return response.text().then(errorText => {
                    console.error('Ошибка ответа сервера:', errorText);
                    alert('Ошибка при отправке запроса. Проверьте корректность данных.');
                });
            }
            return response.json(); // Преобразуем ответ в JSON, если нужно
        })
        .then(data => {
            if (data) {
                alert(`Роли пользователя ${phoneNumber} успешно обновлены: ${selectedRoles.join(", ")}`);
                loadUsers();
            }
        })
        .catch(error => {
            console.error('Ошибка соединения с сервером:', error);
            alert('Не удалось соединиться с сервером.');
        });
}

// Функция для фильтрации пользователей
function filterUsers() {

    const phoneFilter = document.getElementById("filter-phone").value.trim();

    fetchUsers()
        .then(users => {
            // Фильтруем пользователей по номеру телефона
            const filteredUsers = users.filter(user => {
                return user.phone_number.includes(phoneFilter);
            });

            // Перерисовываем список пользователей
            renderUserList(filteredUsers);
        })
        .catch(error => {
            console.error('Ошибка загрузки пользователей:', error);
            alert('Не удалось загрузить пользователей');
        });
}

// Функция для отрисовки списка пользователей
function renderUserList(users) {
    const userList = document.getElementById("user-list");
    userList.innerHTML = ''; // Очищаем список перед загрузкой

    fetchLeaders()
        .then(leaders => {
            users.forEach(user => {
                const li = document.createElement("li");
                li.setAttribute("data-phone", user.phone_number);

                li.innerHTML = `
                    <div class="user-info2">
                        <span>Оператор: ${user.phone_number}</span>
                        <p>${user.oper_name || ''}</p>
                    </div>
                    <div class="form-group">
                        <label for="group_leader_${user.phone_number}">Ваш руководитель</label>
                        <div style="display: flex; align-items: center; gap: 10px;">
                            <select id="group_leader_${user.phone_number}" name="group_leader">
                                <option value="">-- Выберите руководителя --</option>
                                ${Object.entries(leaders).map(([key, value]) => `
                                    <option value="${key}" ${String(key) === String(user.phone_teamleader) ? 'selected' : ''}>
                                        ${key} - ${value}
                                    </option>
                                `).join('')}
                            </select>
                            <button onclick="changeLeader('${user.phone_number}')">Сменить его</button>
                        </div>
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
                        <button onclick="updateRoles('${user.phone_number}')">Обновить роли</button>
                        <button onclick="setNewPass('${user.phone_number}')">Новый пароль</button>
                    </div>
                `;
                userList.appendChild(li);
            });
        })
        .catch(error => {
            console.error('Ошибка загрузки руководителей:', error);
            alert('Не удалось загрузить руководителей');
        });
}

// Функция для открытия формы смены пароля
function setNewPass(phoneNumber) {
    // Создаем модальное окно
    const modal = document.createElement('div');
    modal.id = 'password-modal';
    modal.innerHTML = `
        <div class="modal-content">
            <h2>Смена пароля для ${phoneNumber}</h2>
            <form id="password-form">
                <label for="new-password">Новый пароль</label>
                <input type="password" id="new-password" name="new-password" required minlength="5" placeholder="Введите новый пароль">

                <label for="confirm-password">Подтверждение пароля</label>
                <input type="password" id="confirm-password" name="confirm-password" required minlength="5" placeholder="Повторите новый пароль">

                <button type="submit">Сменить пароль</button>
                <button type="button" id="close-modal">Отмена</button>
            </form>
        </div>
    `;
    document.body.appendChild(modal);

    // Добавляем обработчик для закрытия модального окна
    document.getElementById('close-modal').addEventListener('click', () => {
        document.body.removeChild(modal);
    });

    // Обработчик формы
    document.getElementById('password-form').addEventListener('submit', async (event) => {
        event.preventDefault();

        const newPassword = document.getElementById('new-password').value;
        const confirmPassword = document.getElementById('confirm-password').value;

        if (newPassword !== confirmPassword) {
            alert('Пароли не совпадают!');
            return;
        }

        try {
            const response = await fetch('/auth/change-password', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ phone_number: phoneNumber.toString(), password: newPassword })
            });

            if (response.ok) {
                alert('Пароль успешно изменен!');
                document.body.removeChild(modal);
            } else {
                alert('Ошибка при изменении пароля.');
            }
        } catch (error) {
            console.error('Ошибка:', error);
            alert('Не удалось соединиться с сервером.');
        }
    });
}
let filterTimeout; // Таймер для задержки фильтрации

document.getElementById("filter-phone").addEventListener("input", function () {
    clearTimeout(filterTimeout); // Сбрасываем предыдущий таймер

    const phoneFilter = this.value.trim();
    filterTimeout = setTimeout(() => {
        applyFilters(); // Запускаем фильтрацию
    }, 500); // Задержка 500 мс
});

// Обработчик изменения фильтра по ролям
document.getElementById("filter-role").addEventListener("change", function () {
    applyFilters(); // Запускаем фильтрацию при изменении роли
});

function applyFilters() {
    const phoneFilter = document.getElementById("filter-phone").value.trim();
    const roleFilter = document.getElementById("filter-role").value; // Получаем выбранную роль

    fetchUsers()
        .then(users => {
            const filteredUsers = users.filter(user => {
                const matchesPhone = user.phone_number.includes(phoneFilter);
                const matchesRole =
                    !roleFilter || // Если роль не выбрана, отображаем всех
                    (roleFilter === "Оператор" && user.is_operator) ||
                    (roleFilter === "Контроллер" && user.is_controller) ||
                    (roleFilter === "Руководитель" && user.is_teamlead);

                return matchesPhone && matchesRole;
            });

            renderUserList(filteredUsers);
        })
        .catch(error => {
            console.error('Ошибка загрузки пользователей:', error);
            alert('Не удалось загрузить пользователей');
        });
}

// Загружаем пользователей при загрузке страницы
window.onload = loadUsers;
