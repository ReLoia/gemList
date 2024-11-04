import {fileURLToPath, URL} from 'node:url'

import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        vue({
            template: {
                compilerOptions: {
                    isCustomElement: tag => ["svg-icon", "left-menu", "divider"].includes(tag)
                }
            }
        })
    ],
    resolve: {
        alias: {
            '@': fileURLToPath(new URL('./src', import.meta.url))
        }
    },
    server: {
        host: true,
        base: process.env.ROOT_PATH || '/',
        proxy: {
            '/api': {
                // target: 'https://reloia.ddns.net/gemlist/api/',
                target: process.env.BACKEND_URL || 'http://localhost:8000/',
                changeOrigin: true,
                rewrite: path => path.replace(/^\/api/, '')
            }
        }
    }
})
