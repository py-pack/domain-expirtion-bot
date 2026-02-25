import {httpClient} from '@/shared/http/client'
import {
  createSystemUserPayloadSchema,
  type CreateSystemUserPayload,
  type CurrentUser,
  type ReplaceUserUnitAssignmentsPayload,
  type SystemUser,
  type UpdateCurrentUserPayload,
  type UpdateSystemUserPayload,
  currentUserSchema,
  replaceUserUnitAssignmentsPayloadSchema,
  systemUserSchema,
  type UserUnitAssignment,
  userUnitAssignmentSchema,
  updateSystemUserPayloadSchema,
  updateCurrentUserPayloadSchema,
} from '@/domain/users/model'

export interface UsersRepository {
  getCurrentUser(): Promise<CurrentUser>
  updateCurrentUser(payload: UpdateCurrentUserPayload): Promise<CurrentUser>
  getSystemUsers(): Promise<SystemUser[]>
  createSystemUser(payload: CreateSystemUserPayload): Promise<SystemUser>
  updateSystemUser(id: number, payload: UpdateSystemUserPayload): Promise<SystemUser>
  deleteSystemUser(id: number): Promise<void>
  getUserUnitAssignments(userId: number): Promise<UserUnitAssignment[]>
  replaceUserUnitAssignments(
    userId: number,
    payload: ReplaceUserUnitAssignmentsPayload,
  ): Promise<UserUnitAssignment[]>
}

async function parseCurrentUser(data: unknown): Promise<CurrentUser> {
  return currentUserSchema.parseAsync(data)
}

async function parseSystemUser(data: unknown): Promise<SystemUser> {
  return systemUserSchema.parseAsync(data)
}

async function parseSystemUsers(data: unknown): Promise<SystemUser[]> {
  return systemUserSchema.array().parseAsync(data)
}

async function parseUserUnitAssignments(data: unknown): Promise<UserUnitAssignment[]> {
  return userUnitAssignmentSchema.array().parseAsync(data)
}

export const usersRepository: UsersRepository = {
  async getCurrentUser(): Promise<CurrentUser> {
    const {data} = await httpClient.get('/users/me')
    return parseCurrentUser(data)
  },

  async updateCurrentUser(payload: UpdateCurrentUserPayload): Promise<CurrentUser> {
    const requestPayload = updateCurrentUserPayloadSchema.parse(payload)
    const {data} = await httpClient.patch('/users/me', requestPayload)

    return parseCurrentUser(data)
  },

  async getSystemUsers(): Promise<SystemUser[]> {
    const {data} = await httpClient.get('/users/')
    return parseSystemUsers(data)
  },

  async createSystemUser(payload: CreateSystemUserPayload): Promise<SystemUser> {
    const requestPayload = createSystemUserPayloadSchema.parse(payload)
    const {data} = await httpClient.post('/users/', requestPayload)

    return parseSystemUser(data)
  },

  async updateSystemUser(id: number, payload: UpdateSystemUserPayload): Promise<SystemUser> {
    const requestPayload = updateSystemUserPayloadSchema.parse(payload)
    const {data} = await httpClient.patch(`/users/${id}`, requestPayload)

    return parseSystemUser(data)
  },

  async deleteSystemUser(id: number): Promise<void> {
    await httpClient.delete(`/users/${id}`)
  },

  async getUserUnitAssignments(userId: number): Promise<UserUnitAssignment[]> {
    const {data} = await httpClient.get(`/users/${userId}/units`)
    return parseUserUnitAssignments(data)
  },

  async replaceUserUnitAssignments(
    userId: number,
    payload: ReplaceUserUnitAssignmentsPayload,
  ): Promise<UserUnitAssignment[]> {
    const requestPayload = replaceUserUnitAssignmentsPayloadSchema.parse(payload)
    const {data} = await httpClient.put(`/users/${userId}/units`, requestPayload)
    return parseUserUnitAssignments(data)
  },
}
