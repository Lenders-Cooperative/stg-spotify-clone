const genreSummary = JSON.parse($('#genre-summary').text())
const datasetConfig = {
    backgroundColor: [
        'rgba(255, 99, 132, 0.2)',
        'rgba(54, 162, 235, 0.2)',
        'rgba(255, 206, 86, 0.2)',
        'rgba(75, 192, 192, 0.2)',
        'rgba(153, 102, 255, 0.2)',
        'rgba(255, 159, 64, 0.2)'
    ],
    borderColor: [
        'rgba(255, 99, 132, 1)',
        'rgba(54, 162, 235, 1)',
        'rgba(255, 206, 86, 1)',
        'rgba(75, 192, 192, 1)',
        'rgba(153, 102, 255, 1)',
        'rgba(255, 159, 64, 1)'
    ],
    borderWidth: 1
}
const chartConfig = {
    type: 'bar',
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
}

const songChart = new Chart($('#song-chart')[0].getContext('2d'), {
    ...chartConfig,
    data: {
        labels: genreSummary.labels,
        datasets: [{
            ...datasetConfig,
            label: 'Songs per Genre',
            data: genreSummary.songs
        }]
    }
});

const playChart = new Chart($('#play-chart')[0].getContext('2d'), {
    ...chartConfig,
    data: {
        labels: genreSummary.labels,
        datasets: [{
            ...datasetConfig,
            label: 'Plays per Genre',
            data: genreSummary.plays
        }]
    }
});
