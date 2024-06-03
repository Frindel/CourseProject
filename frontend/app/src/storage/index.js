import { defineStore } from "pinia";
import axios from "axios";

export const useMainStore = defineStore("mainStore", {
  state: () => ({
    apiUrl: "http://localhost:5000/api/v1/",
  }),

  getters: {},

  actions: {
    async accessToken() {
      function parseJwt(token) {
        var base64Url = token.split(".")[1];
        var base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
        var jsonPayload = decodeURIComponent(
          window
            .atob(base64)
            .split("")
            .map(function (c) {
              return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
            })
            .join("")
        );

        return JSON.parse(jsonPayload);
      }

      function saveTokens(tokens) {
        localStorage.setItem("accessToken", tokens.accessToken);
        localStorage.setItem("refreshToken", tokens.refreshToken);
      }

      let accessToken = localStorage.getItem("accessToken");

      if (accessToken == null) {
        let tokens = await axios
          .get("http://localhost:5000/api/v1/register")
          .then((r) => r.data);
        saveTokens(tokens);
        return tokens.accessToken;
      }

      let liveTime = parseJwt(accessToken).iat;
      let now = Math.floor(Date.now() / 1000);

      // обновление токенов
      if (liveTime > now) {
        let newTokens = await axios
          .post(`http://localhost:5000/api/v1/update-access-token`, {
            refreshToken: localStorage.getItem("refreshToken"),
          })
          .then((r) => r.data);

        saveTokens(newTokens);
        return newTokens.accessToken;
      }

      return accessToken;
    },

    async modules(state) {
      return await axios
        .get("http://localhost:5000/api/v1/modules")
        .then((r) => r.data);
    },

    async dataSet(moduleName) {
      try {
        let token = await this.accessToken();
        let a =  `Bearer ${await this.accessToken()}`;
        const response = await axios({
          url: `http://localhost:5000/api/v1/simple/data-set`,
          method: "GET",
          "responseType": "blob",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        return await response.data;
      } catch (error) {
        console.log(error);
        return null;
      }
    },

    async retrain(moduleName, datasetFile, stepsHandler) {
      const webSocket = new WebSocket(`ws://localhost:5000/api/v1/${moduleName}/overfitting`);

      webSocket.onopen = async (event) => {
        // отправка access-токена
        webSocket.send(await this.accessToken());

        // отправка файла
        const reader = new FileReader();

        reader.onload = function (event){
          const arrayBuffer = event.target.result;
          webSocket.send(arrayBuffer);
        };

        reader.readAsArrayBuffer(datasetFile);
      };

      webSocket.onmessage = (event) => {
        let stepInfo = JSON.parse(event.data);
        stepsHandler(stepInfo);
      };

      webSocket.onclose = (event) => {
        console.log("close");
      };
    },
  },
});
