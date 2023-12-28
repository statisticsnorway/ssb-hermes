# SSB Hermes

[![PyPI](https://img.shields.io/pypi/v/ssb-hermes.svg)][pypi status]
[![Status](https://img.shields.io/pypi/status/ssb-hermes.svg)][pypi status]
[![Python Version](https://img.shields.io/pypi/pyversions/ssb-hermes)][pypi status]
[![License](https://img.shields.io/pypi/l/ssb-hermes)][license]

[![Documentation](https://github.com/statisticsnorway/ssb-hermes/actions/workflows/docs.yml/badge.svg)][documentation]
[![Tests](https://github.com/statisticsnorway/ssb-hermes/actions/workflows/tests.yml/badge.svg)][tests]
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=statisticsnorway_ssb-hermes&metric=coverage)][sonarcov]
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=statisticsnorway_ssb-hermes&metric=alert_status)][sonarquality]

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)][pre-commit]
[![Black](https://img.shields.io/badge/code%20style-black-000000.svg)][black]
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)][poetry]

[pypi status]: https://pypi.org/project/ssb-hermes/
[documentation]: https://statisticsnorway.github.io/ssb-hermes
[tests]: https://github.com/statisticsnorway/ssb-hermes/actions?workflow=Tests

[sonarcov]: https://sonarcloud.io/summary/overall?id=statisticsnorway_ssb-hermes
[sonarquality]: https://sonarcloud.io/summary/overall?id=statisticsnorway_ssb-hermes
[pre-commit]: https://github.com/pre-commit/pre-commit
[black]: https://github.com/psf/black
[poetry]: https://python-poetry.org/

## Features

Tool to match adress columns betwen to sources of data. Uses adresses and other geoprahical information like zip code. Enables you to use fuzzywuzzy on two datasets to match idents on street adress.

## Requirements

- pandas
- fuzzywuzzy
- levensthein

## Installation

You can install _SSB Hermes_ via [pip] from [PyPI]:

```console
pip install ssb-hermes
```

## Usage

Please see the [Reference Guide] for details.

## Contributing

Contributions are very welcome.
To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [GPL 3.0 license][license],
_SSB Hermes_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

## Credits

This project was generated from [Statistics Norway]'s [SSB PyPI Template].

[statistics norway]: https://www.ssb.no/en
[pypi]: https://pypi.org/
[ssb pypi template]: https://github.com/statisticsnorway/ssb-pypitemplate
[file an issue]: https://github.com/statisticsnorway/ssb-hermes/issues
[pip]: https://pip.pypa.io/

<!-- github-only -->

[license]: https://github.com/statisticsnorway/ssb-hermes/blob/main/LICENSE
[contributor guide]: https://github.com/statisticsnorway/ssb-hermes/blob/main/CONTRIBUTING.md
[reference guide]: https://statisticsnorway.github.io/ssb-hermes/reference.html
