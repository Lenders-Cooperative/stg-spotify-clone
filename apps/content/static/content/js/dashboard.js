$(document).ready(function () {
    let genreChart = null;
    let songChart = null;
    function genreChartInit() {
        const ctx = document.getElementById('genreChart').getContext('2d');
        genreChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: genreData.map(genre => genre.name),
                datasets: [{
                    label: 'Artists',
                    data: genreData.map(genre => genre.artist_count),
                    backgroundColor: [
                        'rgba(166, 206, 227, 0.2)',
                        'rgba(31, 120, 180, 0.2)',
                        'rgba(178, 223, 138, 0.2)',
                        'rgba(51, 160, 44, 0.2)',
                        'rgba(251, 154, 153, 0.2)',
                        'rgba(227, 26, 28, 0.2)',
                        'rgba(253, 191, 111, 0.2)',
                        'rgba(255, 127, 0, 0.2)',
                        'rgba(202, 178, 214, 0.2)',
                        'rgba(106, 61, 154, 0.2)',
                    ],
                    borderColor: [
                        'rgba(166, 206, 227, 1)',
                        'rgba(31, 120, 180, 1)',
                        'rgba(178, 223, 138, 1)',
                        'rgba(51, 160, 44, 1)',
                        'rgba(251, 154, 153, 1)',
                        'rgba(227, 26, 28, 1)',
                        'rgba(253, 191, 111, 1)',
                        'rgba(255, 127, 0, 1)',
                        'rgba(202, 178, 214, 1)',
                        'rgba(106, 61, 154, 1)',
                    ],
                    borderWidth: 1,
                }],
            },
            options: {
                plugins: {
                    title: {
                        text: '# Artists per Genre',
                    },
                },
                scales: {
                    y: {
                        beginAtZero: true,
                    },
                },
            },
        });
    }
    genreChartInit();
    const genreArtistBtn = $('.genre-artist-btn.nav-link');
    const genreAlbumBtn = $('.genre-album-btn.nav-link');
    const genreSongBtn = $('.genre-song-btn.nav-link');

    genreArtistBtn.click(() => {
        if (genreChart !== null) {
            genreChart.data.datasets[0].data = genreData.map(genre => genre.artist_count);
            genreChart.data.datasets[0].label = 'Artists';
            genreChart.update();
            genreAlbumBtn.removeClass('active');
            genreSongBtn.removeClass('active');
            genreArtistBtn.addClass('active');
        }
    });

    genreAlbumBtn.click(() => {
        if (genreChart !== null) {
            genreChart.data.datasets[0].data = genreData.map(genre => genre.album_count);
            genreChart.data.datasets[0].label = 'Albums';
            genreChart.update();
            genreArtistBtn.removeClass('active');
            genreSongBtn.removeClass('active');
            genreAlbumBtn.addClass('active');
        }
    });

    genreSongBtn.click(() => {
        if (genreChart !== null) {
            genreChart.data.datasets[0].data = genreData.map(genre => genre.song_count);
            genreChart.data.datasets[0].label = 'Songs';
            genreChart.update();
            genreArtistBtn.removeClass('active');
            genreAlbumBtn.removeClass('active');
            genreSongBtn.addClass('active');
        }
    });

    function songChartInit() {
        const ctx = document.getElementById('songChart').getContext('2d');
        songChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: songData.map(song => song.artist_name),
                datasets: [{
                    label: 'Plays',
                    data: songData.map(song => song.plays),
                    backgroundColor: [
                        'rgba(166, 206, 227, 0.2)',
                        'rgba(31, 120, 180, 0.2)',
                        'rgba(178, 223, 138, 0.2)',
                        'rgba(51, 160, 44, 0.2)',
                        'rgba(251, 154, 153, 0.2)',
                        'rgba(227, 26, 28, 0.2)',
                        'rgba(253, 191, 111, 0.2)',
                        'rgba(255, 127, 0, 0.2)',
                        'rgba(202, 178, 214, 0.2)',
                        'rgba(106, 61, 154, 0.2)',
                    ],
                    borderColor: [
                        'rgba(166, 206, 227, 1)',
                        'rgba(31, 120, 180, 1)',
                        'rgba(178, 223, 138, 1)',
                        'rgba(51, 160, 44, 1)',
                        'rgba(251, 154, 153, 1)',
                        'rgba(227, 26, 28, 1)',
                        'rgba(253, 191, 111, 1)',
                        'rgba(255, 127, 0, 1)',
                        'rgba(202, 178, 214, 1)',
                        'rgba(106, 61, 154, 1)',
                    ],
                    borderWidth: 1,
                }],
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                    },
                },
            },
        });
    }
    songChartInit();

    const songTableBtn = $('.song-table-btn.nav-link');
    const songChartBtn = $('.song-chart-btn.nav-link');
    const songTable = $('.song-table');
    const songChartContainer = $('.song-chart-container');

    songTableBtn.click(() => {
        songTable.show();
        songChartContainer.hide();
        songChartBtn.removeClass('active');
        songTableBtn.addClass('active');
    });

    songChartBtn.click(() => {
        songTable.hide();
        songChartContainer.show();
        songTableBtn.removeClass('active');
        songChartBtn.addClass('active');
    });
});
