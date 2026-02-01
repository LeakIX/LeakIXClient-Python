# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.10] - 2024-12-XX

### Changed

- Updated to Python 3.13+
  ([65c5121](https://github.com/LeakIX/LeakIXClient-Python/commit/65c5121))
- Updated l9format requirement from 1.3.1a3 to 1.3.2
  ([0975c1c](https://github.com/LeakIX/LeakIXClient-Python/commit/0975c1c))
- Updated fire requirement from ^0.5.0 to >=0.5,<0.8
  ([7cb5dae](https://github.com/LeakIX/LeakIXClient-Python/commit/7cb5dae))
- Bumped actions/setup-python from 5 to 6
  ([b1bc0da](https://github.com/LeakIX/LeakIXClient-Python/commit/b1bc0da))
- Bumped actions/checkout from 4 to 6
  ([6777ad9](https://github.com/LeakIX/LeakIXClient-Python/commit/6777ad9))

### Infrastructure

- Added pip-audit security scanning to CI
  ([62550bc](https://github.com/LeakIX/LeakIXClient-Python/commit/62550bc))
- Added Dependabot configuration for Python and GitHub Actions
  ([4dd4948](https://github.com/LeakIX/LeakIXClient-Python/commit/4dd4948))

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
