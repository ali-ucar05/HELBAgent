document.addEventListener('DOMContentLoaded', function () {
    // Récupération des données JSON
    const chartData = JSON.parse(
        document.getElementById('chartData').textContent
    );

    const labels1 = Object.keys(chartData);
    const values1 = Object.values(chartData);

    const ctx1 = document.getElementById('myChart');

    new Chart(ctx1, {
        type: 'bar',
        data: {
            labels: labels1,
            datasets: [{
                label: 'Number of messages sent',
                data: values1,
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: { beginAtZero: true }
            }
        }
    });
});