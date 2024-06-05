import { defineStore } from "pinia";
import axios from "axios";
import { useMainStore } from "../../../storage";

export const useRecomendedPhoneStore = defineStore("recomendedPhoneStore", {
  state: () => ({
    apiUrl: "http://localhost:5000/api/v1/",
  }),

  getters: {},

  actions: {
    async phones(request) {
      let token = await useMainStore().accessToken();

      return await axios({
        url: `http://localhost:5000/api/v1/recomended-phone/search`,
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: {
          osClass: request.os,
          priceRange: request.price,
          batteryCapacity: request.batteryCapacity,
          operativeMemory: request.operativeMemory,
          internalMemory: request.internalMemory,
        },
      }).then((r) => r.data);
    },
    async getCountStatistics() {
      let token = await useMainStore().accessToken();

      return await axios({
        url: `http://localhost:5000/api/v1/recomended-phone/years-statistics`,
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`
        }
      }).then((r) => r.data);
    },

    async getPriceStatistics() {
      let token = await useMainStore().accessToken();

      return await axios({
        url: `http://localhost:5000/api/v1/recomended-phone/price-statistics`,
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`
        }
      }).then((r) => r.data);
    }
  },
});
