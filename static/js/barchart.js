function barChart(labeldata, cdata) {

   var ridoChartData = {
      labels: labeldata,
      datasets: [
        {
          label: "Driver Cost",
          fillColor: "rgba(210, 214, 222, 1)",
          strokeColor: "rgba(210, 214, 222, 1)",
          pointColor: "rgba(210, 214, 222, 1)",
          pointStrokeColor: "#c1c7d1",
          pointHighlightFill: "#fff",
          pointHighlightStroke: "rgba(220,220,220,1)",
          data: cdata[0]
        },
        {
          label: "Car Cost",
          fillColor: "rgba(210, 214, 222, 1)",
          strokeColor: "rgba(210, 214, 222, 1)",
          pointColor: "rgba(210, 214, 222, 1)",
          pointStrokeColor: "#c1c7d1",
          pointHighlightFill: "#fff",
          pointHighlightStroke: "rgba(220,220,220,1)",
          data: cdata[1]
        },
        
      ]
    };


    var barChartCanvas = $("#barchart").get(0).getContext("2d");
    var barChart = new Chart(barChartCanvas);
    var barChartData = ridoChartData;
    barChartData.datasets[0].fillColor = "#00c0ef";
    barChartData.datasets[0].strokeColor = "#00c0ef";
    barChartData.datasets[0].pointColor = "#00c0ef";

    barChartData.datasets[1].fillColor = "#f56954";
    barChartData.datasets[1].strokeColor = "#f56954";
    barChartData.datasets[1].pointColor = "#f56954";

    var barChartOptions = {
      scaleBeginAtZero: true,
      scaleShowGridLines: true,
      scaleGridLineColor: "rgba(0,0,0,.05)",
      scaleGridLineWidth: 1,
      scaleShowHorizontalLines: true,
      scaleShowVerticalLines: true,
      barShowStroke: true,
      barStrokeWidth: 2,
      barValueSpacing: 5,
      barDatasetSpacing: 1,
      legendTemplate: "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].fillColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>",
      responsive: true,
      maintainAspectRatio: true
    };

    barChartOptions.datasetFill = false;
    barChart.Bar(barChartData, barChartOptions);
}
