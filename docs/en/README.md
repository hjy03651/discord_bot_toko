# Toko Discord Bot

Toko is a Discord bot that provides various features including book management, event management, item storage, and more.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Commands](#commands)
- [Contributing](#contributing)
- [License](#license)

## Features

### 📚 Book Management (BookRetrieval)
- Book search and listing
- Book lending/returning system
- Add/edit/delete books
- Check lending status
- Search results with pagination

### 🎉 Event Management (Event)
- Event participant aggregation
- Winner drawing functionality
- Event statistics and management

### 📦 Item Storage (Saving)
- Item storage registration
- Storage deadline reminder (DM sent after 6 days)
- Item retrieval processing

### 🎮 Fun Features (ForFun)
- Word chain game
- Image processing features
- Various entertainment commands

### 🔧 Administrator Features (Sql)
- SQL query execution (admin only)
- Direct database management

## Requirements

- Python 3.13+
- PostgreSQL database
- Discord Bot token
- Required Python packages (see requirements.txt)

## Installation

1. Clone the repository
```bash
git clone https://github.com/yourusername/toko.git
cd toko
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Set up environment variables
Create a `.env` file and add the following:
```env
DISCORD_TOKEN=your_discord_bot_token
DB_HOST=your_database_host
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_PORT=5432
```

5. Database setup
Create a PostgreSQL database and set up the required tables.

## Usage

### Running the bot
```bash
python InuiBot130.py
```

### Running with Docker
```bash
docker build -t discord-bot-toko .
docker run --rm -d --name discord-bot-toko --env-file .env discord-bot-toko
```

## Commands

For a detailed list of commands, see [commands.md](commands.md).

### Main command examples
- `/list [book_name]` - Search books
- `/borrow [book_ID]` - Borrow a book
- `/return [book_ID]` - Return a book
- `/event [event_name] [number_of_winners]` - Event draw
- `/store [@user] [item]` - Register item storage

## Development

### Running tests
```bash
pytest tests/
```

### Code quality checks
```bash
# Run Flake8
flake8 .

# Run Pylint
pylint $(git ls-files '*.py')
```

## Deployment

Automatic deployment via GitHub Actions is configured. For more details, see [DEPLOY_SETUP.md](DEPLOY_SETUP.md).

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

[LICENSE](../../LICENSE)