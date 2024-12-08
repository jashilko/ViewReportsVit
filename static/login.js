// Получаем элементы формы и сообщения об ошибке
const loginForm = document.getElementById('login-form');
const errorMessage = document.getElementById('error-message');

// Обработчик отправки формы
loginForm.addEventListener('submit', async function (event) {
    event.preventDefault();  // Отменяем стандартное поведение формы

    // Получаем данные из полей формы
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Создаем объект с данными для отправки
    const loginData = {
        username: username,
        password: password
    };

    // Отправляем POST-запрос на сервер
    try {
        const response = await fetch('http://127.0.0.1:8000/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        // Проверяем успешность запроса
        if (response.ok) {
            // Если запрос успешен, редиректим пользователя на другую страницу
            window.location.href = '/dashboard';  // Пример редиректа
        } else {
            // Если ошибка (например, неверные данные), показываем сообщение
            errorMessage.style.display = 'block';
        }
    } catch (error) {
        console.error('Ошибка при отправке данных:', error);
        alert('Произошла ошибка при попытке войти. Попробуйте снова.');
    }
});
