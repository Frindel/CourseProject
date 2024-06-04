<template>
    <button class="charts-pup-up__display-button" type="button" @click="modalOpen = true">
    </button>

    <teleport to="body">
        <div v-if="modalOpen" class="charts-pup-up">
            <div class="charts-pop-up__container">
                <div class="charts-pop-up__charts">
                    <div class="chart">
                        <div class="chart__header">
                            <h3>Жанры/количество</h3>
                        </div>
                        <div class="chart__view">
                            <Bar id="my-chart-id" :options="firstChart.chartOptions" :data="firstChart.chartData" />
                        </div>
                    </div>
                    <div class="chart">
                        <div class="chart__header">
                            <h3>Даты выпуска/количества</h3>
                        </div>
                        <div class="chart__view">
                            <Line class="chart__chart" id="my-chart-id" :options="secondChart.chartOptions"
                                :data="secondChart.chartData" />
                        </div>
                    </div>
                    <div class="chart">
                        <div class="chart__header">
                            <h3>Рейтинг фильма/количество</h3>
                        </div>
                        <div class="chart__view">
                            <Line id="my-chart-id" :options="thirdChart.chartOptions" :data="thirdChart.chartData" />
                        </div>
                    </div>
                </div>
            </div>
            <div class="charts-pup-up__substrate" v-on:click="modalOpen = false"></div>
        </div>
    </teleport>
</template>

<script>
import { useRecomendedFilmStore } from '../storage'

import { Line, Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)

export default {
    components: {
        Line,
        Bar
    },
    data() {
        return {
            moduleStorage: useRecomendedFilmStore(),

            modalOpen: false,

            firstChart: {
                chartData: {
                    labels: ['January', 'February', 'March'],
                    datasets: [{
                        data: [40, 20, 12],
                        label: 'Жанры/количество',
                        borderColor: '#42A5F5',
                        backgroundColor: 'rgba(66, 165, 245, 0.2)'
                    }]
                },
                chartOptions: {
                    responsive: true
                }
            },

            secondChart: {
                chartData: {
                    labels: ['January', 'February', 'March'],
                    datasets: [{
                        data: [40, 20, 12],
                        label: 'даты выпуска/количество',
                        borderColor: '#42A5F5',
                        backgroundColor: 'rgba(66, 165, 245, 0.2)'
                    }]
                },
                chartOptions: {
                    responsive: true,
                    scales: {
                        x: {
                            display: true,
                            title: {
                                display: true,
                                text: 'количество'
                            }
                        },
                        y: {
                            display: true,
                            title: {
                                display: true,
                                text: 'год выпуска'
                            }
                        }
                    }
                }
            },

            thirdChart: {
                chartData: {
                    labels: [],
                    datasets: [{
                        data: [],
                        label: 'Рейтинг/количество',
                        borderColor: '#42A5F5',
                        backgroundColor: 'rgba(66, 165, 245, 0.2)'
                    }]
                },
                chartOptions: {
                    responsive: true,
                    scales: {
                        x: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Рейтинг'
                            }
                        },
                        y: {
                            display: true,
                            title: {
                                display: true,
                                text: 'Количество'
                            }
                        }
                    }
                }
            }
        }
    },
    async mounted() {
        function splitStatistics(values, firstHeader, secondHeader) {
            let first = [];
            let second = [];
            values.forEach(v => {
                first.push(v[firstHeader]);
                second.push(v[secondHeader]);
            }
            );

            let res ={};
            res[firstHeader] = first;
            res[secondHeader] = second;
            return res;
        };

        // статистика по жанрам
        let genreStatistics = await this.moduleStorage.getGenreStatistics();

        let genresAndCount = splitStatistics(genreStatistics, 'genre', 'count');

        this.firstChart.chartData.labels = genresAndCount.genre;
        this.firstChart.chartData.datasets[0].data = genresAndCount.count;

        // статистика по датам резила
        let releaseDatesStatistics = await this.moduleStorage.getReleaseDatesStatistics();

        let releaseDates = splitStatistics(releaseDatesStatistics, 'year', 'count');

        this.secondChart.chartData.labels = releaseDates.year;
        this.secondChart.chartData.datasets[0].data = releaseDates.count;

        // рейтинг фильма / количество
        let ratingStatistics = await this.moduleStorage.getRatingStatistics();

        let ratings = splitStatistics(ratingStatistics, 'reiting', 'count');

        this.thirdChart.chartData.labels = ratings.reiting;
        this.thirdChart.chartData.datasets[0].data = ratings.count;
    },
}
</script>

<style>
.charts-pup-up__display-button {
    position: absolute;
    bottom: 10px;
    right: 10px;
    width: 45px;
    height: 45px;
    border-radius: 5px;
    background-color: #302d2d;
    background-image: url('/icons/modules/recomnded-film/chart-icon.svg');
    background-position: center;
    background-size: 80%;
    background-repeat: no-repeat;
}

.charts-pup-up__display-button:hover {
    background-color: #424040;
}

.charts-pup-up {
    position: fixed;
    width: 100vw;
    height: 100vh;
    z-index: 100;
    top: 0;
    left: 0;
    display: flex;
    align-items: center;
    justify-content: center;
}

.charts-pop-up__container {
    position: relative;
    z-index: 0;
    width: 1200px;
    height: 700px;
    background-color: #FFF;
    padding: 15px;
    margin: 20px;
}

.charts-pup-up__substrate {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: -1;
}

.charts-pop-up__charts {
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
    overflow-y: scroll;
}

.chart {
    display: flex;
    align-items: center;
    flex-direction: column;
    position: relative;
    height: 500px;
}

.chart__view {
    display: flex;
    justify-content: center;
    width: 100%;
    height: 100%;
    overflow: hidden;
}

.chart__chart {
    width: 100%;
    height: 100%;
}
</style>
