# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- AsyncClient with full async/await support using httpx
- Simple `search()` API accepting raw query strings
- `get_domain()` method for domain lookups
- Streaming `bulk_export_stream()` for memory-efficient exports
- `serialize_queries()` helper to reduce query serialization duplication
- Async example in `example/example_async_client.py`

### Changed

- Use `__get` in both sync and async clients for uniform internal API
- Widen query type from `Query` to `AbstractQuery` to accept `RawQuery` directly
- Updated l9format requirement from =1.3.2 to =1.4.0 ([ae676d9])
- Updated l9format requirement from =1.4.0 to =2.0.0 ([df916e5], [#68])
- Updated l9format requirement from =2.0.0 to =2.0.1 ([5764b2f], [#74])
- Use explicit include lists instead of exclude lists for hatch build targets
  (sdist and wheel) in `pyproject.toml` ([aa9cc03], [#75])
- README: replace inline examples with links to `example/` directory
  ([01b280f], [#76])
- Add PyPI metadata: license, readme, classifiers, urls, keywords
  ([c62d2a4], [#78])

### Fixed

- Return `SuccessResponse` for HTTP 204 No Content instead of `ErrorResponse`

### Added

- Add Python 3.11, 3.12, and 3.14 support ([d111628])

### Removed

- Removed dependency on serde (unmaintained), replaced with dataclasses
  and l9format.l9format.Model ([df916e5], [#68])

### Infrastructure

- CI: use Makefile targets in Windows job and add sequential per-commit
  testing triggered by the ci:per-commit label ([3967e42], [#66])
- Remove duplicated lint-shell target in Makefile ([a652654], [#67])
- Add mypy type checking to CI workflow ([6b9a3db], [#42])
- Bump astral-sh/setup-uv from 6 to 7 ([cfa8b6c], [#72])
- Migrate from Poetry to uv ([14bc55e], [#65])

## [0.1.10] - 2024-12-XX

### Changed

- Updated to Python 3.13+ ([65c5121])
- Updated l9format requirement from 1.3.1a3 to 1.3.2 ([0975c1c])
- Updated fire requirement from ^0.5.0 to >=0.5,<0.8 ([7cb5dae])
- Bumped actions/setup-python from 5 to 6 ([b1bc0da])
- Bumped actions/checkout from 4 to 6 ([6777ad9])

### Infrastructure

- Added pip-audit security scanning to CI ([62550bc])
- Added Dependabot configuration for Python and GitHub Actions
  ([4dd4948])

## [0.1.9] - Previous Release

### Added

- Initial documented release
- Python client for LeakIX API
- Support for service and leak queries
- Host lookup by IPv4
- Plugin listing for authenticated users
- Subdomain queries
- Bulk export functionality
- Query building with MustQuery, MustNotQuery, ShouldQuery
- Field filters: TimeField, PluginField, IPField, PortField, CountryField

[unreleased]: https://github.com/LeakIX/LeakIXClient-Python/compare/v0.1.10...HEAD
[0.1.10]: https://github.com/LeakIX/LeakIXClient-Python/compare/v0.1.9...v0.1.10
[0.1.9]: https://github.com/LeakIX/LeakIXClient-Python/releases/tag/v0.1.9

<!-- Commit links -->
[c62d2a4]: https://github.com/LeakIX/LeakIXClient-Python/commit/c62d2a4
[01b280f]: https://github.com/LeakIX/LeakIXClient-Python/commit/01b280f
[aa9cc03]: https://github.com/LeakIX/LeakIXClient-Python/commit/aa9cc03
[5764b2f]: https://github.com/LeakIX/LeakIXClient-Python/commit/5764b2f
[cfa8b6c]: https://github.com/LeakIX/LeakIXClient-Python/commit/cfa8b6c
[6b9a3db]: https://github.com/LeakIX/LeakIXClient-Python/commit/6b9a3db
[d111628]: https://github.com/LeakIX/LeakIXClient-Python/commit/d111628
[df916e5]: https://github.com/LeakIX/LeakIXClient-Python/commit/df916e5
[14bc55e]: https://github.com/LeakIX/LeakIXClient-Python/commit/14bc55e
[a652654]: https://github.com/LeakIX/LeakIXClient-Python/commit/a652654
[3967e42]: https://github.com/LeakIX/LeakIXClient-Python/commit/3967e42
[ae676d9]: https://github.com/LeakIX/LeakIXClient-Python/commit/ae676d9
[65c5121]: https://github.com/LeakIX/LeakIXClient-Python/commit/65c5121
[0975c1c]: https://github.com/LeakIX/LeakIXClient-Python/commit/0975c1c
[7cb5dae]: https://github.com/LeakIX/LeakIXClient-Python/commit/7cb5dae
[b1bc0da]: https://github.com/LeakIX/LeakIXClient-Python/commit/b1bc0da
[6777ad9]: https://github.com/LeakIX/LeakIXClient-Python/commit/6777ad9
[62550bc]: https://github.com/LeakIX/LeakIXClient-Python/commit/62550bc
[4dd4948]: https://github.com/LeakIX/LeakIXClient-Python/commit/4dd4948

<!-- PR links -->
[#66]: https://github.com/LeakIX/LeakIXClient-Python/pull/66
[#65]: https://github.com/LeakIX/LeakIXClient-Python/issues/65
[#67]: https://github.com/LeakIX/LeakIXClient-Python/issues/67
[#42]: https://github.com/LeakIX/LeakIXClient-Python/issues/42
[#68]: https://github.com/LeakIX/LeakIXClient-Python/pull/68
[#72]: https://github.com/LeakIX/LeakIXClient-Python/pull/72
[#74]: https://github.com/LeakIX/LeakIXClient-Python/pull/74
[#75]: https://github.com/LeakIX/LeakIXClient-Python/pull/75
[#76]: https://github.com/LeakIX/LeakIXClient-Python/pull/76
[#78]: https://github.com/LeakIX/LeakIXClient-Python/pull/78
