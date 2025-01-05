export type GameModel = {
    id: string
    title: string
    description: string
    cover_image_url: string
    release_year: number
    external_links: {
        url: string
        img_url: string
    }[]
    genres: string[]
    developer: string
    publisher: string
    platforms: string[]
    rating_esrb: string
    trailer_url: string
    likes: number
    // len 10 array of times for each rating from 1 to 10
    ratings: number[]
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
