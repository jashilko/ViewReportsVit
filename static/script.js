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


document.getElementById("phone-filter").addEventListener("input", function () {
    let filter = this.value.trim();
    let rows = document.querySelectorAll("#recordings-table tbody tr");

    rows.forEach(row => {
        let src = row.cells[2].textContent.trim(); // Колонка "Кто звонил"
        let dst = row.cells[3].textContent.trim(); // Колонка "Кому звонили"

        if (src.includes(filter) || dst.includes(filter)) {
            row.style.display = "";
        } else {
            row.style.display = "none";
        }
    });
});

// Загружаем список записей при загрузке страницы
//window.onload = () => displayRecordings(recordings);
