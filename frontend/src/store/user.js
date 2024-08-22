import {defineStore} from 'pinia'

export const useUserStore = defineStore('user', {
    state: () => {
        return {
            username: '',
            avatar: ''
        }
    },
    actions: {
        setUser(userdata) {
            this.username = userdata.username;
            this.avatar = userdata.avatar;
        }
    }

})
