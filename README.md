## Badges

(Customize these badges with your own links, and check https://shields.io/ or https://badgen.net/ to see which other badges are available.)

| fair-software.eu recommendations | |
| :-- | :--  |
| (1/5) code repository              | [![github repo badge](https://img.shields.io/badge/github-repo-000.svg?logo=github&labelColor=gray&color=blue)](git@github.com:EIT-ALIVE/eit_dash) |
| (2/5) license                      | [![github license badge](https://img.shields.io/github/license/EIT-ALIVE/eit_dash)](git@github.com:EIT-ALIVE/eit_dash) |
| (3/5) community registry           | [![RSD](https://img.shields.io/badge/rsd-eit_dash-00a3e3.svg)](https://www.research-software.nl/software/eit_dash) [![workflow pypi badge](https://img.shields.io/pypi/v/eit_dash.svg?colorB=blue)](https://pypi.python.org/project/eit_dash/) |
| (4/5) citation                     | [![DOI](https://zenodo.org/badge/DOI/<replace-with-created-DOI>.svg)](https://doi.org/<replace-with-created-DOI>) |
| (5/5) checklist                    | [![workflow cii badge](https://bestpractices.coreinfrastructure.org/projects/<replace-with-created-project-identifier>/badge)](https://bestpractices.coreinfrastructure.org/projects/<replace-with-created-project-identifier>) |
| howfairis                          | [![fair-software badge](https://img.shields.io/badge/fair--software.eu-%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8F%20%20%E2%97%8B-yellow)](https://fair-software.eu) |
| Documentation                      | [![Documentation Status](https://readthedocs.org/projects/eit_dash/badge/?version=latest)](https://eit_dash.readthedocs.io/en/latest/?badge=latest) |


## Mockup

[mockup](https://github.com/EIT-ALIVE/eitprocessing/files/11480259/Proposal.GUI.mockup.pptx)

## How to use eit_dash

GUI to load and analyze image data from electrical impedance tomography (EIT)

The project setup is documented in [project_setup.md](project_setup.md). Feel free to remove this document (and/or the link to this document) if you don't need it.

## Getting started

### Installing Poetry

EIT Dashboard makes use of [poetry](https://python-poetry.org/) to easily manage the needed packages. 
`Poetry` can be installed both at system level following the [installation instructions](https://python-poetry.org/docs/#installation) (suggested) or by running:

```console
pip install poetry
```
in an environment with Python 3.10.

### Creating the virtual environment 

The first time that the dashboard is used, the needed dependencies have to be installed by running:

```console
poetry install
```

### Running the dashboard

Once the environment has been created, the dashboard can be run through:

```console
poetry run python eit_dash/main.py
```

## Installation

To install eit_dash from GitHub repository, do:

```console
git clone git@github.com:EIT-ALIVE/eit_dash.git
cd eit_dash
python3 -m pip install .
```

## Documentation

Include a link to your project's full documentation here.

## Contributing

If you want to contribute to the development of eit_dash,
have a look at the [contribution guidelines](CONTRIBUTING.md).

## Credits

This package was created with [Cookiecutter](https://github.com/audreyr/cookiecutter) and the [NLeSC/python-template](https://github.com/NLeSC/python-template).
