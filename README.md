# Vault Consumption Counter

This repository provides various methods for generating data to understand Vault consumption.

## Description

The project includes different scripts to analyze and understand the consumption patterns of Vault. Each folder contains scripts designed to generate and handle data specific to Vault consumption.

## Prerequisites

Before running the scripts, ensure you have the necessary Vault environment parameters set:

```bash
export VAULT_ADDR=http://localhost2
export VAULT_NAMESPACE=admin
export VAULT_TOKEN=hunter2
```
## Folder Structure

    * Bash: Contains scripts written in Bash.
    * Jupyter: Contains Jupyter notebooks for data analysis.
    * Python: Contains Python scripts for generating data.
    * Testing: Contains test scripts and files.

**doesnt yet work for HCP Vault because activity/export API endpoint is only available form root namespace.**
    
this is a community project and not supported by Hashicorp. PRs welcomed.
