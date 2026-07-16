"""
NWLVH New Starter Progress Tracker Backend
A Flask-based API for tracking onboarding progress of new starters,
backed by a JSON file so data persists across server restarts.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime, date
import json
import os
import uuid

app = Flask(__name__)
CORS(app)

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'tracker_data.json')
PROBATION_WEEKS = 12

# Customize this to match your organization's exact onboarding policy.
CHECKLIST_TEMPLATE = [
    {
        'stage': 'Pre-Employment Checks',
        'items': [
            'Offer accepted & start date confirmed',
            'References received and verified',
            'DBS / background check cleared',
            'Occupational health clearance received',
            'Right to work verified',
            'Professional registration verified (NMC / HCPC / GMC, if applicable)'
        ]
    },
    {
        'stage': 'IT & Systems Access',
        'items': [
            'IT account & email created',
            'Clinical / EPR system access granted',
            'ID badge issued',
            'Building & door access configured',
            'Equipment issued (laptop, phone, uniform)'
        ]
    },
    {
        'stage': 'Day 1 Induction',
        'items': [
            'Welcome pack provided',
            'Site tour completed',
            'Introduced to team and key contacts',
            'Fire safety & emergency procedures briefing',
            'Uniform / PPE issued'
        ]
    },
    {
        'stage': 'Mandatory Training',
        'items': [
            'Fire safety training',
            'Safeguarding adults training',
            'Safeguarding children training',
            'Infection prevention & control training',
            'Moving and handling training',
            'Information governance & data security training',
            'Basic life support (BLS) / resuscitation training',
            'Equality, diversity & inclusion training'
        ]
    },
    {
        'stage': 'Local Induction & Orientation',
        'items': [
            'Department policies and procedures reviewed',
            'Health & safety orientation (local risks)',
            'Rota and shift pattern explained',
            'Shadowing shifts completed',
            'Key departmental contacts introduced'
        ]
    },
    {
        'stage': 'Clinical Supervision & Competency',
        'items': [
            'Clinical supervisor / mentor assigned',
            'First clinical supervision session held',
            'Preceptorship programme enrolled (if newly qualified)',
            'Core competency assessments completed',
            'Sign-off of competency framework'
        ]
    },
    {
        'stage': 'Probation Review Milestones',
        'items': [
            '4-week check-in completed',
            '12-week probation review completed',
            '6-month review completed (if applicable)',
            'Probation confirmed / passed'
        ]
    }
]


def build_checklist():
    return [
        {
            'stage': stage['stage'],
            'items': [
                {'id': str(uuid.uuid4())[:8], 'label': label, 'done': False, 'doneDate': None}
                for label in stage['items']
            ]
        }
        for stage in CHECKLIST_TEMPLATE
    ]


def load_starters():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, 'r') as f:
        return json.load(f)


def save_starters(starters):
    with open(DATA_FILE, 'w') as f:
        json.dump(starters, f, indent=2)


def compute_progress(starter):
    total = 0
    done = 0
    for stage in starter['checklist']:
        for item in stage['items']:
            total += 1
            if item['done']:
                done += 1
    return round((done / total) * 100) if total else 0


def compute_status(starter):
    progress = compute_progress(starter)
    if progress >= 100:
        return 'completed'

    start = date.fromisoformat(starter['startDate'])
    weeks_since_start = (date.today() - start).days / 7
    expected = min(100, max(0, (weeks_since_start / PROBATION_WEEKS) * 100))

    if weeks_since_start > 0 and progress < expected - 20:
        return 'at-risk'
    return 'in-progress'


def serialize(starter):
    data = dict(starter)
    data['progress'] = compute_progress(starter)
    data['status'] = compute_status(starter)
    return data


@app.route('/')
def home():
    return """
    <html>
    <head><title>NWLVH New Starter Progress Tracker</title></head>
    <body>
        <h1>NWLVH New Starter Progress Tracker API</h1>
        <p>This is the backend API. Use tracker.html for a fully standalone (offline) version,
        or point a frontend at these endpoints for shared/multi-user tracking.</p>
        <h2>Available Endpoints:</h2>
        <ul>
            <li>GET /starters - List all new starters (with computed progress/status)</li>
            <li>GET /starters/summary - Aggregate stats (totals, avg progress, at-risk count)</li>
            <li>POST /starters - Add a new starter</li>
            <li>GET /starters/&lt;id&gt; - Get a single starter</li>
            <li>PUT /starters/&lt;id&gt; - Update a starter's details</li>
            <li>PATCH /starters/&lt;id&gt;/checklist/&lt;item_id&gt; - Toggle a checklist item</li>
            <li>PUT /starters/&lt;id&gt;/notes - Update notes</li>
            <li>DELETE /starters/&lt;id&gt; - Remove a starter</li>
        </ul>
    </body>
    </html>
    """


@app.route('/starters', methods=['GET'])
def list_starters():
    starters = load_starters()
    return jsonify({'starters': [serialize(s) for s in starters]})


@app.route('/starters/summary', methods=['GET'])
def summary():
    starters = load_starters()
    total = len(starters)
    statuses = [compute_status(s) for s in starters]
    completed = statuses.count('completed')
    at_risk = statuses.count('at-risk')
    in_progress = total - completed - at_risk
    avg_progress = round(sum(compute_progress(s) for s in starters) / total) if total else 0

    return jsonify({
        'total': total,
        'inProgress': in_progress,
        'completed': completed,
        'atRisk': at_risk,
        'avgProgress': avg_progress
    })


@app.route('/starters', methods=['POST'])
def create_starter():
    data = request.get_json() or {}
    required = ['name', 'role', 'department', 'startDate']
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({'error': f"Missing required field(s): {', '.join(missing)}"}), 400

    starter = {
        'id': str(uuid.uuid4()),
        'name': data['name'],
        'role': data['role'],
        'department': data['department'],
        'startDate': data['startDate'],
        'supervisor': data.get('supervisor', ''),
        'notes': data.get('notes', ''),
        'checklist': build_checklist()
    }

    starters = load_starters()
    starters.append(starter)
    save_starters(starters)
    return jsonify(serialize(starter)), 201


@app.route('/starters/<starter_id>', methods=['GET'])
def get_starter(starter_id):
    starters = load_starters()
    starter = next((s for s in starters if s['id'] == starter_id), None)
    if not starter:
        return jsonify({'error': 'Starter not found'}), 404
    return jsonify(serialize(starter))


@app.route('/starters/<starter_id>', methods=['PUT'])
def update_starter(starter_id):
    data = request.get_json() or {}
    starters = load_starters()
    starter = next((s for s in starters if s['id'] == starter_id), None)
    if not starter:
        return jsonify({'error': 'Starter not found'}), 404

    for field in ['name', 'role', 'department', 'startDate', 'supervisor']:
        if field in data:
            starter[field] = data[field]

    save_starters(starters)
    return jsonify(serialize(starter))


@app.route('/starters/<starter_id>/checklist/<item_id>', methods=['PATCH'])
def toggle_checklist_item(starter_id, item_id):
    data = request.get_json() or {}
    done = bool(data.get('done', True))

    starters = load_starters()
    starter = next((s for s in starters if s['id'] == starter_id), None)
    if not starter:
        return jsonify({'error': 'Starter not found'}), 404

    found = False
    for stage in starter['checklist']:
        for item in stage['items']:
            if item['id'] == item_id:
                item['done'] = done
                item['doneDate'] = datetime.now().strftime('%Y-%m-%d') if done else None
                found = True

    if not found:
        return jsonify({'error': 'Checklist item not found'}), 404

    save_starters(starters)
    return jsonify(serialize(starter))


@app.route('/starters/<starter_id>/notes', methods=['PUT'])
def update_notes(starter_id):
    data = request.get_json() or {}
    starters = load_starters()
    starter = next((s for s in starters if s['id'] == starter_id), None)
    if not starter:
        return jsonify({'error': 'Starter not found'}), 404

    starter['notes'] = data.get('notes', '')
    save_starters(starters)
    return jsonify(serialize(starter))


@app.route('/starters/<starter_id>', methods=['DELETE'])
def delete_starter(starter_id):
    starters = load_starters()
    remaining = [s for s in starters if s['id'] != starter_id]
    if len(remaining) == len(starters):
        return jsonify({'error': 'Starter not found'}), 404

    save_starters(remaining)
    return jsonify({'message': 'Starter removed successfully'})


if __name__ == '__main__':
    print("Starting NWLVH New Starter Progress Tracker...")
    print("Access the API at http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
