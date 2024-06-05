<template>
    <button class="charts-pup-up__display-button" type="button" @click="modalOpen = true">
    </button>

    <teleport to="body">
        <div v-if="modalOpen" class="charts-pup-up">
            <div class="charts-pop-up__container">
                <div class="charts-pop-up__charts">
                    <div class="chart">
                        <div class="chart__header">
                            <h3>Год выпуска/ количество</h3>
                        </div>
                        <div class="chart__view">
                            <Bar id="my-chart-id" :options="firstChart.chartOptions" :data="firstChart.chartData" />
                        </div>
                    </div>
                    <div class="chart">
                        <div class="chart__header">
                            <h3>Цена / количество</h3>
                        </div>
                        <div class="chart__view">
                            <Line class="chart__chart" id="my-chart-id" :options="secondChart.chartOptions"
                                :data="secondChart.chartData" />
                        </div>
                    </div>
                </div>
            </div>
            <div class="charts-pup-up__substrate" v-on:click="modalOpen = false"></div>
        </div>
    </teleport>
</template>

<script>
import { useRecomendedPhoneStore } from '../storage'

import { Line, Bar } from 'vue-chartjs'
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale } from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale)

export default {
    name: 'charts-popupe',
    components: {
        Line,
        Bar
    },
    data() {
        return {
            moduleStorage: useRecomendedPhoneStore(),

            modalOpen: false,

            firstChart: {
                chartData: {
                    labels: ['January', 'February', 'March'],
                    datasets: [{
                        data: [40, 20, 12],
                        label: 'Год выпуска/ количество',
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
                        label: 'Цена / количество',
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
                                text: 'Цена'
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
        let genreStatistics = await this.moduleStorage.getCountStatistics();

        let genresAndCount = splitStatistics(genreStatistics, 'Release', 'Count');

        this.firstChart.chartData.labels = genresAndCount.Release;
        this.firstChart.chartData.datasets[0].data = genresAndCount.Count;

        // статистика по датам резила
        let releaseDatesStatistics = await this.moduleStorage.getPriceStatistics();

        let releaseDates = splitStatistics(releaseDatesStatistics, 'Диапазон цен', 'Количество моделей');

        this.secondChart.chartData.labels = releaseDates['Диапазон цен'];
        this.secondChart.chartData.datasets[0].data = releaseDates['Количество моделей'];
    },
}
</script>

<style>
.charts-pup-up__display-button {
    position: fixed;
    bottom: 20px;
    right: 30px;
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
