<template>
    <div class="list">
        <model-item v-for="module in modules" v-bind:module="module" v-on:displayInfo="displayModuleInfo"
            v-on:displaySettings="displayModelSettings" v-on:open="openModule"></model-item>
    </div>
    <model-info-pop-up v-bind:module="moduleInfoPopUp" v-bind:isVisible="isVisubleinfoPopUp"
        v-on:close="closeModuleInfo"></model-info-pop-up>
    <model-settings-pop-up v-bind:module="moduleSettingsPopUp" v-bind:isVisible="isVisibleModuleSettingsPopUp"
        v-on:close="closeModuleSettings" v-on:loadDataSet="loadDataSet" v-on:retrain="retrain"></model-settings-pop-up>
    <retrain-pop-up v-bind:isVisible="isVisibleRetrainPopUp" v-bind:stepInfo="retrainStepInfo"></retrain-pop-up>
</template>
<script>
import { useMainStore } from '../storage'

import ModelItem from './ModelItem.vue';
import ModelInfoPopUp from './ModelInfoPopUp.vue';
import ModelSettingsPopUp from './ModelSettingsPopUp.vue';
import RetrainPopUp from './RetrainPopUp.vue';

export default {
    components: {
        'model-item': ModelItem,
        'model-info-pop-up': ModelInfoPopUp,
        'model-settings-pop-up': ModelSettingsPopUp,
        'retrain-pop-up': RetrainPopUp
    },

    data() {
        return {
            mainStorage: useMainStore(),
            modules: [],

            moduleInfoPopUp: null,
            isVisubleinfoPopUp: false,

            moduleSettingsPopUp: null,
            isVisibleModuleSettingsPopUp: false,

            isVisibleRetrainPopUp: false,
            retrainStepInfo: null,

            selectedModule: undefined,
        }
    },
    methods: {
        displayModuleInfo(module) {
            this.moduleInfoPopUp = module;
            this.isVisubleinfoPopUp = true;
        },
        closeModuleInfo() {
            this.moduleInfoPupUp = null;
            this.isVisubleinfoPopUp = false;
        },
        displayModelSettings(module) {
            this.moduleSettingsPopUp = module;
            this.isVisibleModuleSettingsPopUp = true;
        },
        closeModuleSettings() {
            this.moduleSettingsPopUp = null;
            this.isVisibleModuleSettingsPopUp = false;
            this.isVisibleRetrainPopUp = false;
        },
        openModule(moduleName) {
            this.$router.push(`/${moduleName}`);
        },
        async loadDataSet() {
            let file = await this.mainStorage.dataSet(this.moduleSettingsPopUp.name);

            const href = URL.createObjectURL(file);
            const link = document.createElement('a');
            link.href = href;

            link.setAttribute('download', `${this.moduleSettingsPopUp.name} dataset.csv`);
            document.body.appendChild(link);
            link.click();

            document.body.removeChild(link);
            URL.revokeObjectURL(href);
        },
        async retrain() {
            // выбор пользователем файла датасета
            const input = document.createElement('input');
            input.type = 'file';
            input.accept = '.csv';

            await new Promise((resolve) => {
                input.addEventListener('change', resolve, { once: true });
                input.click();
            });

            let selectedFile = input.files[0];
            // console.log(selectedFile)

            this.isVisibleRetrainPopUp = true;

            let moduleName = this.moduleSettingsPopUp.name;

            await this.mainStorage.retrain(moduleName, selectedFile, stepInfo => {
                console.log(stepInfo);
                switch (stepInfo.stage) {
                    case 'geting token':
                        this.retrainStepInfo = 'Идентификация пользователя';
                        return;
                    case 'etting dataset':
                        this.retrainStepInfo = 'Получение датасета';
                        return;
                    case 'save dataset':
                        this.retrainStepInfo = 'Сохранение датасета';
                        setTimeout(()=>this.isVisibleRetrainPopUp = false, 5000)
                        return;
                }

                // if (stepInfo.stage == 'save dataset')
                //     this.isVisibleRetrainPopUp = false;
            });
        }
    },
    async mounted() {
        // загрузка информации о модулях
        this.modules = await this.mainStorage.modules();
    },
}
</script>
<style scoped>
.list {
    display: flex;

    width: 100%;
    height: 100%;

    flex-direction: column;
    gap: 4px;

    overflow-y: auto;
    overflow-x: hidden;
}
</style>