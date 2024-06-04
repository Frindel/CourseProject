<template>
    <div class="module">
        <film-search></film-search>
        <charts-popup></charts-popup>
        <!-- <test></test> -->
    </div>
</template>
<script>
import filmSearch from './components/FilmSearch.vue'
import chartsPopUp from './components/ChartsPopUp.vue'
import test from './components/test.vue'

export default {
    components: {
        'film-search': filmSearch,
        'charts-popup': chartsPopUp,
        'test': test
    }
}
</script>

<style scoped>
.module {
    width: 100%;
    height: 100%;
    position: relative;
}</style>