# Overview

## Github Actions

Weekly update script...

## Update the Site

To update the site, create a PR of `prod <- main` and merge it.

## Local Testing

Run `http-server` from the parent directory of where this repo is located. You may need to turn off the local development server to update the cache.

## Jupyter Environment Creation

Create the virtual env:
`python -m venv /path/to/new/virtual/environment-name`

Activate the env:
`source <venv>/bin/activate`

Install ipykernel:
`pip install ipykernel`

Add environment as a kernel:
`python -m ipykernel install --user --name=myenv --display-name="Python (myenv)"`

Make sure to add the new jupyter kernel env to the gitignore!
