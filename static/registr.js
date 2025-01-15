// Получаем элементы формы и сообщения об ошибке
const loginForm = document.getElementById('login-form');
const errorMessage = document.getElementById('error-message');

const isLeaderCheckbox = document.getElementById('is_teamlead');
const groupLeaderSelect = document.getElementById('group_leader');

isLeaderCheckbox.addEventListener('change', () => {
    groupLeaderSelect.disabled = isLeaderCheckbox.checked;
    if (isLeaderCheckbox.checked) {
        groupLeaderSelect.value = ""
    }
});

// Обработчик отправки формы
loginForm.addEventListener('submit', async function (event) {
    event.preventDefault();  // Отменяем стандартное поведение формы

    // Получаем данные из полей формы
    const phone_number = document.getElementById('phone_number').value;
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;
    const isLeaderCheckbox = document.getElementById('is_teamlead').checked;
    const isControllerCheckbox = document.getElementById('is_controller').checked;
    const group_leader = document.getElementById('group_leader').value;

    // Проверяем совпадение паролей
    if (password !== confirmPassword) {
        alert('Пароли не совпадают. Пожалуйста, проверьте и повторите ввод.');
        return; // Прерываем отправку формы
    }

    // Создаем объект с данными для отправки
    const loginData = {
        phone_number: phone_number,
        password: password,
        is_teamlead: isLeaderCheckbox,
        is_controller: isControllerCheckbox,
        phone_teamleader: group_leader
    };

    // Отправляем POST-запрос на сервер
    try {
        const response = await fetch('/auth/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        // Проверяем успешность запроса
        if (response.ok) {
            // Если запрос успешен, редиректим пользователя на другую страницу
            window.location.href = '/users';  // Пример редиректа
        } else {
            // Если ошибка (например, неверные данные), показываем сообщение
            const errorData = await response.json();
            alert(errorData.detail)
            return;
        }
    } catch (error) {
        console.error('Ошибка при отправке данных:', error);
        alert('Произошла ошибка при попытке регистрации. Попробуйте снова.');
    }
});
