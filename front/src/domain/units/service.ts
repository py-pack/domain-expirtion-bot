import type {
  CreateUnitPayload,
  ReplaceUnitResponsiblesPayload,
  Unit,
  UnitDetails,
  UnitResponsible,
  UpdateUnitPayload,
} from '@/domain/units/model'
import {
  createUnitPayloadSchema,
  replaceUnitResponsiblesPayloadSchema,
  updateUnitPayloadSchema,
} from '@/domain/units/model'
import {unitsRepository} from '@/domain/units/repository'

export const unitsService = {
  async getUnits(): Promise<Unit[]> {
    return unitsRepository.getUnits()
  },

  async getUnit(id: number): Promise<UnitDetails> {
    return unitsRepository.getUnit(id)
  },

  async createUnit(payload: CreateUnitPayload): Promise<UnitDetails> {
    const validatedPayload = createUnitPayloadSchema.parse(payload)
    return unitsRepository.createUnit(validatedPayload)
  },

  async updateUnit(id: number, payload: UpdateUnitPayload): Promise<UnitDetails> {
    const validatedPayload = updateUnitPayloadSchema.parse(payload)
    return unitsRepository.updateUnit(id, validatedPayload)
  },

  async deleteUnit(id: number): Promise<void> {
    return unitsRepository.deleteUnit(id)
  },

  async getUnitResponsibles(unitId: number): Promise<UnitResponsible[]> {
    return unitsRepository.getUnitResponsibles(unitId)
  },

  async replaceUnitResponsibles(
    unitId: number,
    payload: ReplaceUnitResponsiblesPayload,
  ): Promise<UnitResponsible[]> {
    const validatedPayload = replaceUnitResponsiblesPayloadSchema.parse(payload)
    return unitsRepository.replaceUnitResponsibles(unitId, validatedPayload)
  },
}
