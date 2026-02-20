import {useMutation} from '@tanstack/vue-query'
import type {
  GoogleCodePayload,
  GoogleOneTapPayload,
  LoginPayload,
} from '@/domain/auth/model'
import {authService} from '@/domain/auth/service'

export function useLoginMutation() {
  return useMutation({
    mutationFn: async (payload: LoginPayload): Promise<void> => authService.login(payload),
  })
}

export function useGoogleCodeLoginMutation() {
  return useMutation({
    mutationFn: async (payload: GoogleCodePayload): Promise<void> =>
      authService.loginWithGoogleCode(payload),
  })
}

export function useGoogleOneTapLoginMutation() {
  return useMutation({
    mutationFn: async (payload: GoogleOneTapPayload): Promise<void> =>
      authService.loginWithGoogleOneTap(payload),
  })
}

export function useLogoutMutation() {
  return useMutation({
    mutationFn: async (): Promise<void> => authService.logout(),
  })
}
