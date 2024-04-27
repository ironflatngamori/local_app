#!/usr/bin/env python
import os
import sys
import csv
import pandas as pd
from config import __CONTENT_DIR__

# NOTE: THOU SHALL NOT TOUCH THIS
csv.field_size_limit(int(sys.maxsize / 10e10))


def get_content_type(content_type):
    """
    get content type
    """
    assert content_type in ['topics', 'subtopics'], 'Invalid content type'
    # all files in the content directory
    files = [file for file in os.listdir(__CONTENT_DIR__)
             if file.endswith('.csv')
             and file != 'phases.csv']

    if content_type == 'topics':
        return [file for file in files
                if 'subtopics' not in file]
    else:
        return [file for file in files if 'subtopics' in file]

def read_csv(csv_file):
    """
    read csv file
    returns list of dictionaries
    """
    path = os.path.join(__CONTENT_DIR__, csv_file)

    with open(path, 'r', encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return list(reader)

def get_all_phases():
    """
    get phases
    """
    return read_csv('phases.csv')

def get_all_topics():
    """
    get topics
    """
    topics = get_content_type('topics')
    all_topics = []
    for topic in topics:
        topic = read_csv(topic)
        all_topics.extend(topic)
    return all_topics

def get_all_subtopics():
    """
    get subtopics
    """
    subtopics = get_content_type('subtopics')
    all_subtopics = []
    for subtopic in subtopics:
        subtopic = read_csv(subtopic)
        all_subtopics.extend(subtopic)

    for item in all_subtopics:
        item["git_repo"] = item.pop("git_repo")

    return all_subtopics

def get_phase(id):
    """
    get phase by id
    """
    phases = get_all_phases()

    for phase in phases:
        if (str(phase['id']) == str(id)):
            phase['topics'] = get_phase_topics(phase['id'])
            return phase
    return None

def get_subtopic(id):
    """
    get subtopic by id
    """
    subtopics = get_content_type('subtopics')
    all_subtopics = []
    for subtopic in subtopics:
        subtopic = read_csv(subtopic)
        all_subtopics.extend(subtopic)
    for item in all_subtopics:
        if (str(item['id']) == str(id)):
            return item
    return None

def get_topic_subtopics(topic_id):
    """
    get subtopics by topic id
    """
    # get all csv files in the content directory
    # filter out the subtopics csv files
    subtopics = get_content_type('subtopics')
    topic_subtopics = []
    for subtopic in subtopics:
        topic = read_csv(subtopic)
        for item in topic:
            if item['parent_topic_id'] == topic_id:
                topic_subtopics.append(item)
    return topic_subtopics

def get_phase_topics(phase_id):
    """
    get topics by phase id
    """
    # get all csv files in the content directory
    # filter out the subtopics csv files
    topics = get_content_type('topics')
    phase_topics = []
    for topic in topics:
        phase = read_csv(topic)
        for item in phase:
            if item['phase_id'] == phase_id:
                item['subtopics'] = get_topic_subtopics(item['id'])
                phase_topics.append(item)

    return phase_topics
