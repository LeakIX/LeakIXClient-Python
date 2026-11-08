# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Infrastructure

- CI/tooling: adopt the common CI and tooling setup: coverage gate,
  pip-audit, TruffleHog secret scanning, zizmor workflow SAST with hardened
  workflows, CycloneDX SBOM, nox, and a mkdocs docs site; expand ruff and
  enable mypy strict on the library; bump all dependencies to their latest
  versions ([fde4aa5])
- CI: bump actions/setup-python 7.0.0 -> 7.1.0 ([d51343b], [#116])
- CI: bump actions/upload-artifact 4.6.2 -> 7.0.2 ([7d6e2f6], [#111])
- CI: bump astral-sh/setup-uv 7.6.0 -> 10.3.2 ([ff128ce], [#118])
- CI: bump trufflesecurity/trufflehog 3.96.0 -> 3.99.7 ([e904e24], [#119])
- CI: bump zizmorcore/zizmor-action 0.6.1 -> 0.8.0 ([414e6f6], [#117])
- Deps (dev): bump cyclonedx-bom 7.3.1 -> 7.6.0 ([0a94743], [#128])
- Deps (dev): bump hypothesis 6.161.6 -> 6.170.14 ([79fb133], [#125])
- Deps (dev): bump mkdocs-material 9.7.7 -> 9.8.0 ([c2477a7], [#121])
- Deps (dev): bump mypy 2.3.0 -> 2.4.1 ([3a86087], [#129])
- Deps (dev): bump nox 2026.7.11 -> 2026.10.20 ([c5ca040], [#122])
- Deps (dev): bump pytest 9.1.1 -> 9.2.0 ([1522206], [#127])
- Deps (dev): bump ruff 0.16.0 -> 0.17.3 ([b2f9444], [#124])
- Deps (dev): bump types-requests 2.33.0.20260712 -> 2.33.0.20261030
  ([e6f7ba6], [#126])
- Deps (dev): bump zizmor 1.28.0 -> 1.31.1 ([5f279b6], [#115])
- Deps: bump vulnerable transitive dependencies flagged by pip-audit
  (certifi, filelock, msgpack, pip, urllib3, virtualenv) ([42e0bc0], [#130])

## [1.1.0] - 2026-03-20

### Added

- Add `get_plugin(name)` method to fetch plugin description by name
  ([dbb4d57], [#85])

### Changed

- README: update PyPI badges and add supported Python versions
  ([d9e4bf8], [#84])

### Infrastructure

- CI: add PR hygiene checks using dannywillems/toolbox ([591c046], [#81])

## [1.0.0] - 2026-03-17

### Added

- AsyncClient with full async/await support using httpx
- Simple `search()` API accepting raw query strings
- `get_domain()` method for domain lookups
- Streaming `bulk_export_stream()` for memory-efficient exports
- `serialize_queries()` helper to reduce query serialization duplication
- Async example in `example/example_async_client.py`
- Add Python 3.11, 3.12, and 3.14 support ([d111628])

### Changed

- Use `__get` in both sync and async clients for uniform internal API
- Widen query type from `Query` to `AbstractQuery` to accept `RawQuery`
  directly
- Updated l9format requirement from =1.3.2 to =1.4.0 ([ae676d9])
- Updated l9format requirement from =1.4.0 to =2.0.0 ([df916e5], [#68])
- Updated l9format requirement from =2.0.0 to =2.0.1 ([5764b2f], [#74])
- Use explicit include lists instead of exclude lists for hatch build
  targets (sdist and wheel) in `pyproject.toml` ([aa9cc03], [#75])
- README: replace inline examples with links to `example/` directory
  ([01b280f], [#76])
- Add PyPI metadata: license, readme, classifiers, urls, keywords
  ([c62d2a4], [#78])

### Fixed

- Return `SuccessResponse` for HTTP 204 No Content instead of
  `ErrorResponse`

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
- Makefile: add `publish` and `publish-dry-run` targets ([87b68f6], [#80])

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

[unreleased]: https://github.com/LeakIX/LeakIXClient-Python/compare/v1.1.0...HEAD
[1.1.0]: https://github.com/LeakIX/LeakIXClient-Python/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/LeakIX/LeakIXClient-Python/compare/v0.1.10...v1.0.0
[0.1.10]: https://github.com/LeakIX/LeakIXClient-Python/compare/v0.1.9...v0.1.10
[0.1.9]: https://github.com/LeakIX/LeakIXClient-Python/releases/tag/v0.1.9

<!-- Commit links -->
[fde4aa5]: https://github.com/LeakIX/LeakIXClient-Python/commit/fde4aa5
[d51343b]: https://github.com/LeakIX/LeakIXClient-Python/commit/d51343b
[7d6e2f6]: https://github.com/LeakIX/LeakIXClient-Python/commit/7d6e2f6
[ff128ce]: https://github.com/LeakIX/LeakIXClient-Python/commit/ff128ce
[e904e24]: https://github.com/LeakIX/LeakIXClient-Python/commit/e904e24
[414e6f6]: https://github.com/LeakIX/LeakIXClient-Python/commit/414e6f6
[0a94743]: https://github.com/LeakIX/LeakIXClient-Python/commit/0a94743
[79fb133]: https://github.com/LeakIX/LeakIXClient-Python/commit/79fb133
[c2477a7]: https://github.com/LeakIX/LeakIXClient-Python/commit/c2477a7
[3a86087]: https://github.com/LeakIX/LeakIXClient-Python/commit/3a86087
[c5ca040]: https://github.com/LeakIX/LeakIXClient-Python/commit/c5ca040
[1522206]: https://github.com/LeakIX/LeakIXClient-Python/commit/1522206
[b2f9444]: https://github.com/LeakIX/LeakIXClient-Python/commit/b2f9444
[e6f7ba6]: https://github.com/LeakIX/LeakIXClient-Python/commit/e6f7ba6
[5f279b6]: https://github.com/LeakIX/LeakIXClient-Python/commit/5f279b6
[42e0bc0]: https://github.com/LeakIX/LeakIXClient-Python/commit/42e0bc0
[dbb4d57]: https://github.com/LeakIX/LeakIXClient-Python/commit/dbb4d57
[d9e4bf8]: https://github.com/LeakIX/LeakIXClient-Python/commit/d9e4bf8
[87b68f6]: https://github.com/LeakIX/LeakIXClient-Python/commit/87b68f6
[591c046]: https://github.com/LeakIX/LeakIXClient-Python/commit/591c046
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
[#130]: https://github.com/LeakIX/LeakIXClient-Python/pull/130
[#116]: https://github.com/LeakIX/LeakIXClient-Python/pull/116
[#111]: https://github.com/LeakIX/LeakIXClient-Python/pull/111
[#118]: https://github.com/LeakIX/LeakIXClient-Python/pull/118
[#119]: https://github.com/LeakIX/LeakIXClient-Python/pull/119
[#117]: https://github.com/LeakIX/LeakIXClient-Python/pull/117
[#128]: https://github.com/LeakIX/LeakIXClient-Python/pull/128
[#125]: https://github.com/LeakIX/LeakIXClient-Python/pull/125
[#121]: https://github.com/LeakIX/LeakIXClient-Python/pull/121
[#129]: https://github.com/LeakIX/LeakIXClient-Python/pull/129
[#122]: https://github.com/LeakIX/LeakIXClient-Python/pull/122
[#127]: https://github.com/LeakIX/LeakIXClient-Python/pull/127
[#124]: https://github.com/LeakIX/LeakIXClient-Python/pull/124
[#126]: https://github.com/LeakIX/LeakIXClient-Python/pull/126
[#115]: https://github.com/LeakIX/LeakIXClient-Python/pull/115
[#85]: https://github.com/LeakIX/LeakIXClient-Python/issues/85
[#84]: https://github.com/LeakIX/LeakIXClient-Python/issues/84
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
[#80]: https://github.com/LeakIX/LeakIXClient-Python/pull/80
[#81]: https://github.com/LeakIX/LeakIXClient-Python/issues/81
