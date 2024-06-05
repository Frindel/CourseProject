<template>
    <div class="module">
        <film-search></film-search>
        <charts-popupe></charts-popupe>
    </div>
</template>
<script>

import chartsPopUp from './components/ChartsPopUp.vue';
import filmSearch from './components/FilmSearch.vue';

export default {
    components: {
        'charts-popupe': chartsPopUp,
        'film-search': filmSearch,
    }
}
</script>

<style scoped>
.module {
    width: 100%;
    height: 100%;
    position: relative;

    overflow: auto;
}</style>