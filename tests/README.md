# DBreconnection Tests

This directory contains tests for the `/dbreconnect` Discord command.

## Test Files

1. **test_dbreconnection.py** - Unit tests with mocked dependencies
   - Tests cog initialization
   - Tests successful reconnection
   - Tests error handling
   - Tests updating other cogs with new connections

2. **test_dbreconnection_integration.py** - Integration tests
   - Tests actual database connections
   - Tests command registration
   - Requires database environment variables

3. **test_dbreconnection_manual.py** - Manual testing helper
   - Checks environment configuration
   - Simulates different connection scenarios
   - Provides testing instructions

## Running Tests

### Unit Tests
```bash
python -m pytest tests/test_dbreconnection.py -v
```

### Integration Tests
```bash
python tests/test_dbreconnection_integration.py
```

### Manual Test Helper
```bash
python tests/test_dbreconnection_manual.py
```

## Testing the Command in Discord

1. Start the bot:
   ```bash
   python InuiBot130.py
   ```

2. In Discord, use:
   ```
   /dbreconnect
   ```

3. Expected Results:
   - **Success**: ✅ 데이터베이스 재연결 성공!
   - **Failure**: 🐱 재연결 실패! 서버 관리자에게 문의하세요

## Environment Requirements

Create a `.env` file with:
```
DB_HOST=your_database_host
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_PORT=5432
DISCORD_TOKEN=your_discord_bot_token
```