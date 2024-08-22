import {defineStore} from 'pinia'

export const useHeaderStore = defineStore('header', {
    state: () => {
        return {
            expanded: true,
            backgroundImage: '',
            title: '',
            description: '',
            type: ''
        }
    },

})
