var color = Chart.helpers.color;

window.chartColors = {
    red: 'rgb(255, 99, 132)',
    orange: 'rgb(255, 159, 64)',
    yellow: 'rgb(255, 205, 86)',
    green: 'rgb(75, 192, 192)',
    blue: 'rgb(54, 162, 235)',
    purple: 'rgb(153, 102, 255)',
    grey: 'rgb(201, 203, 207)'
};
var cfg = {
    data: {
        datasets: [{

            backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
            borderColor: window.chartColors.red,
            data: [],
            type: 'scatter',
            showLine: false,
            pointRadius: 2,
            borderWidth: 0,
            fill: false,
            lineTension: 0
        }]
    },
    options: {
        legend: {
            display: false
        },
        animation: {
            duration: 2
        },
        scales: {
            xAxes: [{
                type: 'time',
                distribution: 'series',
                offset: true,
                ticks: {
                    major: {
                        enabled: true,
                        fontStyle: 'bold'
                    },
                    source: 'data',
                    autoSkip: true,
                    autoSkipPadding: 75,
                    maxRotation: 0,
                    sampleSize: 100
                },

            }],
            yAxes: [{
                gridLines: {
                    drawBorder: false
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Heart Rate (BPM)'
                },
                autoSkip: true,
                autoSkipPadding: 15,
                ticks: {
                    min: 30,    // minimum will be 0, unless there is a lower value.
                    max: 180,
                    stepSize: 10
                }
            }]
        },
        tooltips: {
            intersect: false,
            mode: 'index',
            callbacks: {
                label: function (tooltipItem, myData) {
                    var label = myData.datasets[tooltipItem.datasetIndex].label || '';
                    if (label) {
                        label += ': ';
                    }
                    label += parseFloat(tooltipItem.value).toFixed(2);
                    return label;
                }
            }
        }
    }
};

var cfg_spo2 = {
    data: {
        datasets: [{

            backgroundColor: color(window.chartColors.green).alpha(0.5).rgbString(),
            borderColor: window.chartColors.green,
            data: [],
            type: 'scatter',
            showLine: false,
            pointRadius: 2,
            borderWidth: 0,
            fill: false,
            lineTension: 0
        }]
    },
    options: {
        legend: {
            display: false
        },
        animation: {
            duration: 2
        },
        scales: {
            xAxes: [{
                type: 'time',
                distribution: 'series',
                offset: true,
                ticks: {
                    major: {
                        enabled: true,
                        fontStyle: 'bold'
                    },
                    source: 'data',
                    autoSkip: true,
                    autoSkipPadding: 75,
                    maxRotation: 0,
                    sampleSize: 100
                },

            }],
            yAxes: [{
                gridLines: {
                    drawBorder: false
                },
                scaleLabel: {
                    display: true,
                    labelString: 'RR (avg)'
                },
                autoSkip: true,
                autoSkipPadding: 15,
                ticks: {
                    stepSize: 0.1,
                    suggestedMin: 0,    // minimum will be 0, unless there is a lower value.
                    suggestedMax: 30   // minimum value will be 0.
                }
            }]
        },
        tooltips: {
            intersect: false,
            mode: 'index',
            callbacks: {
                label: function (tooltipItem, myData) {
                    var label = myData.datasets[tooltipItem.datasetIndex].label || '';
                    if (label) {
                        label += ': ';
                    }
                    label += parseFloat(tooltipItem.value).toFixed(2);
                    return label;
                }
            }
        }
    }
};

var cfg1 = {
    data: {
        datasets: [{

            backgroundColor: color(window.chartColors.blue).alpha(0.8).rgbString(),
            borderColor: window.chartColors.blue,
            data: [],
            type: 'bar',
            pointRadius: 0,
            fill: false,
            lineTension: 0,
            borderWidth: 0
        }]
    },
    options: {
        legend: {
            display: false
        },
        animation: {
            duration: 0
        },
        scales: {
            xAxes: [{
                type: 'time',
                distribution: 'series',
                offset: true,
                ticks: {
                    major: {
                        enabled: true,
                        fontStyle: 'bold'
                    },
                    source: 'data',
                    autoSkip: true,
                    autoSkipPadding: 75,
                    maxRotation: 0,
                    sampleSize: 100
                },

            }],
            yAxes: [{
                gridLines: {
                    drawBorder: false
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Steps'
                },
                autoSkip: true,
                autoSkipPadding: 100,

            }]
        },
        tooltips: {
            intersect: false,
            mode: 'index',
            callbacks: {
                label: function (tooltipItem, myData) {
                    var label = myData.datasets[tooltipItem.datasetIndex].label || '';
                    if (label) {
                        label += ': ';
                    }
                    label += parseFloat(tooltipItem.value).toFixed(2);
                    return label;
                }
            }
        }
    }
};

var cfg2 = {
    data: {
        datasets: [{

            backgroundColor: color(window.chartColors.orange).alpha(0.5).rgbString(),
            borderColor: window.chartColors.orange,
            data: [],
            type: 'line',
            pointRadius: 0,
            borderWidth: 0.5,
            fill: false,
            lineTension: 0,
            borderWidth: 2
        }]
    },
    options: {
        legend: {
            display: false
        },
        animation: {
            duration: 2
        },
        scales: {
            xAxes: [{
                type: 'time',
                distribution: 'series',
                offset: true,
                ticks: {
                    major: {
                        enabled: true,
                        fontStyle: 'bold'
                    },
                    source: 'data',
                    autoSkip: true,
                    autoSkipPadding: 75,
                    maxRotation: 0,
                },

            }],
            yAxes: [{
                gridLines: {
                    drawBorder: false
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Battery Level'
                },
                autoSkip: true,
                ticks: {
                    suggestedMin: 0,    // minimum will be 0, unless there is a lower value.
                    // OR //
                    beginAtZero: true   // minimum value will be 0.
                }
            }]
        },
        tooltips: {
            intersect: false,
            mode: 'index',
            callbacks: {
                label: function (tooltipItem, myData) {
                    var label = myData.datasets[tooltipItem.datasetIndex].label || '';
                    if (label) {
                        label += ': ';
                    }
                    label += parseFloat(tooltipItem.value).toFixed(2);
                    return label;
                }
            }
        }
    }
};

var sleepcfg = {
    data: {
        // yLabels: ['Deep','Light','REM','Awake'],
        datasets: [{
            data: [],
            type: 'bar',
            showLine: false,
            // pointRadius: 4,
            // borderWidth: 0,
            fill: false,
            lineTension: 0
        }]
    },
    options: {
        legend: {
            display: false
        },
        animation: {
            duration: 2
        },
        scales: {
            xAxes: [{
                type: 'time',
                distribution: 'series',
                gridLines: {
                    display: false
                },

                ticks: {
                    major: {
                        enabled: true,
                        fontStyle: 'bold'
                    },
                    source: 'data',
                    autoSkip: true,
                    autoSkipPadding: 75,
                    maxRotation: 0,
                    sampleSize: 100
                },

            }],

            yAxes: [{
                gridLines: {
                    display: true
                },
                scaleLabel: {
                    display: false,
                },
                // type: 'category',
                ticks: {
                    suggestedMin: 0,    // minimum will be 0, unless there is a lower value.
                    // OR //
                    // display: false,
                    stepSize: 1,
                    fontColor: "#121a2e",
                    beginAtZero: true,   // minimum value will be 0.
                    callback: function (value) {
                        var x = ["", "Deep", "Light", "REM", "Awake"];
                        return x[value | 0];
                    }
                }
            }]
        },
        tooltips: {
            intersect: false,
            mode: 'index',
            callbacks: {
                label: function (tooltipItem, myData) {
                    var label = ""
                    return label;
                }
            }
        }
    }
};

var annotation_cfg = {
    data: {
        datasets: [
            {
                backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
                borderColor: window.chartColors.red,
                label: 'X',
                data: [],
                type: 'line',
                showLine: true,
                pointRadius: 0,
                borderWidth: 0,
                fill: false,
                lineTension: 1
            },
            {
                backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
                borderColor: window.chartColors.blue,
                label: 'Y',
                data: [],
                type: 'line',
                showLine: true,
                pointRadius: 0,
                borderWidth: 0,
                fill: false,
                lineTension: 1
            },
            {
                backgroundColor: color(window.chartColors.red).alpha(0.5).rgbString(),
                borderColor: window.chartColors.yellow,
                label: 'Z',
                data: [],
                type: 'line',
                showLine: true,
                pointRadius: 0,
                borderWidth: 0,
                fill: false,
                lineTension: 1
            }
        ]
    },
    options: {
        legend: {
            display: true,
            legendText: ['X', 'Y', 'Z']
        },
        animation: {
            duration: 4
        },
        scales: {
            xAxes: [{
                type: 'time',
                distribution: 'series',
                offset: true,
                ticks: {
                    major: {
                        enabled: true,
                        fontStyle: 'bold'
                    },
                    source: 'data',
                    autoSkip: true,
                    autoSkipPadding: 75,
                    maxRotation: 0,
                    sampleSize: 100
                },

            }],
            yAxes: [{
                gridLines: {
                    display:false,
                    drawBorder: false
                },
                scaleLabel: {
                    display: true,
                    labelString: 'Accelerometer (X,Y,Z)'
                },
                autoSkip: true,
                // ticks: {
                //     min: 0,    // minimum will be 0, unless there is a lower value.
                //     max: 10,
                //     stepSize: 1
                // }
            }]
        },
        showTooltips: false,
        hover: {mode: null},
        tooltips: {
            enabled: false
        }
    }
};