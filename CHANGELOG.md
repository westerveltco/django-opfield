# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project attempts to adhere to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

<!--
## [${version}]
### Added - for new features
### Changed - for changes in existing functionality
### Deprecated - for soon-to-be removed features
### Removed - for now removed features
### Fixed - for any bug fixes
### Security - in case of vulnerabilities
[${version}]: https://github.com/westerveltco/django-opfield/releases/tag/v${version}
-->

## [Unreleased]

### Removed

- Dropped support for Python 3.8.

## [0.1.1]

### Changed

- Changed exception raised if `op` CLI not found to `RuntimeError`.

### Fixed

- Removed the passing in of just the `OP_SERVICE_ACCOUNT_TOKEN` variable to the `subprocess.run` call to `op`. This was clobbering the environment and causing configuration issues with the `op` CLI. First reported in [#12](https://github.com/westerveltco/django-opfield/issues/12) by [@joshuadavidthomas](https://github.com/joshuadavidthomas).

### New Contributors

- Jeff Triplett [@jefftriplett](https://github.com/jefftriplett) in [#13](https://github.com/westerveltco/django-opfield/pull/13)

## [0.1.0]

Initial release! 🎉

### Added

- A custom model field `OPField` for storing references to items in a 1Password vault.
- Store a reference to an item in the vault using the `op://` secret reference URI.
- Access the secret stored via a `<field_name>_secret` attribute on the model.
- Restrict which vaults can be used in the field to a list of vault names, passed in the `vaults` argument to the field.
- Explicitly set the name of the secret field in the model, via the `secret_name` argument to the field.
- A custom `OPURIValidator` class for validating 1Password URIs passed to the field.
- Initial application configuration options:
- `OP_COMMAND_TIMEOUT`: for setting the timeout for `op` commands, defaults to 5 seconds.
- `OP_CLI_PATH`: for setting the path to the `op` executable, defaults to using `shutil.which('op')`. If `op` is not found, an exception will be raised.
- `OP_SERVICE_ACCOUNT_TOKEN`: for setting the 1Password service account token, defaults to using the value of the `OP_SERVICE_ACCOUNT_TOKEN` environment variable. If not set, an exception will be raised.
- Initial documentation.
- Initial tests.
- Initial CI/CD.

### New Contributors

- Josh Thomas <josh@joshthomas.dev> (maintainer)

[unreleased]: https://github.com/westerveltco/django-opfield/compare/v0.1.1...HEAD
[0.1.0]: https://github.com/westerveltco/django-opfield/releases/tag/v0.1.0
[0.1.1]: https://github.com/westerveltco/django-opfield/releases/tag/v0.1.1
