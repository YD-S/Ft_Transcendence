
# Ft Transcendence

- [Backend docs](docs/backend.md)
- [Frontend docs](docs/frontend.md)

## Run the project

Copy and configure the `.env` file

```bash
cp env.example .env
```

Create database directory
```bash
mkdir -p ~/data/database
```

Run the project

```bash
docker-compose up
```

Run the project in development mode

```bash
docker-compose -f docker-compose.dev.yml up
```

## Modules

Total points: 7/14

- Major modules (1 point each):
  - [x] MAJOR: Backend framework
  - [x] MAJOR: 2FA, JWT
  - [x] MAJOR: User management
  - [x] MAJOR: OAuth
  - [x] MAJOR: Live chat
  - [ ] MAJOR: AI
  - [ ] MAJOR: Remote players
  - [ ] MAJOR: 3D rendering
  - [ ] MAJOR: Server-side Pong
  - [ ] MAJOR: User history and Matchmaking

- Minor modules (0.5 points each):
  - [x] MINOR: Frontend toolkit
  - [x] MINOR: Database
  - [x] MINOR: SSR
  - [x] MINOR: Translation
  - [ ] MINOR: User stats
  - [ ] MINOR: Game customization
