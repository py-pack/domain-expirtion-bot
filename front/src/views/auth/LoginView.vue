<script setup lang="ts">
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {loginUser} from '@/api/auth'
import Button from '@/components/ui/Button.vue';
import IconBot from '@/components/icons/IconBot.vue';

const email = ref('')
const password = ref('')
const errorMessage = ref<string | null>(null)
const router = useRouter()

const isLoading = ref(false);

const handleLogin = async () => {
  isLoading.value = true;

  errorMessage.value = null

  loginUser({
    email: email.value,
    password: password.value,
  }).then(() => {
    router.push('/dashboard')
  }).catch((error: unknown) => {
    errorMessage.value = error instanceof Error ? error.message : 'Login failed'
  })
}

const handleGoogleSignIn = () => {
  // TODO: Implement Google Sign In
  console.log('Google Sign In clicked');
};
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
