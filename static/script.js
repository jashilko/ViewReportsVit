document.getElementById("filter-button").addEventListener("click", (event) => {
    event.preventDefault();

    const dateFrom = document.getElementById("date_from").value;
    const dateTo = document.getElementById("date_to").value;
    const oper = document.getElementById("oper").value;

    const params = new URLSearchParams();
    if (dateFrom) params.append("date_from", dateFrom);
    if (dateTo) params.append("date_to", dateTo);
    if (oper) params.append("oper", oper);

    window.location.href = `/?${params.toString()}`;
});


async function logoutFunction() {
    try {
        // Отправка POST-запроса для удаления куки на сервере
        let response = await fetch('/auth/logout', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Проверка ответа сервера
        if (response.ok) {
            // Перенаправляем пользователя на страницу логина
            window.location.href = '/login';
        } else {
            // Чтение возможного сообщения об ошибке от сервера
            const errorData = await response.json();
            console.error('Ошибка при выходе:', errorData.message || response.statusText);
        }
    } catch (error) {
        console.error('Ошибка сети', error);
    }
}

// Загружаем список записей при загрузке страницы
//window.onload = () => displayRecordings(recordings);
