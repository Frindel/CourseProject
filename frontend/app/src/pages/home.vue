<template>
    <div class="services">
        <div class="services__servise" v-for="module in modules">
            <div class="service__header">
                <h3>{{ module.niceName }}</h3>
            </div>
            <div class="service__description">
                {{ module.description }}
            </div>
                <router-link v-bind:to="'/' + module.name">Открыть</router-link>
            
        </div>
    </div>
</template>
<script>
import {
    useMainStore
} from "../store"

export default {
    data() {
        return {
            store: useMainStore(),
            modules: null
        };
    },

    methods: {

    },

    async mounted() {
        this.modules = await this.store.modules();
    }
}
</script>