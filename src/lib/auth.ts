// src/lib/auth.ts
export async function login(username: string, password: string) {
  const res = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/accounts/login/`,
    {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, password }),
    },
  )

  if (!res.ok) throw new Error('Credenciais inválidas')

  const data = await res.json()

  // Armazena os tokens no localStorage (client-side)
  localStorage.setItem('access', data.access)
  localStorage.setItem('refresh', data.refresh)

  return data
}
