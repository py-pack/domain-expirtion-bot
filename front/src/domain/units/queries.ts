import {computed, type MaybeRefOrGetter, toValue} from 'vue'
import {useMutation, useQuery, useQueryClient} from '@tanstack/vue-query'
import type {
  CreateUnitPayload,
  ReplaceUnitResponsiblesPayload,
  UpdateUnitPayload,
} from '@/domain/units/model'
import {unitsService} from '@/domain/units/service'

export const unitsQueryKeys = {
  list: ['units', 'list'] as const,
  detail: (id: number) => ['units', 'detail', id] as const,
  responsibles: (id: number) => ['units', 'responsibles', id] as const,
}

export function useUnitsQuery() {
  return useQuery({
    queryKey: unitsQueryKeys.list,
    queryFn: async () => unitsService.getUnits(),
    staleTime: 30_000,
  })
}

export function useUnitQuery(unitId: MaybeRefOrGetter<number | null>) {
  return useQuery({
    queryKey: computed(() => {
      const id = toValue(unitId)
      return id === null ? ['units', 'detail', 'none'] : unitsQueryKeys.detail(id)
    }),
    queryFn: async () => {
      const id = toValue(unitId)
      if (id === null) {
        throw new Error('Unit ID is required')
      }

      return unitsService.getUnit(id)
    },
    enabled: computed(() => toValue(unitId) !== null),
  })
}

export function useUnitResponsiblesQuery(unitId: MaybeRefOrGetter<number | null>) {
  return useQuery({
    queryKey: computed(() => {
      const id = toValue(unitId)
      return id === null ? ['units', 'responsibles', 'none'] : unitsQueryKeys.responsibles(id)
    }),
    queryFn: async () => {
      const id = toValue(unitId)
      if (id === null) {
        throw new Error('Unit ID is required')
      }

      return unitsService.getUnitResponsibles(id)
    },
    enabled: computed(() => toValue(unitId) !== null),
    staleTime: 15_000,
  })
}

export function useCreateUnitMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (payload: CreateUnitPayload) => unitsService.createUnit(payload),
    onSuccess: async () => {
      await queryClient.invalidateQueries({queryKey: unitsQueryKeys.list})
    },
  })
}

export function useUpdateUnitMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async ({id, payload}: {id: number; payload: UpdateUnitPayload}) =>
      unitsService.updateUnit(id, payload),
    onSuccess: async (_, variables) => {
      await Promise.all([
        queryClient.invalidateQueries({queryKey: unitsQueryKeys.list}),
        queryClient.invalidateQueries({queryKey: unitsQueryKeys.detail(variables.id)}),
      ])
    },
  })
}

export function useDeleteUnitMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async (id: number) => unitsService.deleteUnit(id),
    onSuccess: async () => {
      await queryClient.invalidateQueries({queryKey: unitsQueryKeys.list})
    },
  })
}

export function useReplaceUnitResponsiblesMutation() {
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: async ({
      unitId,
      payload,
    }: {
      unitId: number
      payload: ReplaceUnitResponsiblesPayload
    }) => unitsService.replaceUnitResponsibles(unitId, payload),
    onSuccess: async (_, variables) => {
      await Promise.all([
        queryClient.invalidateQueries({queryKey: unitsQueryKeys.list}),
        queryClient.invalidateQueries({
          queryKey: unitsQueryKeys.responsibles(variables.unitId),
        }),
      ])
    },
  })
}
