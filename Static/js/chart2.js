var ctx2 = document.getElementById('doughnut').getContext('2d');
var myChart2 = new Chart(ctx2, {
    type: 'doughnut',
    data: {
        labels: ['Earnings', 'Expenditure', 'Salary', 'Others'],

        datasets: [{
            label: 'Employees',
            data: [40, 30, 20, 10],
            backgroundColor: [
                'rgba(111, 78, 55, 1)',
                'rgba(135, 206, 235,1)',
                'rgba(255, 206, 86, 1)',
                'rgba(144, 238, 144,1)'

            ],
            borderColor: [
                'rgba(111, 78, 55, 1)',
                'rgba(135, 206, 235,1)',
                'rgba(255, 206, 86, 1)',
                'rgba(144, 238, 144,1)'

            ],
            borderWidth: 1
        }]

    },
    options: {
        responsive: true
    }
});