# SuSha

A multimodal ensemble learning prediction tool for microbial salinity adaptation based on genome-wide amino acid composition features.

## Installation

```bash
pip install .
```

## Usage

```bash
SuSha -i <input_fasta> -o <output_prefix>
```

### Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `-i`, `--input` | Yes | Input genome protein sequence file (.faa / .fasta) |
| `-o`, `--output` | Yes | Output Excel/TSV file prefix for prediction results and interpretation |

### Example

```bash
SuSha -i example.faa -o result
```

## Prediction Categories

| Category | Description |
|----------|-------------|
| 0 | Salt-sensitive (盐敏感) |
| 1 | Halotolerant (耐盐) |
| 2 | Slight halophilic (轻嗜盐) |
| 3 | Moderate halophilic (中嗜盐) |
| 4 | Extreme halophilic (极端嗜盐) |

## Features

- **24-dimensional amino acid composition features**: 20 individual amino acid ratios + 4 aggregated group ratios
- **Ensemble learning**: Combines ExtraTrees, RandomForest, Logistic Regression, and LDA classifiers
- **SHAP interpretability**: Provides feature contribution analysis for each prediction

## Dependencies

- numpy
- pandas
- scikit-learn
- biopython
- shap
- openpyxl
