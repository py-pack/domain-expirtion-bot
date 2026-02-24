<script setup lang="ts">
import {computed, onBeforeUnmount, onMounted, ref} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import {env} from '@/env'
import {
  useGoogleCodeLoginMutation,
  useGoogleOneTapLoginMutation,
  useLoginMutation,
} from '@/domain/auth/queries'
import {getApiErrorMessage} from '@/shared/http/errors'
import UiButton from '@/ui/components/common/UiButton.vue'
import UiFormField from '@/ui/components/common/UiFormField.vue'
import IconBot from '@/ui/components/common/icons/IconBot.vue'
import IconGoogle from '@/ui/components/common/icons/IconGoogle.vue'

type GoogleCredentialResponse = {
  credential: string
}

type GoogleAccountsApi = {
  accounts: {
    id: {
      initialize: (params: {
        client_id: string
        callback: (response: GoogleCredentialResponse) => void
        auto_select: boolean
        cancel_on_tap_outside: boolean
      }) => void
      renderButton: (
        container: HTMLElement,
        options: {
          theme: 'filled_black' | 'filled_blue' | 'outline'
          size: 'large' | 'medium' | 'small'
          text: 'continue_with' | 'signin_with' | 'signup_with'
          shape: 'pill' | 'rect' | 'circle' | 'square'
          logo_alignment: 'left' | 'center'
          width?: number
        },
      ) => void
      prompt: () => void
      cancel: () => void
    }
  }
}

type WindowWithGoogle = Window & {
  google?: GoogleAccountsApi
}

const route = useRoute()
const router = useRouter()

const email = ref('')
const password = ref('')
const errorMessage = ref<string | null>(null)
const isGoogleOneTapScriptFailed = ref(false)

const loginMutation = useLoginMutation()
const googleCodeMutation = useGoogleCodeLoginMutation()
const googleOneTapMutation = useGoogleOneTapLoginMutation()

const canUsePasswordLogin = env.auth.passwordEnabled
const canUseGoogleLogin = env.auth.googleEnabled

const isLoading = computed(
  () =>
    loginMutation.isPending.value ||
    googleCodeMutation.isPending.value ||
    googleOneTapMutation.isPending.value,
)
const isGoogleFallbackVisible = computed(() => isGoogleOneTapScriptFailed.value)

function getRedirectPath(): string {
  const redirect = route.query.redirect

  if (typeof redirect === 'string' && redirect.startsWith('/')) {
    return redirect
  }

  return '/'
}

async function completeLoginFlow(): Promise<void> {
  const googleApi = (window as WindowWithGoogle).google
  googleApi?.accounts.id.cancel()

  await router.push(getRedirectPath())
}

async function handlePasswordLogin(): Promise<void> {
  errorMessage.value = null

  try {
    await loginMutation.mutateAsync({
      email: email.value,
      password: password.value,
    })

    await completeLoginFlow()
  } catch (error: unknown) {
    errorMessage.value = getApiErrorMessage(error)
  }
}

function startGoogleOauthFlow(): void {
  const params = new URLSearchParams({
    client_id: env.google.clientId,
    redirect_uri: env.google.redirectUri,
    response_type: 'code',
    scope: 'openid email profile',
    prompt: 'select_account',
    include_granted_scopes: 'true',
  })

  const googleAuthorizeUrl = `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`
  const popup = window.open(
    googleAuthorizeUrl,
    'google-auth',
    'width=520,height=720,menubar=no,toolbar=no,status=no,scrollbars=yes',
  )

  if (!popup) {
    window.location.assign(googleAuthorizeUrl)
  }
}

async function handleGoogleOneTapCallback(
  response: GoogleCredentialResponse,
): Promise<void> {
  errorMessage.value = null

  try {
    await googleOneTapMutation.mutateAsync({
      id_token: response.credential,
    })

    await completeLoginFlow()
  } catch (error: unknown) {
    errorMessage.value = getApiErrorMessage(error)
  }
}

function getGoogleApi(): GoogleAccountsApi | undefined {
  return (window as WindowWithGoogle).google
}

function initializeGoogleOneTap(): void {
  const googleApi = getGoogleApi()

  if (!googleApi) {
    isGoogleOneTapScriptFailed.value = true
    return
  }

  const container = document.getElementById('google-one-tap-container')

  if (!container) {
    isGoogleOneTapScriptFailed.value = true
    return
  }

  try {
    googleApi.accounts.id.initialize({
      client_id: env.google.clientId,
      callback: handleGoogleOneTapCallback,
      auto_select: false,
      cancel_on_tap_outside: false,
    })

    googleApi.accounts.id.renderButton(container, {
      theme: 'filled_black',
      size: 'large',
      text: 'continue_with',
      shape: 'pill',
      logo_alignment: 'left',
      width: 320,
    })

    googleApi.accounts.id.prompt()
    isGoogleOneTapScriptFailed.value = false
  } catch {
    isGoogleOneTapScriptFailed.value = true
  }
}

async function loadGoogleScript(): Promise<void> {
  await new Promise<void>((resolve, reject) => {
    const scriptId = 'google-one-tap-script'
    const existingScript = document.getElementById(scriptId)

    if (existingScript) {
      resolve()
      return
    }

    const script = document.createElement('script')
    script.id = scriptId
    script.src = 'https://accounts.google.com/gsi/client'
    script.async = true
    script.defer = true
    script.onload = () => resolve()
    script.onerror = () => reject(new Error('Failed to load Google script'))

    document.head.appendChild(script)
  })
}

function handleGoogleAuthMessage(event: MessageEvent): void {
  if (event.origin !== window.location.origin) {
    return
  }

  if (event.data?.type !== 'google-auth-callback') {
    return
  }

  const payload = event.data?.payload ?? {}
  const code = payload.code

  if (typeof code !== 'string' || code.length === 0) {
    errorMessage.value = payload.error_description || 'Google login failed.'
    return
  }

  errorMessage.value = null
  googleCodeMutation
    .mutateAsync({code})
    .then(completeLoginFlow)
    .catch((error: unknown) => {
      errorMessage.value = getApiErrorMessage(error)
    })
}

function handleGoogleRedirectCallback(): boolean {
  const queryParams = route.query ?? {}

  if (!Object.keys(queryParams).length) {
    return false
  }

  if (window.opener && window.opener !== window) {
    window.opener.postMessage(
      {
        type: 'google-auth-callback',
        payload: queryParams,
      },
      window.location.origin,
    )
    window.close()
    return true
  }

  void router.replace({query: {}})
  const code = queryParams.code

  if (typeof code !== 'string' || code.length === 0) {
    errorMessage.value =
      typeof queryParams.error_description === 'string'
        ? queryParams.error_description
        : 'Google login failed.'
    return true
  }

  googleCodeMutation
    .mutateAsync({code})
    .then(completeLoginFlow)
    .catch((error: unknown) => {
      errorMessage.value = getApiErrorMessage(error)
    })

  return true
}

onMounted(async () => {
  window.addEventListener('message', handleGoogleAuthMessage)

  const redirectHandled = handleGoogleRedirectCallback()

  if (redirectHandled) {
    return
  }

  if (!canUseGoogleLogin) {
    return
  }

  try {
    await loadGoogleScript()
    initializeGoogleOneTap()
  } catch {
    isGoogleOneTapScriptFailed.value = true
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('message', handleGoogleAuthMessage)
})
</script>

<template>
  <div class="auth-page">
    <div class="auth-content">
      <section class="auth-logo">
        <IconBot class="auth-logo__icon" />
        <h1 class="auth-logo__text">
          DOMAIN
          <br />
          EXPIRATION
          <br />
          BOT
        </h1>
      </section>

      <section class="auth-form-container">
        <h2 class="auth-form-container__title">Sign in</h2>

        <form v-if="canUsePasswordLogin" class="auth-form" @submit.prevent="handlePasswordLogin">
          <UiFormField
            id="login-email"
            label="Email address"
            type="email"
            autocomplete="email"
            required
            :model-value="email"
            @update:model-value="email = $event"
          />

          <UiFormField
            id="login-password"
            label="Password"
            type="password"
            autocomplete="current-password"
            required
            :model-value="password"
            @update:model-value="password = $event"
          />

          <UiButton class="auth-form__submit" type="submit" size="lg" :disabled="isLoading">
            {{ isLoading ? 'Signing in...' : 'Sign in' }}
          </UiButton>
        </form>

        <p v-if="errorMessage" class="auth-form-container__error">{{ errorMessage }}</p>

        <template v-if="canUseGoogleLogin">
          <div class="auth-divider"><span>OR</span></div>

          <div class="auth-google">
            <UiButton
              v-if="isGoogleFallbackVisible"
              class="auth-form__google auth-form__google--dark"
              variant="secondary"
              size="lg"
              :disabled="isLoading"
              @click="startGoogleOauthFlow"
            >
              <IconGoogle class="auth-form__google-icon" />
              Continue with Google
            </UiButton>
            <div v-else id="google-one-tap-container" class="auth-google__one-tap"></div>
          </div>
        </template>

        <p v-if="!canUsePasswordLogin && !canUseGoogleLogin" class="auth-form-container__error">
          No authentication methods are enabled.
        </p>
      </section>
    </div>
  </div>
</template>

<style scoped lang="scss">
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 16px;
  background-color: #0f172a;
  background: radial-gradient(circle at center, #1f2c45 0%, #0f172a 100%);
}

.auth-content {
  width: 100%;
  max-width: 900px;
  display: flex;
  align-items: center;
  justify-content: space-around;
  gap: 32px;
}

.auth-logo {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;

  &__icon {
    color: #4f8bff;
    width: 120px;
    height: 120px;
    filter: drop-shadow(0 0 20px rgba(79, 139, 255, 0.3));
  }

  &__text {
    font-size: 32px;
    font-weight: 700;
    text-align: center;
    line-height: 1.2;
    color: #4f8bff;
    text-shadow: 0 0 20px rgba(79, 139, 255, 0.3);
  }
}

.auth-form-container {
  width: 100%;
  max-width: 400px;
  padding: 32px;
  border-radius: 12px;
  border: 1px solid rgba(148, 163, 184, 0.25);
  box-shadow:
    0 0 0 1px rgba(255, 255, 255, 0.12),
    0 20px 25px -10px rgba(0, 0, 0, 0.18);
  backdrop-filter: blur(10px);
  background: rgba(23, 32, 51, 0.65);
  display: grid;
  gap: 16px;

  &__title {
    margin-bottom: 4px;
    color: #e5edff;
  }

  &__error {
    color: #ff9b8f;
    font-size: 0.875rem;
  }
}

.auth-form {
  display: grid;
  gap: 12px;

  :deep(.ui-form-label) {
    color: #d2dcf3;
  }

  :deep(.ui-input) {
    background-color: rgba(30, 41, 59, 0.85);
    border: 1px solid rgba(148, 163, 184, 0.35);
    color: #f8fbff;
  }

  :deep(.ui-input::placeholder) {
    color: rgba(226, 232, 240, 0.65);
  }

  :deep(.ui-input:focus) {
    border-color: #4f8bff;
    box-shadow: 0 0 0 3px rgba(79, 139, 255, 0.22);
  }

  &__submit,
  &__google {
    width: 100%;
    min-height: 48px;
  }

  &__submit {
    background: linear-gradient(to right, #2563eb, #1d4ed8);
    border-color: transparent;
    color: #ffffff;

    &:hover:not(:disabled) {
      background: linear-gradient(to right, #1d4ed8, #1e40af);
    }
  }

  &__google {
    background: #ffffff;
    border: 1px solid #d7deef;
    color: #1f2a3d;

    &:hover:not(:disabled) {
      background: #f6f8ff;
    }
  }

  &__google--dark {
    background:
      radial-gradient(circle at 14% 20%, rgba(79, 139, 255, 0.12), transparent 52%),
      linear-gradient(180deg, #1b2740 0%, #152238 100%);
    border: 1px solid rgba(120, 156, 221, 0.28);
    color: #f8fafc;
    box-shadow:
      inset 0 1px 0 rgba(255, 255, 255, 0.07),
      inset 0 -1px 0 rgba(79, 139, 255, 0.08),
      0 10px 20px rgba(7, 12, 24, 0.28);

    &:hover:not(:disabled) {
      background:
        radial-gradient(circle at 14% 20%, rgba(79, 139, 255, 0.18), transparent 56%),
        linear-gradient(180deg, #1f2d49 0%, #17263f 100%);
      border-color: rgba(120, 156, 221, 0.34);
    }
  }

  &__google-icon {
    flex-shrink: 0;
  }
}

.auth-google {
  display: flex;
  justify-content: center;
}

.auth-google__one-tap {
  width: 100%;
  min-height: 48px;
  display: flex;
  justify-content: center;
  padding: 8px;
  border-radius: 16px;
  border: 1px solid rgba(120, 156, 221, 0.22);
  background:
    radial-gradient(circle at 12% 20%, rgba(79, 139, 255, 0.1), transparent 58%),
    linear-gradient(180deg, rgba(24, 37, 60, 0.78), rgba(17, 29, 48, 0.92));
  box-shadow:
    inset 0 1px 0 rgba(255, 255, 255, 0.05),
    0 8px 18px rgba(7, 12, 24, 0.18);

  :deep(div),
  :deep(iframe) {
    border-radius: 999px;
  }
}

.auth-divider {
  display: flex;
  align-items: center;
  text-align: center;
  margin: 4px 0;

  &::before,
  &::after {
    content: '';
    flex: 1;
    border-bottom: 1px solid var(--color-border);
  }

  span {
    padding: 0 16px;
    color: rgba(226, 232, 240, 0.68);
    font-size: 0.875rem;
  }
}

@media (max-width: 768px) {
  .auth-content {
    flex-direction: column;
    gap: 24px;
  }

  .auth-logo {
    &__icon {
      width: 88px;
      height: 88px;
    }

    &__text {
      font-size: 24px;
    }
  }
}
</style>
