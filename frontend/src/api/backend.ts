import type {AuthResponse, GameModel, UserModel} from "../types/common";

let ENV_BASE_URL: string = import.meta.env.BASE_URL;
if (ENV_BASE_URL.endsWith("/"))
    ENV_BASE_URL = ENV_BASE_URL.slice(0, -1);

export class APIError extends Error {
    constructor(message: string) {
        super(message);
        this.name = "APIError";
    }
}


export class BackendApiService {
    private baseUrl: string = ENV_BASE_URL + "/api"
    private token: string | null;

    constructor() {
        this.token = null;
    }

    // Set the token for authenticated requests
    setToken(token: string) {
        this.token = token;
    }

    // Helper method to handle the headers
    private getHeaders(authenticated: boolean = false, formData: boolean = false): HeadersInit {
        const headers: HeadersInit = {
            "Content-Type": formData ? "application/x-www-form-urlencoded" : "application/json",
            // Skip the browser warning for ngrok
            "ngrok-skip-browser-warning": "true",
        };
        if (authenticated && this.token) {
            headers["Authorization"] = `Bearer ${this.token}`;
        }
        return headers;
    }

    // GET /games
    async getGames(sort: string = "recent"): Promise<GameModel[]> {
        const response = await fetch(`${this.baseUrl}/games?sort=${sort}`, {
            headers: this.getHeaders(),
        });
        if (!response.ok) {
            throw new Error("Failed to fetch games");
        }
        return response.json();
    }


    // POST /games/get
    async getGamesFromIds(ids: string[]): Promise<GameModel[]> {
        const response = await fetch(`${this.baseUrl}/games/get`, {
            method: "POST",
            headers: this.getHeaders(),
            body: JSON.stringify(ids),
        });
        if (!response.ok) {
            throw new Error("Failed to fetch games");
        }
        return response.json();
    }

    // GET /games/{game_id}
    async getGame(gameId: string): Promise<GameModel> {
        const response = await fetch(`${this.baseUrl}/games/${gameId}`, {
            headers: this.getHeaders(),
        });
        if (!response.ok) {
            throw new Error("Failed to fetch the game");
        }
        return response.json();
    }

    // POST /games/{game_id}/rate
    async rateGame(gameId: string, rating: number): Promise<{ message: string }> {
        const response = await fetch(`${this.baseUrl}/games/${gameId}/rate`, {
            method: "POST",
            headers: this.getHeaders(true),
            body: JSON.stringify({rating}),
        });
        if (!response.ok) {
            throw new Error("Failed to rate the game");
        }
        return response.json();
    }

    // POST /games/{game_id}/like
    async likeGame(gameId: string): Promise<{ message: string }> {
        const response = await fetch(`${this.baseUrl}/games/${gameId}/like`, {
            method: "POST",
            headers: this.getHeaders(true),
        });
        if (!response.ok) {
            throw new Error("Failed to like the game");
        }
        return response.json();
    }

    // POST /login
    async login(username: string, password: string): Promise<AuthResponse> {
        const response = await fetch(`${this.baseUrl}/login`, {
            method: "POST",
            headers: this.getHeaders(false, true),
            body: `username=${username}&password=${password}`,
        });
        if (!response.ok) {
            let data: any;
            try {
                data = await response.json();
            } catch (e) {
                throw new Error("Login failed");
            }
            throw new APIError(data.detail);
        }
        const data = await response.json();
        this.setToken(data.access_token);
        return data;
    }

    // POST /register
    async register(username: string, password: string): Promise<AuthResponse> {
        const response = await fetch(`${this.baseUrl}/register`, {
            method: "POST",
            headers: this.getHeaders(false, true),
            body: `username=${username}&password=${password}`,
        });
        if (!response.ok) {
            let data: any;
            try {
                data = await response.json();
            } catch (e) {
                throw new Error("Registration failed");
            }
            throw new APIError(data.detail);
        }
        const data = await response.json();
        this.setToken(data.access_token);
        return data;
    }

    // GET /users/me
    async getUser(): Promise<UserModel> {
        const response = await fetch(`${this.baseUrl}/users/me`, {
            headers: this.getHeaders(true),
        });
        if (!response.ok) {
            throw new Error("Failed to fetch user data");
        }
        return response.json();
    }
}
