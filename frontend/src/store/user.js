import {defineStore} from 'pinia'
import {BackendApiService} from "../api/backend.ts";

export const useUserStore = defineStore('user', {
    state: () => {
        return {
            id: null,
            username: '',
            avatar: 'https://api.dicebear.com/9.x/adventurer/png?backgroundColor=b6e3f4,c0aede,d1d4f9',
            games_rated: [],
            games_played: [],
            games_liked: [],
        }
    },
    actions: {
        setUser(userdata) {
            this.username = userdata.username;
            if (userdata.avatar) this.avatar = userdata.avatar;
            this.games_rated = userdata.games_rated;
            this.games_played = userdata.games_played;
            this.games_liked = userdata.games_liked;
        },
        async loadUser(token) {
            if (!token) return;
            localStorage.setItem('access_token', token);
            const api = new BackendApiService();
            api.setToken(token);

            let user;
            try {
                user = await api.getUser();
                this.setUser(user);
            } catch (e) {
                console.log(e)
            }
        }
    }

})
