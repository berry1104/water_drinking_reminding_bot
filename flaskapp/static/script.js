document.addEventListener('DOMContentLoaded', function () {
    const progressCtx = document.getElementById('progressChart').getContext('2d');
    const waterCup = document.getElementById('water-level');

    let progressChart = new Chart(progressCtx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [0, 2000], // Initial data, will be updated
                backgroundColor: [
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(255, 255, 255, 0.5)'
                ],
            }],
            labels: [
                'Drank',
                'Remaining'
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
        }
    });

    // Fetch data from the Flask app
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            // Process the data and update the chart
            let totalDrank = data.reduce((acc, entry) => acc + entry[2], 0);
            let remaining = 2000 - totalDrank; // 2000ml is the total capacity
            progressChart.data.datasets[0].data = [totalDrank, remaining];
            progressChart.update();

            // Update the cup visualization based on the data
            let cupHeight = 200; // The total height of the SVG container
            let waterLevel = (remaining / 2000) * cupHeight; // Calculate the water level based on the remaining amount

            waterCup.setAttribute('height', waterLevel.toString());
            waterCup.setAttribute('y', (cupHeight - waterLevel).toString());
        });
});
