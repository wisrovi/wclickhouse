# Changelog - wclickhouse

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-04-13
### Added
- **LTS Release**: First stable long-term support version.
- **Apache Arrow Integration**: Native support for binary columnar ingestion via `insert_arrow()` and `query_arrow()`.
- **Buffer Manager**: Automatic batching of small insertions to maximize server throughput.
- **Query Streaming**: Memory-efficient lazy loading of records via `query_stream()`.
- **Pydantic v2 Core**: Full integration for schema definition and automatic validation.
- **Enhanced Type Mapping**: Support for `Enum`, `Decimal`, `Map`, `Array`, and `LowCardinality` types.
- **Health Checks**: Added `.ping()` and `.ping_async()` methods.
- **Dual API**: Complete synchronous and asynchronous support.
- **Documentation**: New premium landing page and 54+ production-ready examples.
- **Test Infrastructure**: Reorganized `docker/` and `test/` (Unit + Integration) directories.

### Changed
- Reorganized project structure from boilerplate esqueleto to enterprise-grade ORM.
- Updated default ports to `8124` (HTTP) and `9001` (TCP) to avoid local conflicts.

### Fixed
- Authentication issues with default ClickHouse user.
- ILLEGAL_FINAL errors by correctly setting up `ReplacingMergeTree` engines in examples.
- Pydantic validation errors during complex analytical aggregations.
