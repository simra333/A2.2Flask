from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from logger import database
from logger.flow_handler import FlowHandler
from logger.feature_flags import feature_flags

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Display the home page with basic app info"""
    if request.method == 'POST':
        # Handle form submission
        task_content = request.form['content']
        # Add your logic to process the form data
        return redirect('/')
    else:
        return render_template('index.html')

# API endpoint for solutions
@app.route('/api/solutions', methods=['GET'])
def get_solutions():
    conn = database.get_connection()
    # Use your existing database query function
    solutions = get_all_solutions_for_api(conn)
    conn.close()
    return jsonify(solutions)

def get_all_solutions_for_api(conn):
    """Get all solutions in a format suitable for API response"""
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, description FROM solutions")
    solutions = [{"id": row[0], "name": row[1], "description": row[2]} for row in cursor.fetchall()]
    return solutions

# API endpoint for flows in a specific solution
@app.route('/api/solutions/<int:solution_id>/flows', methods=['GET'])
def get_solution_flows(solution_id):
    conn = database.get_connection()
    try:
        # Pass the connection to the function
        flows = get_flows_by_solution_for_api(conn, solution_id)
        return jsonify(flows)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

def get_flows_by_solution_for_api(conn, solution_id):
    """Get flows for a specific solution in a format suitable for API response"""
    cursor = conn.cursor()

    # Use the known columns names from the flows table based on FlowHandler
    query = """
        SELECT id, title as name, description, solution_id, status, priority, assigned_id, creator_id, created_at, updated_at
        FROM flows
        WHERE solution_id = ?
    """

    cursor.execute(query, (solution_id,))
    
    # Map the results to dictionaries
    columns = [description[0] for description in cursor.description]
    flows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    # Get solution name and developer names for better context
    if flows:
        # Get solution name
        cursor.execute("SELECT name FROM solutions WHERE id = ?", (solution_id,))
        solution_result = cursor.fetchone()
        solution_name = solution_result[0] if solution_result else "Unknown Solution"
        
        # Get developer names for assigned_id and creator_id
        for flow in flows:
            # Add solution name
            flow["solution_name"] = solution_name
            
            # Get assignee name if assigned
            if flow.get("assigned_id"):
                cursor.execute("SELECT name FROM developers WHERE id = ?", (flow["assigned_id"],))
                assignee_result = cursor.fetchone()
                flow["assigned"] = assignee_result[0] if assignee_result else "Unknown Developer"
            else:
                flow["assigned"] = "Unassigned"    
    return flows

# API endpoint to create a flow
@app.route('/api/flows', methods=['POST'])
def create_flow():
    """Create a new flow"""
    # Check if feature is enabled
    if not feature_flags.is_enabled('create_flow'):
        return jsonify({"error": "Feature not enabled"}), 403
    
    conn = database.get_connection()
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'solution_id', 'priority', 'creator_id']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Create flow using FlowHandler
        handler = FlowHandler(conn)
        success = handler.create_flow(
            title=data['title'],
            description=data['description'],
            solution_id=data['solution_id'],
            priority=data['priority'],
            creator_id=data['creator_id']
        )
        
        if success:
            return jsonify({"message": "Flow created successfully"}), 201
        else:
            return jsonify({"error": "Failed to create flow"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

# NEW: API endpoint to check feature flags
@app.route('/api/features', methods=['GET'])
def get_features():
    """Return current feature flag status"""
    return jsonify(feature_flags.flags)
		
if __name__ == "__main__":
	with app.app_context():
		db.create_all()
	app.run(host='0.0.0.0', port=5000, debug=True)
