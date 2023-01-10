$(document).ready(function () {
    const getColorsConfig = (alpha) => ({
        backgroundColor: [
            `rgba(255, 99, 132, ${alpha})`,
            `rgba(54, 162, 235, ${alpha})`,
            `rgba(255, 206, 86, ${alpha})`,
            `rgba(75, 192, 192, ${alpha})`,
            `rgba(153, 102, 255, ${alpha})`,
            `rgba(255, 159, 64, ${alpha})`,
            `rgba(100, 159, 64, ${alpha})`,
            `rgba(159, 159, 64, ${alpha})`,
            `rgba(140, 255, 64, ${alpha})`,
            `rgba(50, 159, 140, ${alpha})`,
        ],
        borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)',
            'rgba(255, 159, 64, 1)',
            'rgba(100, 159, 64, 1)',
            'rgba(159, 159, 64, 1)',
            'rgba(140, 255, 64, 1)',
            'rgba(50, 159, 140, 1)',
        ],
        borderWidth: 1
    });

    const genresCtx = document.getElementById('genresChart').getContext('2d');
    const genresChart = new Chart(genresCtx, {
        type: 'bar',
        data: {
            labels: genres_breakdown.map(x => x.name),
            datasets: [{
                label: '# Songs Per Genre',
                data: genres_breakdown.map(x => x.songs_count),
                borderWidth: 1,
                ...getColorsConfig(0.2)
            }, {
                label: '# Artists Per Genre',
                data: genres_breakdown.map(x => x.artist_count),
                borderWidth: 1,
                ...getColorsConfig(0.4)
            }, {
                label: '# Albums Per Genre',
                data: genres_breakdown.map(x => x.albums_count),
                borderWidth: 1,
                ...getColorsConfig(0.6)
            }],

        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
    const top10ctx = document.getElementById('top10chart').getContext('2d');
    const top10Chart = new Chart(top10ctx, {
        type: 'doughnut',
        data: {
            labels: top10.map(x => x.name),
            datasets: [{
                label: '# of plays',
                data: top10.map(x => x.plays),
                borderWidth: 1,
                ...getColorsConfig(1)
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});
