import { api } from '@/lib/api'
import { AuthResponse, RegisterPayload } from '../types/auth-type'

export async function registerUser(
  payload: RegisterPayload,
): Promise<AuthResponse> {
  return await api<AuthResponse>('accounts/register/', 'POST', payload)
}
