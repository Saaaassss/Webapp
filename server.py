from flask import Flask, render_template, jsonify, send_from_directory, request, redirect, url_for
import json
import os

app = Flask(__name__)
# No secret_key needed!
JSON_FILE = 'links.json'

def read_links():
    if not os.path.exists(JSON_FILE):
        return {}
    with open(JSON_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_links(links):
    with open(JSON_FILE, 'w') as f:
        json.dump(links, f, indent=4)

def add_link_to_json(new_link):
    data = read_links()
    category = new_link['category']
    team = new_link['team']

    if category not in data:
        data[category] = {}
    if team not in data[category]:
        data[category][team] = []

    data[category][team].append({
        "url": new_link['url'],
        "description": new_link['description']
    })

    save_links(data)

# Main page (default)
@app.route('/')
@app.route('/main')
def main():
    return render_template('main.html')

# Admin panel (no login required)
@app.route('/admin')
def admin_panel():
    return render_template('index.html')

# Jenkins page
@app.route('/jenkins')
def jenkins():
    return render_template('jenkins.html')

# JFrog page
@app.route('/jfrog')
def jfrog():
    return render_template('jfrog.html')

# API: Get all data
@app.route('/api/data', methods=['GET'])
def get_data():
    return jsonify(read_links())

# API: Get all links (alias)
@app.route('/api/links', methods=['GET'])
def get_links():
    return jsonify(read_links())

# API: Add new link (no auth required - protected by JavaScript)
@app.route('/api/links', methods=['POST'])
def add_link():
    new_link = request.json
    add_link_to_json(new_link)
    return jsonify({'status': 'success', 'message': 'Link added!'}), 201

# API: Delete link (no auth required - protected by JavaScript)
@app.route('/api/links/delete', methods=['POST'])
def delete_link():
    data = request.json
    links = read_links()
    cat = data['category']
    team = data['team']
    url = data['url']
    description = data['description']

    if cat in links and team in links[cat]:
        links[cat][team] = [l for l in links[cat][team] if not (l['url'] == url and l['description'] == description)]
        if not links[cat][team]:
            del links[cat][team]
        if not links[cat]:
            del links[cat]
        save_links(links)
    return jsonify({'status': 'success'}), 200

# API: Edit link (no auth required - protected by JavaScript)
@app.route('/api/links/edit', methods=['POST'])
def edit_link():
    data = request.json
    old_cat = data['old_category']
    old_team = data['old_team']
    old_url = data['old_url']
    old_description = data['old_description']

    new_cat = data['new_category']
    new_team = data['new_team']
    new_url = data['new_url']
    new_description = data['new_description']

    links = read_links()

    if old_cat in links and old_team in links[old_cat]:
        found = None
        for link in links[old_cat][old_team]:
            if link['url'] == old_url and link['description'] == old_description:
                found = link
                break
        if found:
            links[old_cat][old_team].remove(found)
            if not links[old_cat][old_team]:
                del links[old_cat][old_team]
            if not links[old_cat]:
                del links[old_cat]

            if new_cat not in links:
                links[new_cat] = {}
            if new_team not in links[new_cat]:
                links[new_cat][new_team] = []
            links[new_cat][new_team].append({
                "url": new_url,
                "description": new_description
            })
            save_links(links)
    return jsonify({'status': 'success'}), 200

# Serve templates (CSS)
@app.route('/templates/<path:filename>')
def serve_templates(filename):
    return send_from_directory('templates', filename)

# Serve images
@app.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('images', filename)

# Serve static files
@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
