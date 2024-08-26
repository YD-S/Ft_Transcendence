
# Ft Transcendence
- [Frontend docs](docs/frontend.md)

## Run the project

Copy and configure the `.env` file

```bash
cp env.example .env
```

Create volume directory
```bash
mkdir -p ~/data/database
mkdir -p ~/data/redis
```

Run the project in production mode

```bash
docker-compose up --build
```

Run the project in development mode

```bash
docker-compose -f docker-compose-dev.yml up --build
```

## Modules

Total points: 10/12

- Major modules (1 point each):
  - [x] MAJOR: Backend framework
  - [x] MAJOR: 2FA, JWT
  - [x] MAJOR: User management
  - [x] MAJOR: OAuth
  - [x] MAJOR: Live chat
  - [x] MAJOR: Remote players
  - [x] MAJOR: 3D rendering
  - [x] MAJOR: Server-side Pong
  - [ ] MAJOR: AI

- Minor modules (0.5 points each):
  - [x] MINOR: Frontend toolkit
  - [x] MINOR: Database
  - [x] MINOR: SSR
  - [x] MINOR: Translation
  - [ ] MINOR: User stats
  - [ ] MINOR: Game customization
