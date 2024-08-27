export interface GameModel {
    id: string
    title: string
    image: string
    description: string
    externalLinks: {
        url: string
        img_url: string
    }[]
    // The local stats of the game - in the database - this depends on the users of the website
    stats: {
        likes: number
        ratings: number[]
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