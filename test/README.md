# Tests - wclickhouse

Unit and integration tests for the `wclickhouse` library.

## Structure

```
test/
├── README.md                # This file
├── unit/                    # Unit tests (Mocked)
│   └── test_basic.py        # Core repository & sync logic
└── integration/             # Integration tests (Real DB)
    ├── test_full_integration.py
    ├── test_async_coverage.py
    └── test_final_coverage.py
```

## Running Tests

### Setup Environment
First, ensure you have a running ClickHouse instance:
```bash
cd docker
docker-compose up -d
```

### Execute
```bash
# All tests
PYTHONPATH=src pytest test/ -v

# Only unit tests
PYTHONPATH=src pytest test/unit/ -v

# Only integration tests
PYTHONPATH=src pytest test/integration/ -v

# With Coverage (Goal: >95%)
PYTHONPATH=src pytest test/ --cov=wclickhouse --cov-report=term-missing
```

## Requirements
```bash
pip install -e ".[dev]"
```

## Author
**William Steve Rodriguez Villamizar** - [wisrovi](mailto:wisrovi.rodriguez@gmail.com)
