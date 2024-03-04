document.addEventListener('DOMContentLoaded', function() {
  const goalsDataElement = document.getElementById('goalsData');
  const completedGoals = parseInt(goalsDataElement.getAttribute('data-completed'), 10);
  const totalGoals = parseInt(goalsDataElement.getAttribute('data-total'), 10);
  const incompleteGoals = totalGoals - completedGoals;

  // Set new default font family and font color to mimic Bootstrap's default styling
  Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
  Chart.defaults.global.defaultFontColor = '#858796';

  // Doughnut Chart Example
  var ctx = document.getElementById("GoalChart");
  var myPieChart = new Chart(ctx, {
    type: 'doughnut',
    data: {
      labels: ["Completed Goals", "Incomplete Goals"],
      datasets: [{
        data: [completedGoals, incompleteGoals],
        backgroundColor: ['#4e73df', '#e74a3b'],
        hoverBackgroundColor: ['#2e59d9', '#de1c0b'],
        hoverBorderColor: "rgba(234, 236, 244, 1)",
      }],
    },
    options: {
      maintainAspectRatio: false,
      tooltips: {
        backgroundColor: "rgb(255,255,255)",
        bodyFontColor: "#858796",
        borderColor: '#dddfeb',
        borderWidth: 1,
        xPadding: 15,
        yPadding: 15,
        displayColors: false,
        caretPadding: 10,
      },
      legend: {
        display: true,  // Changed to true if you want to display the legend
        position: 'bottom'
      },
      cutoutPercentage: 80,
    },
  });
});