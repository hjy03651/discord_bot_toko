# Docker Usage Guide

This guide explains how to run the Discord bot using Docker and Docker Compose.

## Prerequisites

- Docker installed on your system
- Docker Compose installed
- `.env` file configured with required environment variables

## Running with Docker

### Traditional Docker Commands

Build the image:
```bash
docker build -t discord-bot-toko .
```

Run the container:
```bash
docker run --rm -d --name discord-bot-toko --env-file .env discord-bot-toko
```

### Using Docker Compose (Recommended)

Start the bot:
```bash
docker-compose up -d
```

View logs:
```bash
docker-compose logs -f
```

Stop the bot:
```bash
docker-compose down
```

Rebuild and restart:
```bash
docker-compose up -d --build
```

## Environment Variables

Ensure your `.env` file contains:
```
DISCORD_TOKEN=your_discord_bot_token
DISCORD_APPID=your_discord_app_id
DB_HOST=your_database_host
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_PORT=5432
```

## Troubleshooting

1. **Container exits immediately**: Check logs with `docker-compose logs`
2. **Database connection fails**: Verify database credentials in `.env`
3. **Bot doesn't respond**: Ensure DISCORD_TOKEN is valid

## Development

For development with auto-restart on file changes:
```bash
docker-compose up
```

This runs in attached mode so you can see logs in real-time.