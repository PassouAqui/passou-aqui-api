export function formatApiError(error: unknown): string {
  if (!error || typeof error !== 'object') return 'Erro inesperado'

  // @ts-ignore
  if (error.message) return error.message

  // @ts-ignore
  if (error.detail) return error.detail

  // @ts-ignore
  if (typeof error.json === 'function') {
    return 'Erro ao processar resposta da API'
  }

  // @ts-ignore
  const entries = Object.entries(error)
  if (entries.length > 0) {
    return entries
      .map(([field, msgs]) => `${field}: ${(msgs as string[]).join(', ')}`)
      .join('\n')
  }

  return 'Erro desconhecido'
}
