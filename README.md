## EIT Dashboard

Visualize and manipulate EIT in a code free way using the open source
[eitprocessing](https://github.com/EIT-ALIVE/eitprocessing) software.

**Important:** While the software code is open source, your data may not be. Once the dashboard is downloaded (and/or
updated) on your local machine, no online interaction is needed. Your data remains local and is not shared or uploaded by
this software.

| Badges             |                                                                                                                                                                                                                                                |
| :----------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| code repository    | [![github repo badge](https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue)](git@github.com:EIT-ALIVE/eit_dash)                                                                                             |
| license            | [![github license badge](https://img.shields.io/github/license/EIT-ALIVE/eit_dash)](git@github.com:EIT-ALIVE/eit_dash)                                                                                                                         |
| community registry | [![RSD](https://img.shields.io/badge/rsd-eit_dash-00a3e3.svg)](https://www.research-software.nl/software/eit_dash) [![workflow pypi badge](https://img.shields.io/pypi/v/eit_dash.svg?colorB=blue)](https://pypi.python.org/project/eit_dash/) |
| howfairis          | [![fair-software badge](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow)](https://fair-software.eu)                                                                |
| Documentation      | [![Documentation Status](https://readthedocs.org/projects/eit_dash/badge/?version=latest)](https://eit_dash.readthedocs.io/en/latest/?badge=latest)                                                                                            |

## Getting started

### 1. Installation

##### Install Poetry

EIT Dashboard uses of [poetry](https://python-poetry.org/) to easily manage the needed packages.
Poetry can be installed as follows. Please refer to the [official installation instructions](https://python-poetry.org/docs/#installation) if problems arise:

In Linux (and WSL) or macOS

```console
curl -sSL https://install.python-poetry.org | python3 -
```

Alternatively, you can use Homebrew in macOS:

```console
brew install poetry
```

In Windows (using PowerShell)

```console
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | py -
```

Alternatively, poetry can also be installed [using pip](https://pypi.org/project/poetry/) or [conda](https://anaconda.org/conda-forge/poetry) in a virtual environment of choice.

##### Install EIT Dashboard

The first time that the dashboard is used, the repository needs to be cloned and the needed dependencies have to be
installed by navigating to the path where it should be installed and running:

```console
git clone git@github.com:EIT-ALIVE/eit_dash.git
cd eit_dash
poetry install
```

### 2. Running EIT Dashboard

To run the most up top date version of the dashboard (including any updates since you last used it), navigate to the
folder where the dashboard is installed and run `bash RUN`. To run the dashboard without first updating to the lastest,
instead run `poetry run python eit_dash/main.py`. Next, open the link shown in a browser (generally something like `http://127.0.0.1:8050/`).

Note that while the dashboard should work on any browser, if you are experiencing issues we recommend switching to
Chrome or Firefox, as these are the browsers where we do most of the testing.

### 3. Using EIT Dashboard

Please see our [user manual](docs/user_manual.md) for instructions on how to use the dashboard.

## Contributing

If you want to contribute to the development of eit_dash,
have a look at the [contribution guidelines](CONTRIBUTING.md).

## License

This source code is licensed using a standard [Apache 2.0 License](LICENSE)

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [NLeSC/python-template](https://github.com/NLeSC/python-template).
