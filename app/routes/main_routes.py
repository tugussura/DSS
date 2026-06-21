from flask import Blueprint, render_template, session
from app.models.smartphone import Smartphone
from app.services.ahp_service import calculate_ahp
from app.services.topsis_service import calculate_topsis

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def dashboard():
    total_smartphones = Smartphone.query.count()
    total_criteria = 6
    
    top_smartphones = []
    avg_topsis_score = 0
    ahp_data = None
    all_smartphones_results = []
    if total_smartphones > 0:
        smartphones = [s.to_dict() for s in Smartphone.query.all()]
        ahp_result = session.get('ahp_result')
        
        if ahp_result and ahp_result.get('is_consistent'):
            weights = ahp_result['priority_vector']
            ahp_data = ahp_result
        else:
            weights = [1/6] * 6
            
        topsis_result = calculate_topsis(smartphones, weights)
        all_smartphones_results = topsis_result['results']
        top_smartphones = all_smartphones_results[:3]
        
        if len(all_smartphones_results) > 0:
            avg_topsis_score = sum([s['topsis_score'] for s in all_smartphones_results]) / len(all_smartphones_results)
            
    return render_template('dashboard.html', 
                           total_smartphones=total_smartphones, 
                           total_criteria=total_criteria,
                           top_smartphones=top_smartphones,
                           avg_topsis_score=avg_topsis_score,
                           ahp_data=ahp_data,
                           all_smartphones_results=all_smartphones_results)
