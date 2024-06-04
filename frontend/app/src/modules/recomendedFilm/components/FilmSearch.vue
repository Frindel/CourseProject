<template>
    <div class="film-search">
        <div class="film-search__content">
            <div class="film-search__results">
                <search-result v-for="searchResult in searchResults"
                v-bind:films="searchResult.films"
                v-bind:request="searchResult.request"></search-result>
            </div>
            <div class="film-search__controls">
                <input v-model="description" class="film-search__input" type="text" name="" id=""
                    placeholder="Описание фильма"
                    v-on:keyup.enter="searchFilms">
                <button v-on:click="searchFilms" type="button" class="film-search__search-button">

                </button>
            </div>
        </div>
    </div>
</template>
<script>
import searchResult from './SearchResult.vue';
import { useRecomendedFilmStore } from '../storage/index.js';

export default {
    components: {
        'search-result': searchResult
    },
    data() {
        return {
            moduleStorage: useRecomendedFilmStore(),
            description: undefined,
            searchResults: []
        }
    },
    methods: {
        async searchFilms() {
            if (this.description == undefined)
                return;
            let description = this.description;
            this.description = undefined;

            let searchResult = await this.moduleStorage.films(description);

            this.searchResults.push({ request: description, films: searchResult });

        }
    }
};
</script>

<style scoped>
.film-search {
    width: 100%;
    height: 100%;
    display: flex;
    justify-content: center;
}

.film-search__content {
    position: relative;
    margin: 20px;
    width: 550px;

    padding-bottom: 60px;
}

.film-search__results {
    width: 100%;
    height: 100%;
    margin-bottom: 30px;
    /* background-color: #BBB; */
    display: flex;
    flex-direction: column;

    overflow-y: auto;
    gap: 17px
}

.film-search__controls {
    display: flex;
    position: absolute;

    bottom: 0;
    left: 0;

    overflow: hidden;

    width: 100%;
    height: 35px;

    margin-bottom: 10px;

    background-color: #FFF;
    border-radius: 5px;
    border: #FFF solid 1px;

    transition-property: border;
    transition-duration: 0.3s;
    box-shadow: 0px 1px 2px rgba(0, 0, 0, 0.6)
}

.film-search__controls:hover {
    border: #CCC solid 1px
}


.film-search__input {
    border-width: 0;
    background-color: #FFF;
    height: 100%;
    width: 100%;
    font-size: 20px;
    margin: 0 5px;
    margin-right: 35px
}

.film-search__input:focus {
    outline: none
}

.film-search__search-button {
    position: absolute;

    top: 0;
    right: 0;

    width: 35px;
    height: 35px;

    border-width: 0;

    background-color: #FFF0;
    background-size: 60%;
    background-position: center;
    background-repeat: no-repeat;
    background-image: url('/icons/modules/recomnded-film/search-icon.svg');
}

.film-search__search-button:hover {
    background-color: #EEE;
}
</style>