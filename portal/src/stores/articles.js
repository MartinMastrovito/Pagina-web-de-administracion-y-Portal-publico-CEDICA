import { defineStore } from 'pinia'
import axios from 'axios'

export const useArticlesStore = defineStore('articlesStore', {
    state: ()=>({
        articles: [],
        pages: 0,
        loading: false,
        error: null,
    }),
    actions: {
        async fetchArticles( filters = {}){
            try {
                const urlApi = import.meta.env.VITE_ARTICLES_API
                const per_page = "per_page=4"
                this.loading = true
                this.error = null
                const queryParams = new URLSearchParams(filters).toString();
                const response = await axios.get(`${urlApi}?${queryParams}&${per_page}`)
                this.articles = response.data.articles
                this.pages = response.data.pages ?? 0
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