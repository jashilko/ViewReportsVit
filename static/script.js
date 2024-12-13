// Пример данных с фамилией, временем записи и аудиофайлами
const recordings = [
    { id: 1, surname: 'Иванов', name: 'Запись 1', file: 'audio/record1.mp3', time: '09:30' },
    { id: 2, surname: 'Петров', name: 'Запись 2', file: 'audio/record2.mp3', time: '10:15' },
    { id: 3, surname: 'Смирнов', name: 'Запись 3', file: 'audio/record3.mp3', time: '11:45' },
    { id: 4, surname: 'Иванов', name: 'Запись 4', file: 'audio/record4.mp3', time: '14:00' },
    { id: 5, surname: 'Смирнов', name: 'Запись 5', file: 'audio/record5.mp3', time: '15:30' },
    { id: 6, surname: 'Петров', name: 'Запись 6', file: 'audio/record6.mp3', time: '17:00' }
];

// Функция для отображения списка записей в таблице
function displayRecordings(filteredRecordings) {
    try{
        const response = await fetch('/reports');

        if (!response.ok) {
            // Получаем данные об ошибке
            const errorData = await response.json();
            //displayErrors(errorData);  // Отображаем ошибки
            return;  // Прерываем выполнение функции
        }
        const reports = await response.json();
    }
    } catch (error) {
        console.error('Ошибка:', error);
        alert('Произошла ошибка при регистрации. Пожалуйста, попробуйте снова.');
    }
    const tableBody = document.querySelector('#recordings-table tbody');
    tableBody.innerHTML = ''; // очищаем таблицу перед загрузкой

    filteredRecordings.forEach(recording => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${recording.surname}</td>
            <td>${recording.name}</td>
            <td>${recording.time}</td>
            <td>
                <audio controls>
                    <source src="${recording.file}" type="audio/mp3">
                    Ваш браузер не поддерживает элемент audio.
                </audio>
            </td>
        `;
        tableBody.appendChild(row);
    });
}

// Фильтрация записей по времени и фамилии
function filterByTimeAndSurname() {
    const startTime = document.getElementById('start-time').value;
    const endTime = document.getElementById('end-time').value;
    const surnameFilter = document.getElementById('surname').value.toLowerCase();

    const filteredRecordings = recordings.filter(recording => {
        const isMatchingSurname = surnameFilter ? recording.surname.toLowerCase().includes(surnameFilter) : true;
        const isAfterStartTime = startTime ? recording.time >= startTime : true;
        const isBeforeEndTime = endTime ? recording.time <= endTime : true;
        return isMatchingSurname && isAfterStartTime && isBeforeEndTime;
    });

    displayRecordings(filteredRecordings);
}

// Загружаем список записей при загрузке страницы
//window.onload = () => displayRecordings(recordings);
