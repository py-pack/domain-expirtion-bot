type RawEnv = {
  VITE__API_BASE_URL: string
  VITE__GOOGLE_CLIENT_ID: string
  VITE__GOOGLE_REDIRECT_URI: string
}

function getEnv<K extends keyof RawEnv>(key: K): RawEnv[K] {
  const value = import.meta.env[key]
  if (!value) {
    throw new Error(`❌ Env variable "${key}" is not defined`)
  }
  return value
}

export const env = {
  api: {
    baseUrl: getEnv('VITE__API_BASE_URL'),
  },
  google: {
    clientId: getEnv('VITE__GOOGLE_CLIENT_ID'),
    redirectUri: getEnv('VITE__GOOGLE_REDIRECT_URI'),
  },
}
