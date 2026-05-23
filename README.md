# SuSha

**Version: v0.1**

A multimodal ensemble learning prediction tool for microbial salinity adaptation based on genome-wide amino acid composition features.

## Platform Support

| Platform | OS | Minimum RAM |
|----------|-----|-------------|
| x86_64 | Windows | 8 GB |
| x86_64 | Linux | 4 GB |

> **Coming Soon**: ARM for Linux and LoongArch for Linux support

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
| 0 | Salt-sensitive |
| 1 | Halotolerant |
| 2 | Slight halophilic |
| 3 | Moderate halophilic |
| 4 | Extreme halophilic |

## Features

- **24-dimensional amino acid composition features**: 20 individual amino acid ratios + 4 aggregated group ratios
- **Ensemble learning**: Combines ExtraTrees, RandomForest, Logistic Regression, and LDA classifiers
- **SHAP interpretability**: Provides feature contribution analysis for each prediction

## Dependencies

- numpy
- pandas
- scikit-learn
- imbalanced-learn
- biopython
- shap
- openpyxl

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
