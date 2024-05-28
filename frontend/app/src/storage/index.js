import { defineStore } from "pinia";
import axios from "axios";

export const useMainStore = defineStore("mainStore", {
  state: () => ({
    apiUrl: "http://localhost:5000/api/v1/",
  }),

  getters: {},

  actions: {
    async userUid (state){
      let token = localStorage.getItem("uid");

      if (token != null) return token;

      // запрос токена
      token = await axios
        .get("http://localhost:5000/api/v1/authorization")
        .then((r) => r.data.token);

      // сохранение токена
      localStorage.setItem("uid", token);

      return token;
    },
    async modules (state) {
      // получение названий и описания модуей через api
      // await axios.get("http://localhost:5000/api/v1/modules").then(r=>console.log(data));

      return await axios
        .get("http://localhost:5000/api/v1/modules")
        .then((r) => r.data);
    },
    async dataSet (moduleName) {
      try {
        let a= this;
        const response = await axios({
          url: `http://localhost:5000/api/v1/${moduleName}/data-set`,
          method: 'GET',
          responseType: 'blob',
          headers: {
            key: await this.userUid(),
          },
        });

        return await response.data;
      } catch (error) {
        console.log(error);
        return null;
      }
    },
  },
});
