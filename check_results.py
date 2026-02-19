#!/usr/bin/env python3
"""
Check C-index results from executed notebook
"""

import re
import sys

print("Validating C-index results...")

try:
    with open('executed_notebook.ipynb', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check for LODO C-index
    lodo_match = re.search(r'LODO-CV.*?([0-9]\.[0-9]+)', content, re.IGNORECASE | re.DOTALL)
    if lodo_match:
        lodo = float(lodo_match.group(1))
        print(f'✓ LODO C-index found: {lodo}')
        assert 0.5 <= lodo <= 1.0, f'LODO C-index out of range: {lodo}'
    else:
        print('⚠ LODO C-index not found in output')
    
    # Check for LOPO C-index
    lopo_match = re.search(r'LOPO-CV.*?([0-9]\.[0-9]+)', content, re.IGNORECASE | re.DOTALL)
    if lopo_match:
        lopo = float(lopo_match.group(1))
        print(f'✓ LOPO C-index found: {lopo}')
        assert 0.5 <= lopo <= 1.0, f'LOPO C-index out of range: {lopo}'
    else:
        print('⚠ LOPO C-index not found in output')
    
    # Check for LOOPD C-index
    loopd_match = re.search(r'LOOPD-CV.*?([0-9]\.[0-9]+)', content, re.IGNORECASE | re.DOTALL)
    if loopd_match:
        loopd = float(loopd_match.group(1))
        print(f'✓ LOOPD C-index found: {loopd}')
        assert 0.5 <= loopd <= 1.0, f'LOOPD C-index out of range: {loopd}'
    else:
        print('⚠ LOOPD C-index not found in output')
    
    print('✓ All C-index validations passed')
    sys.exit(0)

except FileNotFoundError:
    print('✗ executed_notebook.ipynb not found')
    sys.exit(1)
except Exception as e:
    print(f'✗ Error checking results: {e}')
    sys.exit(1)
