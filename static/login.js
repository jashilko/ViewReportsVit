// Получаем элементы формы и сообщения об ошибке
const loginForm = document.getElementById('login-form');
const errorMessage = document.getElementById('error-message');

function openRegister() {
   alert('Обратитесь к администратору для регистрации пользователя');
}

// Обработчик отправки формы
loginForm.addEventListener('submit', async function (event) {
    event.preventDefault();  // Отменяем стандартное поведение формы

    // Получаем данные из полей формы
    const phone_number = document.getElementById('phone_number').value;
    const password = document.getElementById('password').value;

    // Создаем объект с данными для отправки
    const loginData = {
        phone_number: phone_number,
        password: password
    };

    // Отправляем POST-запрос на сервер
    try {
        const response = await fetch('/auth/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(loginData)
        });

        // Проверяем успешность запроса
        if (response.ok) {
            // Если запрос успешен, редиректим пользователя на другую страницу
            window.location.href = '/';  // Пример редиректа
        } else {
            // Если ошибка (например, неверные данные), показываем сообщение
            const errorData = await response.json();
            if (errorData && errorData.detail) {
                errorMessage.style.display = 'block';
                errorMessage.value =errorData.detail
               }

        }
    } catch (error) {
        console.error('Ошибка при отправке данных:', error);
        alert('Произошла ошибка при попытке войти. Попробуйте снова.');
    }
});
