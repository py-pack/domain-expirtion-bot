import {httpClient} from '@/shared/http/client'
import {
  createUnitPayloadSchema,
  type CreateUnitPayload,
  type ReplaceUnitResponsiblesPayload,
  replaceUnitResponsiblesPayloadSchema,
  type Unit,
  type UnitDetails,
  type UnitResponsible,
  unitDetailsSchema,
  unitResponsibleSchema,
  unitSchema,
  type UpdateUnitPayload,
  updateUnitPayloadSchema,
} from '@/domain/units/model'

export interface UnitsRepository {
  getUnits(): Promise<Unit[]>
  getUnit(id: number): Promise<UnitDetails>
  createUnit(payload: CreateUnitPayload): Promise<UnitDetails>
  updateUnit(id: number, payload: UpdateUnitPayload): Promise<UnitDetails>
  deleteUnit(id: number): Promise<void>
  getUnitResponsibles(unitId: number): Promise<UnitResponsible[]>
  replaceUnitResponsibles(
    unitId: number,
    payload: ReplaceUnitResponsiblesPayload,
  ): Promise<UnitResponsible[]>
}

async function parseUnits(data: unknown): Promise<Unit[]> {
  return unitSchema.array().parseAsync(data)
}

async function parseUnit(data: unknown): Promise<UnitDetails> {
  return unitDetailsSchema.parseAsync(data)
}

async function parseUnitResponsibles(data: unknown): Promise<UnitResponsible[]> {
  return unitResponsibleSchema.array().parseAsync(data)
}

export const unitsRepository: UnitsRepository = {
  async getUnits(): Promise<Unit[]> {
    const {data} = await httpClient.get('/units/')
    return parseUnits(data)
  },

  async getUnit(id: number): Promise<UnitDetails> {
    const {data} = await httpClient.get(`/units/${id}`)
    return parseUnit(data)
  },

  async createUnit(payload: CreateUnitPayload): Promise<UnitDetails> {
    const requestPayload = createUnitPayloadSchema.parse(payload)
    const {data} = await httpClient.post('/units/', requestPayload)
    return parseUnit(data)
  },

  async updateUnit(id: number, payload: UpdateUnitPayload): Promise<UnitDetails> {
    const requestPayload = updateUnitPayloadSchema.parse(payload)
    const {data} = await httpClient.patch(`/units/${id}`, requestPayload)
    return parseUnit(data)
  },

  async deleteUnit(id: number): Promise<void> {
    await httpClient.delete(`/units/${id}`)
  },

  async getUnitResponsibles(unitId: number): Promise<UnitResponsible[]> {
    const {data} = await httpClient.get(`/units/${unitId}/responsibles`)
    return parseUnitResponsibles(data)
  },

  async replaceUnitResponsibles(
    unitId: number,
    payload: ReplaceUnitResponsiblesPayload,
  ): Promise<UnitResponsible[]> {
    const requestPayload = replaceUnitResponsiblesPayloadSchema.parse(payload)
    const {data} = await httpClient.put(`/units/${unitId}/responsibles`, requestPayload)
    return parseUnitResponsibles(data)
  },
}
