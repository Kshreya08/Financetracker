// ===================== Chart Handling =====================
const ctx = document.getElementById('spendingTrendChart')?.getContext('2d');
let spendingTrendChart;

function loadChartData() {
    fetch('http://127.0.0.1:5000/api/expenses')
        .then(res => res.json())
        .then(data => {
            const labels = data.map(item => item.feature);
            const values = data.map(item => item.amount);

            if (spendingTrendChart) {
                spendingTrendChart.data.labels = labels;
                spendingTrendChart.data.datasets[0].data = values;
                spendingTrendChart.update();
            } else if (ctx) {
                spendingTrendChart = new Chart(ctx, {
                    type: 'line',
                    data: {
                        labels: labels,
                        datasets: [{
                            label: 'Monthly Expenses',
                            data: values,
                            borderColor: 'rgba(75, 192, 192, 1)',
                            backgroundColor: 'rgba(75, 192, 192, 0.2)',
                            borderWidth: 2,
                            pointRadius: 5,
                            pointBackgroundColor: 'purple',
                            tension: 0.4
                        }]
                    },
                    options: {
                        responsive: true,
                        plugins: {
                            tooltip: {
                                callbacks: {
                                    label: function (tooltipItem) {
                                        return `Expense: ₹${tooltipItem.raw}`;
                                    }
                                }
                            }
                        },
                        scales: {
                            y: {
                                beginAtZero: true,
                                title: {
                                    display: true,
                                    text: 'Expenses (₹)'
                                }
                            },
                            x: {
                                title: {
                                    display: true,
                                    text: 'Features and Benefits'
                                }
                            }
                        }
                    }
                });
            }
        })
        .catch(error => {
            console.error("Error loading chart data:", error);
        });
}

function addSampleExpenses() {
    const testData = [
        { feature: 'View balances across bank accounts', amount: 6000 },
        { feature: 'One place for all transactions', amount: 4500 },
        { feature: 'See where you spend the most', amount: 3000 },
        { feature: 'Get consolidated', amount: 1500 },
        { feature: 'Track your FDs', amount: 1000 },
        { feature: 'Sync multiple', amount: 500 }
    ];

    testData.forEach(item => {
        fetch('http://127.0.0.1:5000/api/expenses', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(item)
        })
        .then(() => loadChartData());
    });
}

// ===================== User Registration =====================
function registerUser() {
    const account = document.getElementById('account')?.value;
    const email = document.getElementById('email')?.value;

    if (!account || !email) {
        document.getElementById('response').innerText = 'Please enter both account number and email.';
        return;
    }

    fetch('http://127.0.0.1:5000/api/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ account, email })
    })
    .then(response => {
        if (response.status === 201) {
            // Redirect to personal.html on successful registration
            window.location.href = 'personal.html';
        } else {
            return response.json().then(data => {
                document.getElementById('response').innerText = data.error || 'Registration failed.';
            });
        }
    })
    .catch(error => {
        document.getElementById('response').innerText = 'An error occurred: ' + error;
    });
}

// ===================== Auto Load =====================
window.addEventListener('DOMContentLoaded', () => {
    loadChartData(); // Load chart only if canvas exists
});
