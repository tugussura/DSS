from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.smartphone import Smartphone
from app.services.ahp_service import calculate_ahp, CRITERIA
from app.services.topsis_service import calculate_topsis
import json

dss_bp = Blueprint('dss', __name__)

PRESETS = {
    'tiktok': {
        # 0:Harga, 1:Foto, 2:Video, 3:Chipset, 4:Baterai, 5:Storage
        # Harga vs others (Harga is very low priority)
        'v_0_1': '1/7', 'v_0_2': '1/7', 'v_0_3': '1/5', 'v_0_4': '1/3', 'v_0_5': '1/5',
        # Foto vs others
        'v_1_2': '3', 'v_1_3': '5', 'v_1_4': '5', 'v_1_5': '5',
        # Video vs others
        'v_2_3': '3', 'v_2_4': '5', 'v_2_5': '3',
        # Chipset vs others
        'v_3_4': '3', 'v_3_5': '1',
        # Baterai vs Storage
        'v_4_5': '1/3'
    },
    'youtube': {
        # Priority: 1. Video, 2. Storage, 3. Chipset, 4. Foto, 5. Baterai, 6. Harga
        'v_0_1': '1/4', 'v_0_2': '1/9', 'v_0_3': '1/6', 'v_0_4': '1/2', 'v_0_5': '1/8',
        'v_1_2': '1/3', 'v_1_3': '1/2', 'v_1_4': '2', 'v_1_5': '1/2',
        'v_2_3': '2', 'v_2_4': '5', 'v_2_5': '2',
        'v_3_4': '3', 'v_3_5': '1',
        'v_4_5': '1/4'
    },
    'mobile_film': {
        # Priority: 1. Video, 2. Foto, 3. Chipset, 4. Storage, 5. Baterai, 6. Harga
        'v_0_1': '1/7', 'v_0_2': '1/9', 'v_0_3': '1/5', 'v_0_4': '1/3', 'v_0_5': '1/5',
        'v_1_2': '1/3', 'v_1_3': '3', 'v_1_4': '5', 'v_1_5': '3',
        'v_2_3': '5', 'v_2_4': '7', 'v_2_5': '5',
        'v_3_4': '3', 'v_3_5': '1',
        'v_4_5': '1/3'
    },
    'budget': {
        # Priority: 1. Harga, 2. Foto, 3. Video, 4. Baterai, 5. Chipset, 6. Storage
        'v_0_1': '3', 'v_0_2': '3', 'v_0_3': '5', 'v_0_4': '5', 'v_0_5': '7',
        'v_1_2': '1', 'v_1_3': '3', 'v_1_4': '3', 'v_1_5': '5',
        'v_2_3': '3', 'v_2_4': '3', 'v_2_5': '5',
        'v_3_4': '1', 'v_3_5': '3',
        'v_4_5': '3'
    },
    'custom': {
        # All equal
        'v_0_1': '1', 'v_0_2': '1', 'v_0_3': '1', 'v_0_4': '1', 'v_0_5': '1',
        'v_1_2': '1', 'v_1_3': '1', 'v_1_4': '1', 'v_1_5': '1',
        'v_2_3': '1', 'v_2_4': '1', 'v_2_5': '1',
        'v_3_4': '1', 'v_3_5': '1',
        'v_4_5': '1'
    }
}

def parse_fraction(val_str):
    if '/' in val_str:
        num, den = val_str.split('/')
        return float(num) / float(den)
    return float(val_str)

@dss_bp.route('/step1', methods=['GET', 'POST'])
def step1():
    if request.method == 'POST':
        profile = request.form.get('profile', 'custom')
        session['profile'] = profile
        return redirect(url_for('dss.step2'))
    return render_template('recommendation/step1_profile.html')

@dss_bp.route('/step2', methods=['GET', 'POST'])
def step2():
    profile = session.get('profile', 'custom')
    presets = PRESETS.get(profile, PRESETS['custom'])
    
    # If user submits the form
    if request.method == 'POST':
        matrix = [[1.0 for _ in range(6)] for _ in range(6)]
        
        # We need to fill the upper and lower triangles
        for i in range(6):
            for j in range(i+1, 6):
                key = f'v_{i}_{j}'
                val_str = request.form.get(key, '1')
                val = parse_fraction(val_str)
                matrix[i][j] = val
                matrix[j][i] = 1.0 / val
                
        # Calculate AHP
        ahp_result = calculate_ahp(matrix)
        session['ahp_result'] = ahp_result
        return redirect(url_for('dss.step3'))
        
    return render_template('recommendation/step2_ahp.html', presets=presets, criteria=CRITERIA)

@dss_bp.route('/step3', methods=['GET'])
def step3():
    ahp_result = session.get('ahp_result')
    if not ahp_result:
        return redirect(url_for('dss.step2'))
    return render_template('recommendation/step3_validation.html', ahp_result=ahp_result)

@dss_bp.route('/step4', methods=['GET'])
def step4():
    ahp_result = session.get('ahp_result')
    if not ahp_result or not ahp_result['is_consistent']:
        flash('Lakukan proses AHP yang konsisten terlebih dahulu.', 'warning')
        return redirect(url_for('dss.step2'))
        
    # Run TOPSIS
    smartphones = [s.to_dict() for s in Smartphone.query.all()]
    if not smartphones:
        flash('Data smartphone kosong.', 'danger')
        return redirect(url_for('main.dashboard'))
        
    weights = ahp_result['priority_vector']
    topsis_result = calculate_topsis(smartphones, weights)
    
    return render_template('recommendation/step4_result.html', 
                           top_smartphone=topsis_result['results'][0], 
                           results=topsis_result['results'],
                           criteria=CRITERIA,
                           weights=weights)

@dss_bp.route('/analysis', methods=['GET'])
def analysis():
    ahp_result = session.get('ahp_result')
    
    if not ahp_result or not ahp_result['is_consistent']:
        flash('Silakan selesaikan proses perhitungan AHP terlebih dahulu untuk melihat analisis.', 'warning')
        return redirect(url_for('dss.step1'))
        
    smartphones = [s.to_dict() for s in Smartphone.query.all()]
    weights = ahp_result['priority_vector']
    topsis_result = calculate_topsis(smartphones, weights)
        
    return render_template('analysis.html', 
                           criteria=CRITERIA,
                           weights=weights,
                           results=topsis_result['results'])

@dss_bp.route('/calculation_details', methods=['GET'])
def calculation_details():
    ahp_result = session.get('ahp_result')
    
    if not ahp_result or not ahp_result['is_consistent']:
        flash('Silakan selesaikan proses perhitungan AHP terlebih dahulu untuk melihat detail perhitungan.', 'warning')
        return redirect(url_for('dss.step1'))
        
    smartphones = [s.to_dict() for s in Smartphone.query.all()]
    weights = ahp_result['priority_vector']
    topsis_full_result = calculate_topsis(smartphones, weights)
        
    return render_template('calculation_details.html', 
                           ahp=ahp_result, 
                           topsis=topsis_full_result,
                           smartphones=[s['nama'] for s in smartphones],
                           criteria=CRITERIA)
