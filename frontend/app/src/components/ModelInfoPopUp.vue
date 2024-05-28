<template>
    <teleport to='body'>
        <div v-if="isVisible" class="pop-up">
            <div class="pop-up__container">
                <div class="pop-up__header">
                    <h2>{{ module.niceName }}</h2>
                </div>
                <div class="pop-up__content">
                    <p>{{ module.description }}</p>
                </div>
                <button v-on:click="close" class="close-button"></button>
            </div>
            <div  v-on:click="close"  class="pop-up__substrate"></div>
        </div>
    </teleport>
</template>
<script>
export default {
    props: {
        module: {
            type: [Object, null],
            required: true
        },
        isVisible: {
            type: Boolean,
            required: true,
            default: false
        }
    },
    emits: ['close'],
    methods: {
        close() {
            this.$emit('close');
        }
    }
}
</script>
<style scoped>
.pop-up {
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

.pop-up__container{
    position: relative;
    z-index: 0;

    width: 600px;
    height: 400px;

    background-color: #FFF;
    padding: 15px;
    margin: 20px;
}

.pop-up__substrate{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    z-index: -1;
}

.pop-up__header > h2 {
    font-size: 24px;
    font-weight: 700;
    margin-top: 27px;
    font-family:system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, 'Open Sans', 'Helvetica Neue', sans-serif
}

.pop-up__content {
    font-size: 18px;
    font-family: Geneva, Verdana, sans-serif;
}

.close-button{
    position: absolute;
    top: 2px;
    right: 2px;

    width: 40px;
    height: 40px;

    background-color: #fff0;
    background-size: 80%;
    background-position: center;
    background-repeat: no-repeat;
    background-image: url('/icons/close-icon.svg');

    border-width: 0px;
    border-radius: 5px;
}

.close-button:hover{
    
    background-color: #E2E0E0;
}
</style>