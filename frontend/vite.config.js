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
        proxy: {
            '/api': {
                // TODO: change to backend url
                target: 'http://localhost:8000',
                changeOrigin: true,
                rewrite: path => path.replace(/^\/api/, '')
            }
        }
    }
})
