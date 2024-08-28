import {defineStore} from 'pinia'

export const useUserStore = defineStore('user', {
    state: () => {
        return {
            username: '',
            avatar: 'https://api.dicebear.com/9.x/adventurer/png?backgroundColor=b6e3f4,c0aede,d1d4f9',
            token: ''
        }
    },
    actions: {
        setUser(userdata) {
            this.username = userdata.username;
            this.avatar = userdata.avatar;
        }
    }

})
