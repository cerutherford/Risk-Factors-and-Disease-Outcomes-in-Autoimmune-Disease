# SARD-ILD Codebase

This repository contains the code used to construct systemic autoimmune rheumatic disease (SARD) cohorts in the All of Us Research Program, identify interstitial lung disease (ILD) within those cohorts, generate descriptive summary tables, run logistic regression analyses, perform positive-control analyses, and produce figures.

The main analysis notebook for this repository is:

- `sard_ild_codebase.ipynb`

Additional figure scripts included in the repository are:

- `flowchart_clean.py`
- `regression_figure_bold.py`

## Overview

This codebase was developed for a thesis project examining ILD across multiple SARDs in the All of Us dataset. The workflow includes:

1. Construction of six SARD cohorts:
   - Rheumatoid arthritis (RA)
   - Systemic lupus erythematosus (SLE)
   - Systemic sclerosis (SSc)
   - Sjögren’s disease (SjD)
   - Idiopathic inflammatory myopathies/inflammatory myositis (IIM / IM)
   - Mixed connective tissue disease (MCTD)

2. Identification of SARD-ILD cohorts using:
   - a **loose/relaxed ILD definition**
   - a **strict ILD definition**

3. Generation of descriptive summary tables for:
   - the overall SARD cohort
   - the ILD sub-cohort
   - the SARD-noILD cohort
   - positive-control and negative-control cohorts

4. Logistic regression analyses evaluating associations between:
   - age
   - sex
   - smoking status  
   and SARD-ILD status

5. Positive-control analyses using:
   - idiopathic pulmonary fibrosis (IPF)
   - lung cancer

6. Creation of figures, including:
   - a cohort ascertainment flowchart
   - a regression forest plot

## Data source and computing environment

This project is designed to run in the **All of Us Researcher Workbench** using the OMOP-based All of Us Curated Data Repository (CDR) and BigQuery.

The notebook expects the environment variable:

- `WORKSPACE_CDR`

to be defined and to point to the appropriate All of Us dataset.

### Python dependencies

The notebook and figure scripts use Python packages including:

- `os`
- `re`
- `numpy`
- `pandas`
- `pandas_gbq`
- `scipy`
- `statsmodels`
- `matplotlib`

You will also need valid access to the All of Us Workbench / BigQuery environment to run the SQL queries in the notebook.

## Repository contents

### `sard_ild_codebase.ipynb`

This is the main end-to-end analysis notebook. It contains the full analytic pipeline, organized into the following major sections:

#### 1. Cohort construction
Builds SARD cohorts from diagnosis-code algorithms using non-standard source concepts expanded from cohort-builder criteria. The notebook includes helper functions for:

- expanding ICD-9/ICD-10 code roots to selectable source concept IDs
- defining inpatient vs outpatient logic
- requiring repeated diagnosis codes over specified time windows
- optionally requiring disease-specific medication exposure
- assembling disease-specific SQL queries and combining them into a full SARD cohort query

#### 2. Descriptive statistics and comparative analysis
Builds summary tables for the overall SARD cohort and ILD sub-cohorts. These tables include:

- age
- sex
- self-reported race
- smoking status
- pack-years
- immunosuppressive medication use
- ILD prevalence under loose and strict definitions

The notebook also constructs:

- a **SARD-ILD** summary table
- a **SARD-noILD** summary table
- comparison tables with p-values

#### 3. Logistic regression
Builds person-level datasets and runs unadjusted and multivariable logistic regression models for SARD-ILD status.

Primary predictors include:

- age (modeled per 10 years)
- male sex
- ever smoking

The adjusted models additionally account for overlapping SARD membership indicators.

#### 4. Positive-control analyses
Runs analogous descriptive and regression analyses for:

- IPF
- lung cancer

using strict negative controls defined as All of Us participants with no SARD, ILD, IPF, or lung cancer codes and evidence of EHR consent.

#### 5. Miscellaneous / supplementary analyses
Includes additional helper analyses such as:

- total number of All of Us participants
- missingness in smoking and pack-years variables
- overlap across SARD algorithms

## Disease definitions

The notebook implements disease-specific phenotyping algorithms for the following SARDs.

### RA
- At least 2 RA ICD-9/ICD-10 codes
- Codes at least 7 days apart
- At least 1 RA medication within 365 days after a qualifying RA code

### SLE
- At least 2 SLE ICD-9/ICD-10 codes
- Codes at least 30 days apart
- At least 1 SLE medication on or after a qualifying SLE code

### SSc
- Either:
  - at least 1 inpatient qualifying code, or
  - at least 2 outpatient qualifying codes at least 30 days apart

### SjD
- At least 2 qualifying codes
- Codes at least 28 days apart

### IIM / IM
- Either:
  - at least 1 inpatient qualifying code, or
  - at least 2 outpatient qualifying codes 30–365 days apart
- At least 1 qualifying medication within 365 days after qualifying code

### MCTD
- Either:
  - at least 1 inpatient qualifying code, or
  - at least 2 outpatient qualifying codes 30–365 days apart

## ILD definitions

The notebook uses two ILD definitions.

### Loose / relaxed ILD definition (used in thesis)
A participant is classified as ILD-positive if they have:

- at least 2 ILD-coded events
- separated by at least 30 days

### Strict ILD definition (not used in final thesis)
A stricter ILD phenotype is also constructed by combining ILD evidence with pulmonary function testing timing logic.

### SARD-noILD definition
For the primary comparison analyses, SARD-noILD participants are SARD cohort members with:

- **no ILD codes ever**

## Outputs

Running the notebook produces CSV exports for descriptive and regression tables. Filenames are timestamped.

Outputs include files such as:

- main SARD summary tables
- ILD summary tables
- SARD-noILD summary tables
- regression result tables
- positive-control regression tables

## Figures

### `flowchart_clean.py`
Creates a cohort ascertainment flowchart showing:

- total All of Us participants
- total SARD cohort
- disease-specific cohort counts
- disease-specific ILD vs non-ILD counts

It saves:

- `flowchart_final.png`
- `flowchart_final.pdf`

### `regression_figure_bold.py`
Creates a two-panel forest plot of unadjusted and multivariable-adjusted odds ratios for:

- age
- sex
- smoking

across the pooled SARD analysis and disease-specific analyses.

It saves:

- `forest_plot.eps`
- `forest_plot.pdf`
- `forest_plot.png`

## How to use

### Option 1: Run the full workflow
Open and run:

- `sard_ild_codebase.ipynb`

This is the main notebook and contains the full analysis pipeline from cohort construction through tables and regressions.

### Option 2: Generate figures only
Run one or both of:

- `python flowchart_clean.py`
- `python regression_figure_bold.py`

These scripts generate final figures independently of the notebook, using manually specified counts / results already embedded in the scripts.

## Important notes

- This code is intended for use within the **All of Us Researcher Workbench** environment.
- Access to the underlying data requires appropriate permissions and compliance with All of Us data-use policies.
- Some cell-count suppression logic is included in the summary-table workflow for small counts.
- Disease-specific cohorts are **not mutually exclusive**; participants may meet more than one SARD algorithm.
- Reproducing the notebook exactly may require the same CDR version, Workbench permissions, and access to the same survey / EHR tables used in the original project.

## Reproducibility

To maximize reproducibility:

1. Run the notebook in the All of Us Researcher Workbench.
2. Confirm that `WORKSPACE_CDR` points to the correct CDR.
3. Ensure Python packages are installed.
4. Run notebook cells in order.
5. Export tables and figures from the relevant sections.

## Citation / acknowledgment

If you use or adapt this code, please cite or acknowledge the associated thesis project and the All of Us Research Program as appropriate.

## Disclaimer

This repository is provided for research and reproducibility purposes. It is not intended for clinical decision-making. This README was written with the assistance of ChatGPT.
