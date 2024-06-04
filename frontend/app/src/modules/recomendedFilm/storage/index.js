import { defineStore } from "pinia";
import axios from "axios";
import { useMainStore } from "../../../storage";

export const useRecomendedFilmStore = defineStore("recomendedFilmStore", {
  state: () => ({
    apiUrl: "http://localhost:5000/api/v1/",
  }),

  getters: {},

  actions: {
    async films(description) {
      let token = await useMainStore().accessToken();

      return await axios({
        url: `http://localhost:5000/api/v1/recomended-film/search`,
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        params: {
          description: description,
        },
      }).then((r) => r.data);
    },
    async getGenreStatistics() {
      let token = await useMainStore().accessToken();

      return await axios({
        url: `http://localhost:5000/api/v1/recomended-film/genre-statistics`,
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`
        }
      }).then((r) => r.data);
    },

    async getReleaseDatesStatistics() {
      let token = await useMainStore().accessToken();

      return await axios({
        url: `http://localhost:5000/api/v1/recomended-film/releaseDate-statistics`,
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`
        }
      }).then((r) => r.data);
    },

    async getRatingStatistics() {
      let token = await useMainStore().accessToken();

      return await axios({
        url: `http://localhost:5000/api/v1/recomended-film/reiting-statistics`,
        method: "GET",
        headers: {
          Authorization: `Bearer ${token}`
        }
      }).then((r) => r.data);
    },
  },
});
