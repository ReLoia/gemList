import {defineConfig} from 'vite'
import vue from '@vitejs/plugin-vue'

// add /api redirect to backend

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
            '@': '/src'
        }
    },
    server: {
        base: process.env.ROOT_PATH || '/',
        proxy: {
            '/api': {
                target: 'https://vercel-proxy-alpha-three.vercel.app/gemlist/api/',
                changeOrigin: true,
                rewrite: path => path.replace(/^\/api/, '')
            }
        }
    }
})
