<template>
    <div class="main-container">
        <side-bar></side-bar>
        <div class="content-container">
            <router-view></router-view>
        </div>
    </div>
</template>

<script>
import SideBar from './components/SideBar.vue';
import ModelSettings from './components/ModelSettingsPopUp.vue';

export default {
    components: {
        'side-bar': SideBar,
        'model-settings': ModelSettings
    }
}

</script>

<style>
.main-container {
    display: flex;
    
    width: 100%;
    height: 100vh;
}

.content-container {

    width: 100%;
    height: 100%;

    /* background-color: #383535; */
    
    background-color: #CCC;
}
</style>
