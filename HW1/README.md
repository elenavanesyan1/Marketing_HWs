# AirPods Pro 3 Bass Diffusion Project

This repository contains the Python code, historical AirPods sales data, and final report used for the Bass diffusion analysis of Apple AirPods Pro 3.

## Project Structure

```text
HW1/
│
├── code/
    └── analysis.ipynb
├── data/
│   └── airpods_sales.csv
├── img/
│   └── 1.png
│   └── 2.png
│   └── 3.png
|   └── 4.png
├── report/
│   ├── report_source.md
│   └── report.pdf
├── references/
│   └── references.md
└── README.md
```

## How to Run the Analysis

The analysis is implemented in Python using a Jupyter Notebook.

### 1. Install the Required Packages

The notebook uses the following Python libraries:

```text
pandas
numpy
matplotlib
scipy
```

If they are not already installed, run:

```bash
pip install pandas numpy matplotlib scipy
```

### 2. Open the Notebook

Open:

```text
analysis.ipynb
```

using VS Code, Jupyter Notebook, or JupyterLab.

Make sure a Python kernel with the required packages is selected.

### 3. Data File

The historical AirPods sales dataset should be stored at:

```text
data/airpods_sales_2017_2025.csv
```

The notebook should load the dataset using a relative path, for example:

```python
sales = pd.read_csv("data/airpods_sales_2017_2025.csv")
```

This allows the notebook to run correctly after the repository is downloaded or cloned.

### 4. Run the Notebook

Run all notebook cells from top to bottom.

The notebook:

1. loads the historical AirPods sales data;
2. prepares the time and cumulative sales variables;
3. defines the Bass diffusion function;
4. estimates the Bass parameters using nonlinear least squares;
5. calculates fitted historical sales;
6. uses the estimated diffusion parameters to forecast AirPods Pro 3 adoption;
7. creates the forecast table and visualizations.

## Bass Model Estimation

The Bass parameters are estimated using:

```python
scipy.optimize.curve_fit
```

The estimated parameters are:

```text
m = market potential
p = coefficient of innovation
q = coefficient of imitation
```

## AirPods Pro 3 Forecast

For the AirPods Pro 3 forecast, the historical estimates of `p` and `q` are reused.

The market potential for AirPods Pro 3 is set separately in the notebook as:

```python
m = 500
```

The value is measured in millions of units.

The forecast begins in 2026 and covers 15 years.

## Outputs

Running the notebook produces:

- estimated Bass model parameters;
- predicted historical AirPods sales;
- annual AirPods Pro 3 adoption estimates;
- cumulative adoption estimates;
- visualizations used in the final report.

The final report is available at:

```text
report/report.pdf
```
