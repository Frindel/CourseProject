<template>
    <div class="sidebar-container">

        <div class="sidebar" v-bind:class="[isHidden ? 'sidebar_hidden' : '']">
            <div class="sidebar__content">
                <div class="sidebar__header">
                    <h1>Модели</h1>
                </div>
                <div class="sidebar__models-list">
                    <models-list></models-list>
                </div>
                <div class="sidebar__controls">
                    <!-- кнопки -->
                </div>

            </div>
            <button class="roll-up-button" v-on:click="hiddenSidebar"></button>
        </div>
        <div class="display-button" v-if="isHidden" v-on:click="displaySidebar"></div>
    </div>
</template>
<script>
import ModelsList from './ModelsList.vue'

export default {
    components: {
        'models-list': ModelsList
    },
    data() {
        return {
            isHidden: false
        }
    },
    methods: {
        displaySidebar() {
            this.isHidden = false;
        },
        hiddenSidebar() {
            this.isHidden = true;
        }
    }
}
</script>
<style scoped>
.sidebar-container {
    display: flex;
    position: relative;

    height: 100%;
    width: auto;
    overflow-x: visible;
}

.sidebar {
    display: flex;

    height: 100%;
    min-width: 270px;
    width: 270px;
    position: relative;

    background-color: #302d2d;
    color: #FFF;

    transition-property: min-width, width;
    transition-duration: 0.3s;
    overflow: hidden;
}

.sidebar__header {
    margin: 0 10px;
}

.sidebar__header>h1 {
    font-size: 20px;
    font-weight: 700;
    font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif
}

.sidebar_hidden {
    min-width: 0;
    width: 0;
}

.sidebar__content {
    position: relative;
    display: flex;

    height: 100%;
    width: 100%;

    margin: 10px 0;
    flex-direction: column;
}

.sidebar__models-list {
    height: 100%;
    margin-bottom: 70px;
    /* background-color: green; */
}

.sidebar__controls {
    position: absolute;
    bottom: 0;

    height: 40px;
    width: 100%;

    transform: translate(0, -20px);
    /* background-color: red; */
}

.display-button {
    position: absolute;
    right: 0;
    top: 0;

    height: 100%;
    width: 20px;

    transform: translate(100%, 0);
    z-index: 100;

    background-image: linear-gradient(left, #443f3f, rgba(68, 63, 63, 0));
    background-image: -o-linear-gradient(left, #302d2d, rgba(68, 63, 63, 0));
    background-image: -moz-linear-gradient(left, #302d2d, rgba(68, 63, 63, 0));
    background-image: -webkit-linear-gradient(left, #302d2d, rgba(68, 63, 63, 0));
    opacity: 0;

    transition-property: opacity;
    transition-duration: 0.7s;
}

.display-button:hover {
    opacity: 1;
    cursor: pointer;
}

.roll-up-button {
    position: absolute;
    top: 2px;
    right: 2px;

    width: 40px;
    height: 40px;

    background-color: #fff0;
    background-size: 30%;
    background-position: center;
    background-repeat: no-repeat;
    background-image: url('/icons/roll-up-icon.svg');

    border-width: 0px;
    border-radius: 5px;
}

.roll-up-button:hover {
    background-color: #424040;
}
</style>