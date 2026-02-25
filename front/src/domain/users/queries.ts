import {useMutation, useQuery, useQueryClient} from '@tanstack/vue-query'
import {computed, type MaybeRefOrGetter, toValue} from 'vue'
import type {
  CreateSystemUserPayload,
  ReplaceUserUnitAssignmentsPayload,
  UpdateCurrentUserPayload,
  UpdateSystemUserPayload,
} from '@/domain/users/model'
import {usersService} from '@/domain/users/service'

export const usersQueryKeys = {
  me: ['users', 'me'] as const,
  list: ['users', 'list'] as const,
  units: (userId: number) => ['users', 'units', userId] as const,
}

export function useCurrentUserQuery() {
  return useQuery({
    queryKey: usersQueryKeys.me,
    queryFn: async () => usersService.getCurrentUser(),
    staleTime: 60_000,
  })
}

export function useUpdateCurrentUserMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (payload: UpdateCurrentUserPayload) =>
      usersService.updateCurrentUser(payload),
    onSuccess: async () => {
      await queryClient.invalidateQueries({
        queryKey: usersQueryKeys.me,
      })
    },
  })
}

export function useSystemUsersQuery() {
  return useQuery({
    queryKey: usersQueryKeys.list,
    queryFn: async () => usersService.getSystemUsers(),
    staleTime: 30_000,
  })
}

export function useCreateSystemUserMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (payload: CreateSystemUserPayload) =>
      usersService.createSystemUser(payload),
    onSuccess: async () => {
      await queryClient.invalidateQueries({queryKey: usersQueryKeys.list})
    },
  })
}

export function useUpdateSystemUserMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async ({
      id,
      payload,
    }: {
      id: number
      payload: UpdateSystemUserPayload
    }) => usersService.updateSystemUser(id, payload),
    onSuccess: async () => {
      await queryClient.invalidateQueries({queryKey: usersQueryKeys.list})
    },
  })
}

export function useDeleteSystemUserMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (id: number) => usersService.deleteSystemUser(id),
    onSuccess: async () => {
      await queryClient.invalidateQueries({queryKey: usersQueryKeys.list})
    },
  })
}

export function useUserUnitAssignmentsQuery(userId: MaybeRefOrGetter<number | null>) {
  return useQuery({
    queryKey: computed(() => {
      const id = toValue(userId)
      return id === null ? ['users', 'units', 'none'] : usersQueryKeys.units(id)
    }),
    queryFn: async () => {
      const id = toValue(userId)
      if (id === null) {
        throw new Error('User ID is required')
      }

      return usersService.getUserUnitAssignments(id)
    },
    enabled: computed(() => toValue(userId) !== null),
    staleTime: 15_000,
  })
}

export function useReplaceUserUnitAssignmentsMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async ({
      userId,
      payload,
    }: {
      userId: number
      payload: ReplaceUserUnitAssignmentsPayload
    }) => usersService.replaceUserUnitAssignments(userId, payload),
    onSuccess: async (_, variables) => {
      await queryClient.invalidateQueries({
        queryKey: usersQueryKeys.units(variables.userId),
      })
    },
  })
}
