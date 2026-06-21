import numpy as np

CRITERIA_TYPES = ['cost', 'benefit', 'benefit', 'benefit', 'benefit', 'benefit']

def calculate_topsis(smartphones, weights):
    """
    smartphones: list of dictionaries representing smartphones.
    weights: list of floats from AHP priority vector.
    """
    # 1. Decision Matrix
    # Order: Harga, Foto, Video, Chipset, Baterai, Storage
    matrix = []
    for sp in smartphones:
        matrix.append([
            sp['harga'],
            sp['foto'],
            sp['video'],
            sp['chipset'],
            sp['baterai'],
            sp['storage']
        ])
    
    mat = np.array(matrix, dtype=float)
    
    # 2. Normalized Matrix
    # Divide each column by sqrt(sum of squares of that column)
    col_sq_sums = np.sqrt(np.sum(mat**2, axis=0))
    norm_mat = mat / col_sq_sums
    
    # 3. Weighted Normalized Matrix
    weight_arr = np.array(weights, dtype=float)
    weighted_mat = norm_mat * weight_arr
    
    # 4. Ideal Best (A+) and Ideal Worst (A-)
    a_plus = []
    a_minus = []
    for j in range(len(CRITERIA_TYPES)):
        col = weighted_mat[:, j]
        if CRITERIA_TYPES[j] == 'benefit':
            a_plus.append(np.max(col))
            a_minus.append(np.min(col))
        else: # cost
            a_plus.append(np.min(col))
            a_minus.append(np.max(col))
            
    a_plus = np.array(a_plus)
    a_minus = np.array(a_minus)
    
    # 5. Separation Measures (D+ and D-)
    d_plus = np.sqrt(np.sum((weighted_mat - a_plus)**2, axis=1))
    d_minus = np.sqrt(np.sum((weighted_mat - a_minus)**2, axis=1))
    
    # 6. Performance Score
    # Add a small epsilon to avoid division by zero just in case
    c_score = d_minus / (d_plus + d_minus + 1e-10)
    
    # 7. Ranking
    # Add scores back to smartphones and sort
    results = []
    for i, sp in enumerate(smartphones):
        sp_copy = dict(sp)
        sp_copy['topsis_score'] = float(c_score[i])
        sp_copy['d_plus'] = float(d_plus[i])
        sp_copy['d_minus'] = float(d_minus[i])
        results.append(sp_copy)
        
    # Sort descending based on topsis_score
    results.sort(key=lambda x: x['topsis_score'], reverse=True)
    
    # Add rank
    for i, res in enumerate(results):
        res['rank'] = i + 1
        
    return {
        "decision_matrix": mat.tolist(),
        "normalized_matrix": norm_mat.tolist(),
        "weighted_matrix": weighted_mat.tolist(),
        "a_plus": a_plus.tolist(),
        "a_minus": a_minus.tolist(),
        "d_plus": d_plus.tolist(),
        "d_minus": d_minus.tolist(),
        "c_score": c_score.tolist(),
        "results": results
    }
