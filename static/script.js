

function logout()
{
// Отправляем POST-запрос на сервер
    try {
        const response = fetch('/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: {}
        });
        console.error('Ответ', response);
        // Проверяем успешность запроса
        // Проверяем успешность запроса
        if (response.ok) {
            // Если запрос успешен, редиректим пользователя на другую страницу
            window.location.href = '/login';  // Редирект
        } else {
            // Если ошибка (например, неверные данные), показываем сообщение
            const errorData = response.json();
            if (errorData && errorData.detail) {
                errorMessage.style.display = 'block';
                errorMessage.value =errorData.detail
               }

        }
    } catch (error) {
        console.error('Ошибка', error);
        alert('Произошла ошибка при попытке войти. Попробуйте снова.');
    }
}

// Загружаем список записей при загрузке страницы
//window.onload = () => displayRecordings(recordings);
