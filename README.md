<<<<<<< HEAD
Env exemple
POSTGRES_DB='nome_db'
POSTGRES_USER='user_db'
POSTGRES_PASSWORD='senha_db'
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
=======
# 🧠 Passou Aqui - Frontend

Projeto frontend utilizando [Next.js 15+](https://nextjs.org/), [Mantine](https://mantine.dev/), [Tailwind CSS](https://tailwindcss.com/), [TypeScript](https://www.typescriptlang.org/) e [pnpm](https://pnpm.io/), com ambiente completo para desenvolvimento e produção via Docker.

---

## 📦 Tecnologias

- [Next.js 15 (App Router)](https://nextjs.org/docs)
- [TypeScript](https://www.typescriptlang.org/)
- [Mantine UI](https://mantine.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [pnpm](https://pnpm.io/)
- [ESLint + Prettier + Husky + Lint-Staged](https://eslint.org/)
- [Docker](https://www.docker.com/)

---

## 🚀 Como rodar o projeto

### ✅ Usando Docker (recomendado)

> Não precisa instalar Node, pnpm nem dependências locais.

#### 1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/passou-aqui-client.git
cd passou-aqui-client
```

#### 2. Rode com Docker Compose (modo desenvolvimento):

```bash
docker-compose -f config/docker/docker-compose.dev.yml up --build
```

#### 3. Acesse:

[http://localhost:3000](http://localhost:3000)

---

## 🧪 Scripts de desenvolvimento

### Se quiser usar pnpm localmente:

```bash
pnpm install          # instala dependências
pnpm dev              # roda o projeto local (sem docker)
pnpm lint             # lint + prettier
pnpm format           # aplica prettier
pnpm dev:docker       # roda com docker-compose.dev.yml
pnpm prod:docker      # roda com docker-compose.yml (build de produção)
```

---

## 📁 Estrutura de pastas

```bash
/passou-aqui-client
├── config
│   ├── docker
│   │   ├── Dockerfile
│   │   ├── Dockerfile.dev
│   │   ├── docker-compose.yml
│   │   └── docker-compose.dev.yml
├── public
├── src
├── .env.local
├── .gitignore
├── .prettierrc
├── .dockerignore
├── postcss.config.mjs
├── tailwind.config.ts
├── next.config.ts
├── tsconfig.json
├── package.json
├── README.md
├── eslint.config.mjs
```

---

## 🌐 Variáveis de ambiente

- Ambiente de desenvolvimento: `.env.local`
- Ambiente de produção: `.env.production`

Exemplo:

```env
NEXT_PUBLIC_API_URL=http://localhost:3000/api
```

---

## 🐳 Observações Docker

- A imagem base usa `node:22-alpine`
- Hot reload funcionando com volume bind do host
- Porta padrão exposta: `3000`

---
<<<<<<< HEAD


>>>>>>> fb4b0b5 (Update README.md)
=======
>>>>>>> 85c6060 (feat: add login functionality and middleware protection)
