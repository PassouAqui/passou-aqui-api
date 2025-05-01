// src/app/login/page.tsx
'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { login } from '@/lib/auth'
import { Button, TextInput } from '@mantine/core'

export default function LoginPage() {
  const [username, setUserName] = useState('')
  const [password, setPassword] = useState('')
  const router = useRouter()

  const handleLogin = async () => {
    try {
      await login(username, password)
      if (!localStorage.getItem('access')) {
        alert('Falha no login')
        return
      }
      router.push('/dashboard')
    } catch (err) {
      alert('Falha no login')
    }
  }

  return (
    <div className="p-8 max-w-md mx-auto">
      <h1 className="text-2xl font-bold mb-4">Entrar</h1>
      <TextInput
        label="Username"
        value={username}
        onChange={(e) => setUserName(e.currentTarget.value)}
      />
      <TextInput
        label="Senha"
        type="password"
        value={password}
        onChange={(e) => setPassword(e.currentTarget.value)}
        className="mt-4"
      />
      <Button onClick={handleLogin} className="mt-6">
        Entrar
      </Button>
    </div>
  )
}
