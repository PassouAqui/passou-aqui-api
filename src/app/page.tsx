'use client'

import { Button, Container, Title, Text, Paper } from '@mantine/core'
import { useRouter } from 'next/navigation'

export default function HomePage() {
  const router = useRouter()

  const handleNavigate = () => {
    router.push('/teste')
  }

  return (
    <main className="min-h-screen flex bg-blue-200 text-white">
      <Container size="sm">
        <Paper
          p="xl"
          radius="md"
          shadow="md"
          className="bg-white text-gray-900 mt-8"
        >
          <Title order={2} className="mb-4 text-center ">
            🎉 Boas-vindas ao Passou Aquiiiiiiiiiiiiii!
          </Title>
          <Text size="md" className="text-center mb-6">
            Seu sistema de gerenciamento de produtos está pronto para evoluir.
          </Text>
          <div className="flex justify-center">
            <Button
              color="indigo"
              size="md"
              variant="filled"
              onClick={handleNavigate}
            >
              Acessar dashboard
            </Button>
          </div>
        </Paper>
      </Container>
    </main>
  )
}
