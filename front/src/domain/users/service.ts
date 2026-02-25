import type {
  CreateSystemUserPayload,
  CurrentUser,
  ReplaceUserUnitAssignmentsPayload,
  SystemUser,
  UpdateCurrentUserPayload,
  UpdateSystemUserPayload,
  UserUnitAssignment,
} from '@/domain/users/model'
import {
  createSystemUserPayloadSchema,
  replaceUserUnitAssignmentsPayloadSchema,
  updateSystemUserPayloadSchema,
  updateCurrentUserPayloadSchema,
} from '@/domain/users/model'
import {usersRepository} from '@/domain/users/repository'

export const usersService = {
  async getCurrentUser(): Promise<CurrentUser> {
    return usersRepository.getCurrentUser()
  },

  async updateCurrentUser(
    payload: UpdateCurrentUserPayload,
  ): Promise<CurrentUser> {
    const validatedPayload = updateCurrentUserPayloadSchema.parse(payload)
    return usersRepository.updateCurrentUser(validatedPayload)
  },

  async getSystemUsers(): Promise<SystemUser[]> {
    return usersRepository.getSystemUsers()
  },

  async createSystemUser(payload: CreateSystemUserPayload): Promise<SystemUser> {
    const validatedPayload = createSystemUserPayloadSchema.parse(payload)
    return usersRepository.createSystemUser(validatedPayload)
  },

  async updateSystemUser(
    id: number,
    payload: UpdateSystemUserPayload,
  ): Promise<SystemUser> {
    const validatedPayload = updateSystemUserPayloadSchema.parse(payload)
    return usersRepository.updateSystemUser(id, validatedPayload)
  },

  async deleteSystemUser(id: number): Promise<void> {
    return usersRepository.deleteSystemUser(id)
  },

  async getUserUnitAssignments(userId: number): Promise<UserUnitAssignment[]> {
    return usersRepository.getUserUnitAssignments(userId)
  },

  async replaceUserUnitAssignments(
    userId: number,
    payload: ReplaceUserUnitAssignmentsPayload,
  ): Promise<UserUnitAssignment[]> {
    const validatedPayload = replaceUserUnitAssignmentsPayloadSchema.parse(payload)
    return usersRepository.replaceUserUnitAssignments(userId, validatedPayload)
  },
}
