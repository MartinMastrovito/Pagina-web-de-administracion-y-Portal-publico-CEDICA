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
                this.loading = true
                this.error = null
                const queryParams = new URLSearchParams(filters).toString();
                const response = await axios.get(`http://localhost:5000/api/articles?${queryParams}`)
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