import {fileURLToPath, URL} from 'node:url'

import {defineConfig, loadEnv} from 'vite'
import vue from '@vitejs/plugin-vue'
import vueDevTools from 'vite-plugin-vue-devtools'

function isTruthy(value?: string): boolean {
  if (!value) {
    return false
  }

  return ['1', 'true', 'yes', 'on'].includes(value.toLowerCase())
}

function parseNumber(value?: string): number | undefined {
  if (!value) {
    return undefined
  }

  const parsed = Number(value)
  return Number.isFinite(parsed) ? parsed : undefined
}

// https://vite.dev/config/
export default defineConfig(({mode}) => {
  const env = loadEnv(mode, process.cwd(), 'VITE__')
  const port = Number(env.VITE__PORT) || 5173
  const domain = env.VITE__DOMAIN || 'domainex.dev'
  const hmrProtocol = env.VITE__HMR_PROTOCOL as 'ws' | 'wss' | undefined
  const hmrHost = env.VITE__HMR_HOST || domain
  const hmrClientPort = parseNumber(env.VITE__HMR_CLIENT_PORT)
  const hmrPort = parseNumber(env.VITE__HMR_PORT)
  const watchUsePolling = isTruthy(env.VITE__WATCH_USE_POLLING)
  const watchInterval = parseNumber(env.VITE__WATCH_INTERVAL) || 150

  return {
    plugins: [vue(), vueDevTools()],
    resolve: {
      extensions: ['.ts', '.js', '.vue', '.json'],
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url)),
      },
    },
    server: {
      host: '0.0.0.0',
      port,
      allowedHosts: [domain],
      hmr: {
        protocol: hmrProtocol,
        host: hmrHost,
        clientPort: hmrClientPort,
        port: hmrPort,
      },
      watch: watchUsePolling
        ? {
            usePolling: true,
            interval: watchInterval,
          }
        : undefined,
    },
  }
})
