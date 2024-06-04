<template>
    <div class="search-result">
        <div class="search-result__request">
            <p>{{ request }}</p>
        </div>
        <div class="search-result__films">
            <film-info v-for="film in films" v-bind:film="film"></film-info>
        </div>
    </div>
</template>
<script>
import FilmInfo from './FilmInfo.vue';
import filmInfo from './FilmInfo.vue'

export default {
    components: {
        'film-info': filmInfo
    },
    props: ['request','films']
}
</script>
<style>
.search-result {
    width: 100%;

    padding: 0 10px;
    padding-bottom: 10px;
    background-color: #EEE;
    color: #000;
    
    font-family: Geneva, Verdana, sans-serif;
    font-size: 18px;
    /* font-weight: 600; */

    box-shadow: 1px 0 8px rgba(0, 0, 0, 0.3);
    border-radius: 3px;
    
}


.search-result__films{
    display: flex;
    flex-direction: column;
    gap: 10px;
}
</style>