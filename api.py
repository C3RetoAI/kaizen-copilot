from dataclasses import asdict
import json
from flask import Flask, request, jsonify
from agent.models.mcphost import MCPHost
from agent.models.issue import Issue
from agent.models.input import QueryFormatterInput

app = Flask(__name__)

app.config['DEBUG'] = True
    
@app.route('/fix_issue', methods=['POST'])
def fix_issue():
    try:
        if request.method =='POST':
            request_data = request.get_json()
            issue = Issue(title=request_data['title'], description=request_data['description'], repo_url=request_data['repo_url'])
            
            input_data = QueryFormatterInput(issue)
            
            host = MCPHost()
        
            solution = host.run_workflow('issue_resolution', input_data)
            json_output = json.dumps(asdict(solution), indent=2)
            return json_output
    except Exception as e:
        print("Error en el webhook:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run()