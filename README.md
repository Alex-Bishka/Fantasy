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

## Articles on Deck:

- [ ] 2023 review series
    - [ ] Wide receiver 2023 review
    - [ ] Tight end 2023 review
    - [ ] Running back 2023 review
- [ ] Modeling Explorations
    - [ ] Modeling running backs re-write
    - [ ] Modeling wide receivers re-write
    - [ ] Modeling tight ends
    - [ ] Modeling quarterbacks
- [ ] Revisit per-game sticky stats?
    - [ ] RBs
    - [ ] WRs
    - [ ] TEs
- [ ] College modeling exploration
    - [ ] QBs
    - [ ] RBs
    - [ ] WRs
    - [ ] TEs
- [ ] Individual player reviews?
- [ ] Buys/Sells?
- [ ] 


## Tooling/Site Upgrades on Deck:

- [ ] Re-write clustering notebook
- [ ] Improve ML re-usability
    - [ ] Create modeling pipeline
    - [ ] Create data pipeline
- [ ] Grab college data
    - [ ] Stats for college teams
    - [ ] Combine numbers
    - [ ] Draft picks/order
- [ ] S3 buckets for CSV data?
- [ ] PCA analysis when?
- [ ] Computer vision when?
- [ ] 


## Site Features on Deck:

- [ ] Re-write/tool data bank
    - [ ] Every year we have?
    - [ ] Easier to select items
- [ ] Player comparison
    - [ ] By NFL/Fantasy season
    - [ ] By NFL/Fantasy career
    - [ ] By college production
    - [ ] By measurables (i.e. combine)
    - [ ] By draft order
- [ ] Design overhual?
- [ ] Dates to articles?
- [ ] 