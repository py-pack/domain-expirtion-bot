<script setup lang="ts">
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {loginUser} from '@/api/auth'

const email = ref('')
const password = ref('')
const errorMessage = ref<string | null>(null)
const router = useRouter()

const handleLogin = async () => {
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
</script>

<template>
  <div class="d-flex justify-content-center align-items-center flex-column"
       style="min-height: 100vh">
    <h1 class="mb-4">Login</h1>

    <form @submit.prevent="handleLogin" class="w-100" style="max-width: 400px">
      <div class="mb-3">
        <label for="email" class="form-label">Email</label>
        <input
            v-model="email"
            type="email"
            class="form-control"
            id="email"
            placeholder="Enter your email"
            required
        />
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">Password</label>
        <input
            v-model="password"
            type="password"
            class="form-control"
            id="password"
            placeholder="Enter your password"
            required
        />
      </div>

      <div v-if="errorMessage" class="alert alert-danger">
        {{ errorMessage }}
      </div>

      <button type="submit" class="btn btn-primary w-100">Log In</button>
    </form>
  </div>
</template>
