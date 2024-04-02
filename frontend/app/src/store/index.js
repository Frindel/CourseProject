import { defineStore } from "pinia";
import axios from "axios";

export const useMainStore = defineStore('mainStore', {
    state: () => ({
        apiUrl: 'http://localhost:5000/api/v1/'
    }),

    getters: {

    },

    actions: {
        userUid: async (state) => {
            let token = localStorage.getItem('uid');

            if (token != null)
                return token;

            // запрос токена
            token = await axios.get("http://localhost:5000/api/v1/authorization").then(r=>r.data.token);

            // сохранение токена
            localStorage.setItem('uid', token)

            return token;
        },
        modules: async (state) => {
            // получение названий и описания модуей через api
            // await axios.get("http://localhost:5000/api/v1/modules").then(r=>console.log(data));
            
            return await axios.get("http://localhost:5000/api/v1/modules").then(r=>
            r.data);
        }
    }
})