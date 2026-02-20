type RawEnv = {
  VITE__API_BASE_URL?: string
  VITE__GOOGLE_CLIENT_ID?: string
  VITE__GOOGLE_REDIRECT_URI?: string
  VITE_AUTH_PASSWORD_ENABLED?: string
  VITE_AUTH_GOOGLE_ENABLED?: string
}

const rawEnv = import.meta.env as unknown as RawEnv

function requireEnv(key: keyof RawEnv): string {
  const value = rawEnv[key]
  if (!value) {
    throw new Error(`Env variable "${key}" is not defined`)
  }

  return value
}

function readBooleanEnv(key: keyof RawEnv, fallback: boolean): boolean {
  const value = rawEnv[key]

  if (value === undefined || value === '') {
    return fallback
  }

  return ['1', 'true', 'yes', 'on'].includes(value.toLowerCase())
}

const hasGoogleConfig = Boolean(rawEnv.VITE__GOOGLE_CLIENT_ID && rawEnv.VITE__GOOGLE_REDIRECT_URI)
const googleEnabled = readBooleanEnv('VITE_AUTH_GOOGLE_ENABLED', hasGoogleConfig)

if (googleEnabled && !hasGoogleConfig) {
  throw new Error(
    'Google auth is enabled but VITE__GOOGLE_CLIENT_ID or VITE__GOOGLE_REDIRECT_URI is missing',
  )
}

export const env = {
  api: {
    baseUrl: requireEnv('VITE__API_BASE_URL'),
  },
  auth: {
    passwordEnabled: readBooleanEnv('VITE_AUTH_PASSWORD_ENABLED', true),
    googleEnabled,
  },
  google: {
    clientId: rawEnv.VITE__GOOGLE_CLIENT_ID ?? '',
    redirectUri: rawEnv.VITE__GOOGLE_REDIRECT_URI ?? '',
  },
}
