document.addEventListener('DOMContentLoaded', function () {
    // This function sets the water level background
    function setWaterLevelBackground(percentage) {

        // Set the background of the body to a linear gradient
        document.body.style.backgroundImage = `linear-gradient(
            to top,
            #98CCFFAA 0%,
            #98CCFFAA ${percentage}%,
            #98CCFF30 ${percentage}%,
            #98CCFF30 100%
        )`;

        // This makes the gradient background cover the entire body, with no repetition
        document.body.style.backgroundSize = 'cover';
    }

    // Function to update the header message with water consumption info
    function updateWaterConsumptionHeader(totalDrank) {
        const remaining = Math.max(0, 2000 - totalDrank); // Ensure it doesn't go negative

        // Construct the message
        const message = `You have had ${totalDrank}mL today. Drink ${remaining}mL more to reach your 2000mL daily goal.`;

        // Select the header element and update its content
        document.getElementById('waterConsumptionHeader1').textContent = `${totalDrank}mL / ${remaining}mL`;
        document.getElementById('waterConsumptionHeader2').textContent = message;
    }

    // Fetch data from the Flask app
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            // Process the data
            let totalDrank = data.reduce((acc, entry) => acc + entry[2], 0);
            if (totalDrank > 2000) {
                totalDrank = 2000; // Cap at 2000mL
            }

            // Calculate the percentage of the screen to fill
            let percentage = (totalDrank / 2000) * 100;

            // Set the water level background
            setWaterLevelBackground(percentage);

            // Update the header message based on the total water drank
            updateWaterConsumptionHeader(totalDrank);
            
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
    

        
    const progressCtx = document.getElementById('progressChart').getContext('2d');
    const waterCup = document.getElementById('water-level');

    let progressChart = new Chart(progressCtx, {
        type: 'doughnut',
        data: {
            datasets: [{
                data: [0, 2000], // Initial data, will be updated
                backgroundColor: [
                    'rgba(54, 162, 235, 0.5)',
                    'rgba(200, 200, 200, 0.5)'
                ],
            }],
            labels: [
                'Drank',
                'Remaining'
            ]
        },
        options: {
            responsive: false,
            maintainAspectRatio: true,
        }
    });

    // Fetch data from the Flask app
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            // Process the data and update the chart
            let totalDrank = data.reduce((acc, entry) => acc + entry[2], 0);
            if (totalDrank > 2000) {
                totalDrank = 2000;
            }
            let remaining = 2000 - totalDrank; // 2000ml is the total capacity
            progressChart.data.datasets[0].data = [totalDrank, remaining];
            progressChart.update();

            // Update the cup visualization based on the data
            let cupHeight = 200; // The total height of the SVG container
            let waterLevel = (remaining / 2000) * cupHeight; // Calculate the water level based on the remaining amount
            // Ensure water level is within the bounds
            // waterLevel = Math.max(0, Math.min(waterLevel, cupHeight));

            waterCup.setAttribute('height', waterLevel.toString());
            waterCup.setAttribute('y', (cupHeight - waterLevel).toString());
        });

    // // Function to update the line chart based on the selected time period
    // function updateLineChart(period) {
    //     fetch(`/data/${period}`)
    //         .then(response => response.json())
    //         .then(data => {
    //             console.log(data);
    //             // let labels = data.map(entry => new Date(entry[0]).toLocaleTimeString()); // Adjust if your timestamp format differs
    //             let labels = data.map(entry => entry[0]);
    //             let dataPoints = data.map(entry => entry[2]); // Adjust based on where your data point is within each entry

    //             // If the chart already exists, destroy it before creating a new one
    //             if (window.lineChartInstance) {
    //                 window.lineChartInstance.destroy();
    //             }

    //             window.lineChartInstance = new Chart(document.getElementById('lineChart'), {
    //                 type: 'line',
    //                 data: {
    //                     labels: labels,
    //                     datasets: [{
    //                         label: 'Water Consumption',
    //                         data: dataPoints,
    //                         fill: false,
    //                         borderColor: 'rgb(75, 192, 192)',
    //                         tension: 0.1
    //                     }]
    //                 },
    //                 options: {
    //                     responsive: true,
    //                     maintainAspectRatio: false,
    //                     scales: {
    //                         x: {
    //                             type: 'time',
    //                             time: {
    //                                 unit: period === '24h' ? 'hour' : 'day'
    //                             }
    //                         }
    //                     }
    //                 }
    //             });
    //         });
    // }

    // // Initial chart load
    // updateLineChart('24h'); // Default period

    // // Event listener for the dropdown change
    // document.getElementById('timePeriod').addEventListener('change', function() {
    //     let selectedPeriod = this.value;
    //     updateLineChart(selectedPeriod);
    // });



    // fetch('/data/last_24_hours')
    // .then(response => response.json())
    // .then(data => {
    //     // Assuming 'data' is an array of records and each record is an array like [id, timestamp, amount]
    //     const labels = data.map(record => record[1]); // extract timestamps
    //     const dataPoints = data.map(record => record[2]); // extract amounts

    //     // If the chart already exists, destroy it before creating a new one
    //     if (window.lineChartInstance) {
    //         window.lineChartInstance.destroy();
    //     }

    //     window.lineChartInstance = new Chart(document.getElementById('lineChart'), {
    //         type: 'line',
    //         data: {
    //             labels: labels,
    //             datasets: [{
    //                 label: 'Water Consumption',
    //                 data: dataPoints,
    //                 fill: false,
    //                 borderColor: 'rgb(75, 192, 192)',
    //                 tension: 0.1
    //             }]
    //         },
    //         options: {
    //             responsive: true,
    //             maintainAspectRatio: false,
    //             scales: {
    //                 x: {
    //                     type: 'time',
    //                     time: {
    //                         unit: period === '24h' ? 'hour' : 'day'
    //                     }
    //                 }
    //             }
    //         }
    //     });
    // })
    // .catch(error => {
    //     console.error('Error fetching data:', error);
    // });








    // Function to create/update the line chart
    function createLineChart(data) {
        // Prepare data points and labels from the data
        // let labels = data.map(entry => entry[0]); // Assuming entry[0] is your time data
        // let dataPoints = data.map(entry => entry[2]); // Assuming entry[2] is your measurement data

        const labels = data.map(record => record[1]); // extract timestamps
        const dataPoints = data.map(record => record[2]); // extract amounts

        // Create the line chart
        let ctx = document.getElementById('lineChart').getContext('2d');
        let lineChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Water Intake',
                    data: dataPoints,
                    fill: true,
                    borderColor: 'blue',
                    tension: 0.1
                }]
            },
            options: {
                // ... [any specific options you want for the line chart] ...
            }
        });
    }

    // Fetch the data and create the chart
    fetch('/data/last_24_hours') // Make sure this URL is correct and the server is returning the expected data
        .then(response => response.json())
        .then(data => {
            createLineChart(data);
        })
        .catch(error => {
            console.error('Error fetching data:', error);
        });
});












// JavaScript 代码
const waterLevel = document.getElementById('water-level');
const amountDisplay = document.getElementById('amount-display');
const dataBody = document.getElementById('data-body');
const totalAmountDisplay = document.getElementById('total-amount');
const startButton = document.getElementById('start-button');
const stopButton = document.getElementById('stop-button');

// 设置定时刷新，这里的时间间隔是毫秒
const refreshInterval = 60000; // 60秒

function autoRefresh() {
    // 执行你想要刷新的操作，例如重新获取数据或重载页面
    location.reload(); // 这会刷新整个页面

    // 或者你可以触发一个特定的操作
    // fetch('/get_data'); // 例如，重新获取数据
}

// 设置定时器，以每隔指定时间间隔自动执行 autoRefresh 函数
const refreshTimer = setInterval(autoRefresh, refreshInterval);

// start button event listeners
startButton.addEventListener('click', () => {
    // run water_BCM.py
    fetch('../start', {
        method: 'POST'
    });


    
});


// stop button event listeners
stopButton.addEventListener('click', () => {
    // stop water_BCM.py
    fetch('../stop', {
        method: 'POST'
    });
});



// variable to track the total amount of water consumed
let totalAmount = 0;

// 从服务器获取数据
fetch('/get_data')
    .then(response => response.json())
    .then(data => {
        // 处理从服务器获取的数据
        console.log(data);  // 在控制台输出数据

        // 清空数据表格
        dataBody.innerHTML = '';

        // 更新页面以显示数据
        data.forEach(entry => {
            const row = document.createElement('tr');
            const timeCell = document.createElement('td');
            const amountCell = document.createElement('td');

            timeCell.textContent = entry[1];  // entry[1] 是时间
            amountCell.textContent = entry[2];  // entry[2] 是饮水量

            // 更新总饮水量
            totalAmount += entry[2];

            row.appendChild(timeCell);
            row.appendChild(amountCell);

            dataBody.appendChild(row);
        });

        // 更新总饮水量的显示
        totalAmountDisplay.textContent = `Total Amount: ${totalAmount} ml`;
    })
    .catch(error => console.error(error));
