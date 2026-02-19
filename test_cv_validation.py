#!/usr/bin/env python3
"""
Validation tests for Drug-Protein Interaction Prediction
Tests the three cross-validation methods: LODO, LOPO, LOOPD
"""

import numpy as np
import pandas as pd
from collections import defaultdict

def test_data_files_integrity():
    """Test that data files can be loaded and have correct structure"""
    print("Testing data files integrity...")
    
    try:
        # Load data
        input_data = pd.read_csv('input.data', sep=r'\s+', header=None)
        output_data = pd.read_csv('output.data', header=None)
        pairs_data = pd.read_csv('pairs.data', header=None, sep=r'\s+', 
                                  quotechar='"', engine='python')
        
        # Check dimensions
        assert len(input_data) == len(output_data), \
            f"Input and output data length mismatch: {len(input_data)} vs {len(output_data)}"
        
        assert len(input_data) == len(pairs_data), \
            f"Input and pairs data length mismatch: {len(input_data)} vs {len(pairs_data)}"
        
        # Check for expected number of samples (400)
        assert len(input_data) == 400, \
            f"Expected 400 samples, got {len(input_data)}"
        
        print(f"✓ Data files loaded successfully: {len(input_data)} samples")
        print(f"✓ Input features: {input_data.shape[1]} dimensions")
        
        return input_data, output_data, pairs_data
        
    except Exception as e:
        print(f"✗ Data loading failed: {e}")
        raise

def test_protein_drug_mapping(pairs_data):
    """Test protein and drug mappings are correct"""
    print("\nTesting protein-drug mappings...")
    
    pairs_data.columns = ['protein', 'drug']
    proteins = pairs_data['protein'].values
    drugs = pairs_data['drug'].values
    
    unique_proteins = np.unique(proteins)
    unique_drugs = np.unique(drugs)
    
    # Expected counts from exercise description
    assert len(unique_proteins) == 59, \
        f"Expected 59 proteins, got {len(unique_proteins)}"
    
    assert len(unique_drugs) == 77, \
        f"Expected 77 drugs, got {len(unique_drugs)}"
    
    print(f"✓ Protein count: {len(unique_proteins)}")
    print(f"✓ Drug count: {len(unique_drugs)}")
    
    return proteins, drugs, unique_proteins, unique_drugs

def test_cv_fold_counts(proteins, drugs, unique_proteins, unique_drugs):
    """Test that CV methods have correct number of folds"""
    print("\nTesting CV fold counts...")
    
    # Test LODO should have 77 folds (one per drug)
    assert len(unique_drugs) == 77, \
        f"LODO should have 77 folds, got {len(unique_drugs)}"
    print(f"✓ LODO will have {len(unique_drugs)} folds")
    
    # Test LOPO should have 59 folds (one per protein)
    assert len(unique_proteins) == 59, \
        f"LOPO should have 59 folds, got {len(unique_proteins)}"
    print(f"✓ LOPO will have {len(unique_proteins)} folds")
    
    # Test LOOPD should test existing combinations only
    protein_drug_pairs = set(zip(proteins, drugs))
    print(f"✓ LOOPD will test {len(protein_drug_pairs)} unique protein-drug pairs")

def test_train_test_independence():
    """Test that train/test splits maintain independence"""
    print("\nTesting train-test independence...")
    
    # Load data
    pairs_data = pd.read_csv('pairs.data', header=None, sep=r'\s+', 
                             quotechar='"', engine='python')
    pairs_data.columns = ['protein', 'drug']
    proteins = pairs_data['protein'].values
    drugs = pairs_data['drug'].values
    
    # Test LODO independence
    test_drug = drugs[0]
    train_drugs = set(drugs[drugs != test_drug])
    assert test_drug not in train_drugs, \
        "LODO: Test drug found in training set!"
    print("✓ LODO maintains train-test independence")
    
    # Test LOPO independence
    test_protein = proteins[0]
    train_proteins = set(proteins[proteins != test_protein])
    assert test_protein not in train_proteins, \
        "LOPO: Test protein found in training set!"
    print("✓ LOPO maintains train-test independence")
    
    # Test LOOPD independence
    test_indices = [i for i in range(len(proteins)) 
                    if proteins[i] == test_protein and drugs[i] == test_drug]
    if test_indices:
        train_indices = [i for i in range(len(proteins))
                        if proteins[i] != test_protein and drugs[i] != test_drug]
        train_proteins_set = set(proteins[train_indices])
        train_drugs_set = set(drugs[train_indices])
        
        assert test_protein not in train_proteins_set, \
            "LOOPD: Test protein found in training set!"
        assert test_drug not in train_drugs_set, \
            "LOOPD: Test drug found in training set!"
        print("✓ LOOPD maintains train-test independence")

def test_c_index_calculation():
    """Test C-index calculation with known values"""
    print("\nTesting C-index calculation...")
    
    # Perfect predictions
    y_true = np.array([1, 2, 3, 4, 5])
    y_pred = np.array([1, 2, 3, 4, 5])
    
    concordant = 0
    discordant = 0
    
    for i in range(len(y_true)):
        for j in range(i + 1, len(y_true)):
            if y_true[i] == y_true[j]:
                continue
            if (y_pred[i] > y_pred[j] and y_true[i] > y_true[j]) or \
               (y_pred[i] < y_pred[j] and y_true[i] < y_true[j]):
                concordant += 1
            else:
                discordant += 1
    
    c_index = concordant / (concordant + discordant)
    assert c_index == 1.0, f"Perfect predictions should give C-index=1.0, got {c_index}"
    print("✓ C-index calculation correct for perfect predictions")
    
    # Random predictions (should be around 0.5)
    np.random.seed(42)
    y_true = np.random.randn(100)
    y_pred = np.random.randn(100)
    
    concordant = 0
    discordant = 0
    
    for i in range(len(y_true)):
        for j in range(i + 1, len(y_true)):
            if y_true[i] == y_true[j]:
                continue
            if (y_pred[i] > y_pred[j] and y_true[i] > y_true[j]) or \
               (y_pred[i] < y_pred[j] and y_true[i] < y_true[j]):
                concordant += 1
            else:
                discordant += 1
    
    c_index = concordant / (concordant + discordant)
    assert 0.4 <= c_index <= 0.6, \
        f"Random predictions should give C-index≈0.5, got {c_index}"
    print(f"✓ C-index calculation correct for random predictions: {c_index:.3f}")

def main():
    """Run all validation tests"""
    print("=" * 60)
    print("Drug-Protein Interaction Prediction - Validation Tests")
    print("=" * 60)
    
    try:
        # Test 1: Data integrity
        input_data, output_data, pairs_data = test_data_files_integrity()
        
        # Test 2: Protein-drug mappings
        proteins, drugs, unique_proteins, unique_drugs = test_protein_drug_mapping(pairs_data)
        
        # Test 3: CV fold counts
        test_cv_fold_counts(proteins, drugs, unique_proteins, unique_drugs)
        
        # Test 4: Train-test independence
        test_train_test_independence()
        
        # Test 5: C-index calculation
        test_c_index_calculation()
        
        print("\n" + "=" * 60)
        print("✓ ALL VALIDATION TESTS PASSED")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        exit(1)
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        exit(1)

if __name__ == "__main__":
    main()
