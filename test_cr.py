import numpy as np

RI_DICT = {1: 0, 2: 0, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}

def parse_fraction(val_str):
    if '/' in val_str:
        num, den = val_str.split('/')
        return float(num) / float(den)
    return float(val_str)

def check_cr(preset):
    matrix = [[1.0 for _ in range(6)] for _ in range(6)]
    for i in range(6):
        for j in range(i+1, 6):
            key = f'v_{i}_{j}'
            val_str = preset.get(key, '1')
            val = parse_fraction(val_str)
            matrix[i][j] = val
            matrix[j][i] = 1.0 / val
            
    mat = np.array(matrix, dtype=float)
    col_sums = mat.sum(axis=0)
    norm_mat = mat / col_sums
    priority_vector = norm_mat.mean(axis=1)
    eigen_value = np.sum(col_sums * priority_vector)
    n = 6
    ci = (eigen_value - n) / (n - 1)
    ri = RI_DICT.get(n, 1.24)
    cr = ci / ri if ri != 0 else 0
    return cr

youtube_preset_3 = {
    'v_0_1': '1/4', 'v_0_2': '1/9', 'v_0_3': '1/6', 'v_0_4': '1/2', 'v_0_5': '1/8',
    'v_1_2': '1/3', 'v_1_3': '1/2', 'v_1_4': '2', 'v_1_5': '1/2',
    'v_2_3': '2', 'v_2_4': '5', 'v_2_5': '2', # Changed from 1 to 2
    'v_3_4': '3', 'v_3_5': '1',
    'v_4_5': '1/4'
}

print(f"New CR 3: {check_cr(youtube_preset_3)}")
