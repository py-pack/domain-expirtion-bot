<script setup lang="ts">
import {ref, onMounted} from 'vue'
import {useRouter, useRoute} from 'vue-router'
import {loginUser, loginWithGoogle, loginWithGoogleOneTap} from '@/api/auth'
import Button from '@/components/ui/Button.vue';
import IconBot from '@/components/icons/IconBot.vue';
import {env} from '@/env'

const email = ref('')
const password = ref('')
const errorMessage = ref<string | null>(null)
const router = useRouter()

const isLoading = ref(false);

const handleLogin = async () => {
  isLoading.value = true;
  errorMessage.value = null

  loginUser({email: email.value, password: password.value,})
      .then(() => {
        // @ts-ignore
        window.google?.accounts?.id?.cancel?.()
        router.push('/')
      })
      .catch((error: unknown) => {
        errorMessage.value = error instanceof Error ? error.message : 'Login failed'
      })
      .finally(() => isLoading.value = false)
}

const handleGoogleSignIn = () => {
  const params = new URLSearchParams({
    client_id: env.google.clientId,
    redirect_uri: env.google.redirectUri,
    response_type: 'code',
    scope: 'openid email profile',
    prompt: 'select_account',
    access_type: 'offline',
  })

  window.location.href = `https://accounts.google.com/o/oauth2/v2/auth?${params.toString()}`
}

async function handleGoogleCredentialResponse(response: google.accounts.id.CredentialResponse) {
  isLoading.value = true
  errorMessage.value = null

  const idToken = response.credential
  loginWithGoogleOneTap(idToken)
      .then(() => {
        // @ts-ignore
        window.google?.accounts?.id?.cancel?.()
        router.push('/')
      })
      .catch((error: unknown) => {
        errorMessage.value = error instanceof Error ? error.message : 'Login failed'
        try {
          // @ts-ignore
          window.google.accounts.id.prompt()
        } catch (err) {
          console.warn("Manual prompt error", err)
        }
      })
      .finally(() => isLoading.value = false)
}

function loadGoogleScript() {
  return new Promise((resolve) => {
    const existing = document.getElementById('google-one-tap')
    if (!existing) {
      const script = document.createElement('script')
      script.src = 'https://accounts.google.com/gsi/client'
      script.async = true
      script.defer = true
      script.id = 'google-one-tap'
      script.onload = resolve
      document.head.appendChild(script)
    } else {
      resolve(null)
    }
  }).then(() => {
    // @ts-ignore
    window.google.accounts.id.initialize({
      client_id: env.google.clientId,
      callback: handleGoogleCredentialResponse,
      auto_select: false,
      cancel_on_tap_outside: false,
    })

    // @ts-ignore
    window.google.accounts.id.prompt()
  })
}

onMounted(() => {
  loadGoogleScript()

  const route = useRoute();
  const code = route.query.code as string | null;
  if (code) {
    isLoading.value = true
    loginWithGoogle(code)
        .then(() => {
          // @ts-ignore
          window.google?.accounts?.id?.cancel?.()
          router.push('/')
        })
        .catch((error: unknown) => {
          errorMessage.value = error instanceof Error ? error.message : 'Google login failed'
        })
        .finally(() => isLoading.value = false)
  }
})

</script>

<template>

  <div class="auth-page">
    <div class="auth-content">
      <div class="auth-logo">
        <IconBot class="logo-icon"/>
        <h1 class="logo-text">
          DOMAIN<br>
          EXPIRATION<br>
          BOT
        </h1>
      </div>

      <div class="auth-form-container">
        <form class="auth-form" @submit.prevent="handleLogin">
          <div class="form-group">
            <label for="email">Email address</label>
            <input
                type="email"
                id="email"
                v-model="email"
                required
                autocomplete="email"
            />
          </div>

          <div class="form-group">
            <label for="password">Password</label>
            <input
                type="password"
                id="password"
                v-model="password"
                required
                autocomplete="current-password"
            />
          </div>

          <div v-if="errorMessage" class="alert alert-danger">
            {{ errorMessage }}
          </div>

          <Button
              variant="primary"
              type="submit"
              :disabled="isLoading"
              class="sign-in-btn"
          >
            {{ isLoading ? 'Signing in...' : 'Sign in' }}
          </Button>

          <div class="divider">
            <span>OR</span>
          </div>

          <Button
              variant="secondary"
              type="button"
              @click="handleGoogleSignIn"
              class="google-btn"
          >
            Sign in with Google
          </Button>
        </form>
      </div>
    </div>
  </div>
</template>
