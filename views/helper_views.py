#!/usr/bin/python3
"""
contains helper routes for the application
"""
from flask import jsonify
from views import app_views
from sql_utils import get_all_topics, get_all_subtopics, get_all_phases


@app_views.route('/stats', strict_slashes=False)
def stats():
    """
    get stats
    """
    topics = get_all_topics()
    subtopics = get_all_subtopics()
    phases = get_all_phases()

    return jsonify({
        'topics': len(topics),
        'subtopics': len(subtopics),
        'phases': len(phases)
    })
