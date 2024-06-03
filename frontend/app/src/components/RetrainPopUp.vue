<template>
    <teleport to='body'>
        <div v-if="isVisible" class="pop-up">
            <div class="pop-up__container">
                <div class="pop-up__message">
                    <p>{{ stepInfo }}</p>
                </div>
            </div>
            <!-- <div v-on:click="close" class="pop-up__substrate"></div> -->
        </div>
    </teleport>
</template>
<script>
export default {
    props: {
        stepInfo: {
            type: String,
            required: true
        },
        isVisible: {
            type: Boolean,
            required: true,
            default: false
        }
    }
}
</script>
<style scoped>
.pop-up{
    position: fixed;
    width: 100vw;
    /* height: 100vh; */
    z-index: 100;
    top: 0;
    left: 0;

    display: flex;
    justify-content: center;
}

.pop-up__container {
    position: relative;
    z-index: 0;

    width: 500px;
    height: 80px;

    background-color: #FFF;
    padding: 15px;
    margin: 20px;
}

.pop-up__substrate {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0);
    z-index: -1;
}

.pop-up__message{
    text-align: center;
    font-size: 18px;
}
</style>