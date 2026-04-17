# Task from 0.0-etl.ipynb

Reusable ETL task checklist — apply these same steps when creating other ETL notebooks.

## Source

- File: `Dados Carregamento_24-25-26_RAMPs.xlsx`
- Location: `data/raw/`

## Transformations

1. **Convert datatype for each column** — ensure each column has the correct dtype (datetime, numeric, string).
2. **Filter dataframe by non-nan values from column `Taxa de Emissão PIER kg/h`** — drop rows where this column is NaN.

## Output

- Save processed dataframe as `.csv` in `data/processed/`.

## Steps

1. Load the raw Excel file with `pd.read_excel`.
2. Inspect schema with `df.info()`.
3. Convert datatypes per column (datetime first, then numeric, fallback to string).
4. Filter out rows with NaN in `Taxa de Emissão PIER kg/h`.
5. Validate the resulting shape and dtypes with `df.info()`.
6. Export the processed dataframe to `data/processed/*.csv`.
