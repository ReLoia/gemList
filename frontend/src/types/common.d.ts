export export interface GameModel {
    id: string
    title: string
    image: string
    description: string
    external_links: {
        url: string
        img_url: string
    }[]
    likes: number
    // The local stats of the game - in the database - this depends on the users of the website
    stats: {
        ratings: number[],
    },
    // The global stats of the game - from the API
    meta: {
        platforms: string
        releaseYear: string
        genres: string
        developer: string
        publisher: string
    } | any
}

export type UserModel = {
    id: string;
    username: string;
    creation_date: string;
    // email: string;
    games_rated: Record<string, number>;
    games_liked: string[];
    games_played: string[];
};

export type AuthResponse = {
    access_token: string;
    token_type: string;
};
