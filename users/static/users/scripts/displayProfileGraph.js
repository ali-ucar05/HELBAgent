document.addEventListener('DOMContentLoaded', function () {
        // Récupérer les données JSON
        const chartData = JSON.parse(
            document.getElementById('chartData').textContent
        );
        const dailyMessages = JSON.parse(
            document.getElementById('dailyMessages').textContent
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

        const labelsDaily = Object.keys(dailyMessages);
        const valuesDaily = Object.values(dailyMessages);

        const ctxDaily = document.getElementById('myChartDaily');

        new Chart(ctxDaily, {
            type: 'line', 
            data: {
                labels: labelsDaily,
                datasets: [{
                    label: 'Messages sent per day',
                    data: valuesDaily,
                    borderWidth: 1,
                    borderColor: 'rgba(75, 192, 192, 1)', 
                    tension: 0.4, 
                    fill: false
                }]
            },
            options: {
                scales: {
                    x: { 
                        title: {
                            display: true,
                            text: 'Date'
                        }
                    },
                    y: { 
                        title: {
                            display: true,
                            text: 'Number of messages'
                        },
                        beginAtZero: true
                    }
                }
            }
        });
    });