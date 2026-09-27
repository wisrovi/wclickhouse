<p align="center">
  <a href="https://pypi.org/project/wclickhouse/"><img src="https://img.shields.io/pypi/v/wclickhouse?style=for-the-badge&logo=pypi&color=3b82f6" alt="PyPI version" /></a>
  <a href="https://pypi.org/project/wclickhouse/"><img src="https://img.shields.io/pypi/pyversions/wclickhouse.svg?style=for-the-badge&logo=python&color=3775A9" alt="Python versions" /></a>
  <a href="https://linkedin.com/in/wisrovi-rodriguez"><img src="https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="https://wisrovi.dev"><img src="https://img.shields.io/badge/Author-wisrovi.dev-111827?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Portal" /></a>
  <a href="https://orcid.org/0009-0005-0710-1861"><img src="https://img.shields.io/badge/ORCID-0009--0005--0710--1861-A6CE39?style=for-the-badge&logo=orcid&logoColor=white" alt="ORCID" /></a>
  <a href="https://opensource.org/licenses/MIT"><img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License" /></a>
</p>

# 🚀 WClickHouse — High-Performance ClickHouse ORM

A high-performance ClickHouse ORM for Python using **Pydantic v2**, **clickhouse-connect**, and **Apache Arrow**.

```mermaid
flowchart LR
    A["Python Objects / Pandas"] --> B["Pydantic v2 Schema Validation"]
    B --> C["WClickHouse Engine"]
    C --> D["Apache Arrow Columnar Buffer"]
    D --> E["ClickHouse OLAP Server"]
    style A fill:#1e293b,stroke:#3b82f6,color:#ffffff
    style B fill:#1e293b,stroke:#10b981,color:#ffffff
    style C fill:#1e293b,stroke:#f59e0b,color:#ffffff
    style D fill:#1e293b,stroke:#ec4899,color:#ffffff
    style E fill:#1e293b,stroke:#8b5cf6,color:#ffffff
```

## Features

- **Pydantic v2 Integration**: Define your ClickHouse tables as Pydantic models with full validation.
- **Apache Arrow Native**: High-speed binary columnar data exchange via `insert_arrow()` and `query_arrow()`.
- **Buffer Manager**: Automatic grouping of small inserts to protect server performance.
- **Query Streaming**: Process millions of rows with low memory footprint using lazy loading.
- **Auto-Sync**: Automatically creates tables and syncs schema (adds missing columns).
- **Dual API**: Full support for both **Synchronous** and **Asynchronous** operations.
- **OLAP Optimized**: Built-in support for bulk insertions and Pandas DataFrames.
- **LTS Version**: Enterprise-grade stability with 95% test coverage.

## Installation

```bash
pip install wclickhouse
```

## Quick Start

```python
from pydantic import BaseModel
from wclickhouse import WClickHouse
from datetime import datetime
from typing import List

# 1. Define your model
class AnalyticsEvent(BaseModel):
    event_id: int
    event_name: str
    properties: List[str]
    created_at: datetime = datetime.now()

# 2. Configure connection
db_config = {
    "host": "localhost",
    "port": 8124,
    "username": "default",
    "password": "test_pass",
    "database": "default"
}

# 3. Initialize (Auto-creates table)
db = WClickHouse(AnalyticsEvent, db_config)

# 4. Bulk Insert (High performance)
events = [
    AnalyticsEvent(event_id=1, event_name="login", properties=["web", "chrome"]),
    AnalyticsEvent(event_id=2, event_name="purchase", properties=["mobile", "ios"])
]
db.insert_many(events)

# 5. Query
results = db.get_all()
print(f"Total events: {len(results)}")
```

## Performance Note

ClickHouse is an OLAP database. For best performance:
1. Use **Apache Arrow** for massive ingestion (`insert_arrow`).
2. Enable the **Buffer Manager** for streaming small individual records.
3. Prefer `insert_many()` or `insert_dataframe()` over multiple `insert()` calls.

## Documentation

Full documentation available at [wclickhouse.readthedocs.io](https://wclickhouse.readthedocs.io/) and the interactive landing page `index.html`.

## License

MIT License

---

## 👤 Autor & Afiliación Oficial

* **William Steve Rodriguez Villamizar (Wisrovi)**
* **Cargo:** Principal AI Engineer & Applied AI Solutions Architect | Scientific Researcher
* 📧 **Email:** [wisrovi.rodriguez@gmail.com](mailto:wisrovi.rodriguez@gmail.com)
* 🌐 **Portal Oficial:** [wisrovi.dev](https://wisrovi.dev)
* 💼 **LinkedIn:** [wisrovi-rodriguez](https://www.linkedin.com/in/wisrovi-rodriguez/)
* 🆔 **ORCID:** [0009-0005-0710-1861](https://orcid.org/0009-0005-0710-1861)
* 📦 **PyPI:** [pypi.org/user/wisrovi/](https://pypi.org/user/wisrovi/)
* 🐙 **GitHub:** [@wisrovi](https://github.com/wisrovi)
