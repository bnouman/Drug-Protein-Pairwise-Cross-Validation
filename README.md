# Drug-Protein Interaction Prediction - CI Setup

This repository contains the implementation of cross-validation methods for protein-drug binding affinity prediction with automated Continuous Integration.

## 📁 Project Structure

```
.
├── .github/
│   └── workflows/
│       └── ci.yml                          # GitHub Actions CI workflow
├── Drug-Protein Interaction Prediction.ipynb  # Main notebook
├── input.data                              # Feature data
├── output.data                             # Affinity measurements
├── pairs.data                              # Protein-drug identifiers
├── test_cv_validation.py                   # Validation test script
├── requirements.txt                        # Python dependencies
└── README.md                               # This file
```

## 🚀 Setup Instructions

### 1. Initialize Git Repository (if not done)

```bash
git init
git add .
git commit -m "Initial commit: ML cross-validation with CI"
```

### 2. Create GitHub Repository

1. Go to [GitHub](https://github.com/new)
2. Create a new repository (don't initialize with README)
3. Copy the repository URL

### 3. Push to GitHub

```bash
git remote add origin https://github.com/bnouman/Drug-Protein-Pairwise-Cross-Validation.git
git branch -M main
git push -u origin main
```

### 4. CI Workflow Automatically Runs

Once pushed, GitHub Actions will automatically:
- ✓ Verify all data files exist
- ✓ Install Python 3.13 and dependencies
- ✓ Run validation tests
- ✓ Execute the notebook
- ✓ Check C-index calculations (LODO, LOPO, LOOPD)
- ✓ Generate test reports

## 🧪 What CI Tests

### Data Integrity Tests
- Verifies `input.data`, `output.data`, and `pairs.data` exist
- Checks 400 samples are present
- Validates 59 proteins and 77 drugs

### Cross-Validation Tests
- **LODO (Leave-One-Drug-Out)**: Expected C-index ~0.87
- **LOPO (Leave-One-Protein-Out)**: Expected C-index ~0.89
- **LOOPD (Leave-One-Protein-AND-Drug-Out)**: Expected C-index ~0.52

### Independence Tests
- Ensures test drugs don't appear in LODO training set
- Ensures test proteins don't appear in LOPO training set
- Ensures neither test protein nor drug appear in LOOPD training set

## 🔍 Viewing CI Results

1. Go to your GitHub repository
2. Click on the **Actions** tab
3. Select the latest workflow run
4. View detailed logs and test results

## 🏃 Running Tests Locally

```bash
# Install dependencies
pip install -r requirements.txt

# Run validation tests
python test_cv_validation.py

# Execute notebook
jupyter nbconvert --to notebook --execute "Drug-Protein Interaction Prediction.ipynb"
```

## 📊 Expected Results

| CV Method | C-index | What it tests |
|-----------|---------|---------------|
| Naive LOO | >0.90 | Incorrect (data leakage) |
| LODO | ~0.87 | New drug generalization |
| LOPO | ~0.89 | New protein generalization |
| LOOPD | ~0.52 | New drug + protein generalization |

## 🔧 CI Configuration

The CI workflow (`.github/workflows/ci.yml`) runs on:
- Every push to any branch
- All pull requests

To modify CI behavior, edit `.github/workflows/ci.yml`


## 👤 Author

Nouman Bashir - University of Turku 

Based on research by Professor Tapio Pahikkala: "Interaction Concordance Index: Performance Evaluation for Interaction Prediction Methods"

## 📄 License

MIT License - Feel free to use for research and educational purposes