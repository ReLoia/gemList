export interface GameModel {
    id: string
    title: string
    image: string
    description: string
    externalLinks: {
        url: string
        img_url: string
    }[]
    stats: {
        likes: number
        ratings: number[]
    },
    meta: any
}