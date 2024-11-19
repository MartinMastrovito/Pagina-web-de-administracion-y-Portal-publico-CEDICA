import { defineStore } from 'pinia'
import axios from 'axios'

export const useArticlesStore = defineStore('articlesStore', {
    state: ()=>({
        articles: [],
        loading: false,
        error: null,
    }),
    actions: {
        async fetchArticles( filters = {}){
            try {
                const urlApi = import.meta.env.VITE_ARTICLES_API
                this.loading = true
                this.error = null
                const queryParams = new URLSearchParams(filters).toString();
                const response = await axios.get(`${urlApi}?${queryParams}`)
                this.articles = response.data
            } 
            catch{
                this.error = 'Error al conseguir articulos'
            }
            finally{
                this.loading = false
            }
        },
    },
})