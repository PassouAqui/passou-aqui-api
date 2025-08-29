'use client'

import { MantineProvider, createTheme } from '@mantine/core'
import { Notifications } from '@mantine/notifications'
import { ReactNode } from 'react'

const theme = createTheme({})

export function Providers({ children }: { children: ReactNode }) {
  return (
    <MantineProvider theme={theme} defaultColorScheme="light">
      <Notifications />
      {children}
    </MantineProvider>
  )
}
