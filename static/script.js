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

// Загружаем список записей при загрузке страницы
//window.onload = () => displayRecordings(recordings);
