import {defineStore} from 'pinia'
import {BackendApiService} from "../api/backend.ts";

export const useUserStore = defineStore('user', {
    state: () => {
        return {
            id: null,
            username: '',
            avatar: 'https://www.freeiconspng.com/uploads/am-a-19-year-old-multimedia-artist-student-from-manila--21.png',
            creation_date: '',
            games_rated: [],
            games_played: [],
            games_liked: [],
        }
    },
    actions: {
        setUser(userdata) {
            this.username = userdata.username;
            if (userdata.avatar) this.avatar = userdata.avatar;
            else this.avatar = "https://api.dicebear.com/9.x/pixel-art/svg?flip=true&backgroundType=gradientLinear,solid&randomizeIds=true&accessoriesProbability=25&beardProbability=20&clothingColor=00b159,03396c,428bca,44c585,5bc0de,88d8b0,ae0001,ffc425,ffd969,ffeead&glassesProbability=25&hatProbability=10&mouth=happy01,happy02,happy03,happy04,happy05,happy06,happy07,happy08,happy09,happy10,happy11,happy12,happy13,sad10&backgroundColor=b6e3f4,ffdfbf,aa001b,4a882a"
            this.creation_date = userdata.creation_date;
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
                // console.log(e)
                localStorage.removeItem('access_token');
            }
        }
    }

})
