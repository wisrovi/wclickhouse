# Docker Environment - wclickhouse

Infrastructure for local development and testing of `wclickhouse`.

## Services

This project uses **ClickHouse** as the primary database engine.

### ClickHouse Server
- **Image**: `clickhouse/clickhouse-server:latest`
- **HTTP Port**: `8124` (mapped from 8123)
- **TCP Port**: `9001` (mapped from 9000)
- **Database**: `test_db`
- **User**: `default`
- **Password**: `test_pass`

## Usage

### Start Environment
```bash
docker-compose up -d
```

### Stop Environment
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f
```

## Troubleshooting

If the ports `8124` or `9001` are already in use, you can modify them in `docker-compose.yml`. Remember to update your `db_config` in your Python scripts accordingly.
