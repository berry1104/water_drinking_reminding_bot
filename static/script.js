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
