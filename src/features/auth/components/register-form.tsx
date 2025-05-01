'use client'

import { useState } from 'react'
import {
  TextInput,
  PasswordInput,
  Button,
  Paper,
  Title,
  Stack,
} from '@mantine/core'
import { useForm } from '@mantine/form'
import { notifications } from '@mantine/notifications'
import { RegisterPayload } from '../types/auth-type'
import { registerUser } from '../services/register-user'

export function RegisterForm() {
  const [loading, setLoading] = useState(false)

  const form = useForm<RegisterPayload>({
    initialValues: {
      username: '',
      email: '',
      password: '',
    },
  })

  const handleSubmit = async (values: RegisterPayload) => {
    setLoading(true)
    try {
      const data = await registerUser(values)
      notifications.show({
        title: 'Sucesso',
        message: 'Registrado com sucesso!',
      })
      console.log('Tokens recebidos:', data)
    } catch (error: any) {
      notifications.show({
        color: 'red',
        title: 'Erro',
        message: error.message,
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Paper
      withBorder
      shadow="md"
      p="xl"
      radius="md"
      className="max-w-md mx-auto mt-10"
    >
      <Title order={2} className="mb-4 text-center">
        Criar Conta
      </Title>
      <form onSubmit={form.onSubmit(handleSubmit)}>
        <Stack>
          <TextInput label="Usuário" {...form.getInputProps('username')} />
          <TextInput
            label="Email"
            type="email"
            {...form.getInputProps('email')}
          />
          <PasswordInput label="Senha" {...form.getInputProps('password')} />
          <Button type="submit" loading={loading} fullWidth>
            Cadastrar
          </Button>
        </Stack>
      </form>
    </Paper>
  )
}
