import '@mantine/core/styles.css'
import '@mantine/notifications/styles.css'

import { ColorSchemeScript } from '@mantine/core'
import { Providers } from './mantine-provider'
import type { ReactNode } from 'react'
import './globals.css'

export const metadata = {
  title: 'Passou Aqui',
  description: 'Dashboard de solicitações',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="pt-BR" suppressHydrationWarning>
      <head>
        <ColorSchemeScript />
      </head>
      <body>
        <Providers>{children}</Providers>
      </body>
    </html>
  )
}
