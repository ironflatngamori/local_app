#!/usr/bin/env python
"""
contains the phases routes
"""
from views import app_views
from flask import jsonify, render_template
from sql_utils import get_all_phases, get_phase_by_id, get_subtopic_by_id
import html

@app_views.route('/', strict_slashes=False)
@app_views.route('/phases', strict_slashes=False)
def phases():
    """
    get phases
    """
    return render_template('phases.html', phases=get_all_phases())

@app_views.route('/phases/<uuid:id>/topics', methods=['GET'], strict_slashes=False)
@app_views.route('/phases/<uuid:id>', methods=['GET'], strict_slashes=False)
def phase(id):
    """
    get phase by id
    """
    phase = get_phase_by_id(id)
    if not phase:
        return jsonify({'error': 'Phase not found'}), 404
    return render_template('phase.html', phase=phase, topics=phase['topics'])

@app_views.route('/phases/<uuid:phase_id>/topics/<uuid:topic_id>/subtopics/<uuid:subtopic_id>',
           methods=['GET'], strict_slashes=False)
def subtopic(phase_id, topic_id, subtopic_id):
    """
    get subtopic by phase id, topic id and subtopic id
    """
    subtopic = get_subtopic_by_id(subtopic_id)
    phase = get_phase_by_id(phase_id)
    if not subtopic:
        return jsonify({'error': 'Subtopic not found'}), 404
    content = html.unescape(subtopic['content'])
    return render_template('subtopic.html',  phase=phase, subtopic=subtopic, content=content.replace(
                '<span style="font-size: 24pt; background-color: #3598db; border: 2px solid;">',
                "<span class=''>"
              )
              .replace("https://moringa.instructure.com/", ""))
