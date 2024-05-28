<template>
    <div class="model-item">
        <div class="model-item__header">
            <h2 v-on:click="open">{{ module.niceName }}</h2>
        </div>
        <div class="model-item__controls">
            <button v-on:click="displayInfo" class="model-control model-control_info"></button>
            <button v-on:click="displaySettings" class="model-control model-control_settings"></button>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        module: {
            type: Object,
            required: true
        }
    },
    emits: ['displayInfo', 'displaySettings', 'open'],
    methods: {
        displayInfo() {
            this.$emit('displayInfo', this.module);
        },
        displaySettings() {
            this.$emit('displaySettings', this.module);
        },
        open() {
            this.$emit('open', this.module.name);
        }
    }
}
</script>
<style scoped>
.model-item {
    display: flex;

    align-items: center;
    width: 100%;
    height: 50px;

    background-color: #fff0;
    padding: 2px 10px 2px 10px;

    transition-property: background-color;
    transition-duration: 0.3s;
    overflow: hidden;
}

.model-item:hover {
    background-color: #424040;
}

.model-item__header {
    max-width: 175px;
    overflow: hidden;
    white-space: nowrap;
    cursor: pointer;
}

.model-item__header>h2 {
    font-size: 1rem;
    font-family: sans-serif;
}

.model-item__controls {
    position: absolute;
    right: 0;

    display: flex;
    gap: 8px;
    align-items: center;
    justify-content: right;
    padding-right: 5px;
    margin-right: 5px;
}

.item__controls {
    display: flex;
}

.model-control {
    width: 25px;
    height: 25px;

    background-color: #FFF0;
    border-width: 0px;
    background-size: 80%;
    background-position: center;
    background-repeat: no-repeat;
    cursor: pointer;
    border-radius: 5px;
}

.model-control:hover {
    background-color: #2c2b2b;
}

.model-control_info {
    background-image: url(/icons/info-icon.svg);
}

.model-control_settings {
    background-image: url(/icons/settings-icon.svg);
}
</style>