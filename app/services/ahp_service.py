import numpy as np

CRITERIA = ["Harga", "Foto", "Video", "Chipset", "Baterai", "Storage"]
RI_DICT = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}

def calculate_ahp(matrix):
    """
    matrix: 6x6 list of lists containing pairwise comparisons.
    Returns dictionary with all steps.
    """
    n = len(matrix)
    mat = np.array(matrix, dtype=float)
    
    # 1. Sum of each column
    col_sums = mat.sum(axis=0)
    
    # 2. Normalized Matrix
    norm_mat = mat / col_sums
    
    # 3. Priority Vector (Row Averages)
    priority_vector = norm_mat.mean(axis=1)
    
    # 4. Consistency Calculation
    # Ax = lambda_max * x
    # We can approximate lambda_max as sum of (col_sums * priority_vector)
    eigen_value = np.sum(col_sums * priority_vector)
    
    # 5. Consistency Index (CI)
    ci = (eigen_value - n) / (n - 1)
    
    # 6. Consistency Ratio (CR)
    ri = RI_DICT.get(n, 1.24)
    cr = ci / ri if ri != 0 else 0
    
    is_consistent = bool(cr < 0.1)
    
    return {
        "criteria": CRITERIA,
        "matrix": mat.tolist(),
        "col_sums": col_sums.tolist(),
        "normalized_matrix": norm_mat.tolist(),
        "priority_vector": priority_vector.tolist(),
        "eigen_value": float(eigen_value),
        "ci": float(ci),
        "cr": float(cr),
        "is_consistent": is_consistent
    }
