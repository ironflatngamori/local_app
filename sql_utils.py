#!/usr/bin/env python
"""
uses sqlite3 to retrieve data from the database

Contains the following functions:
    * connect_to_db - connects to the database
    * get_all_phases - retrieves all phases from the database
    * get_all_topics - retrieves all topics from the database
    * get_all_subtopics - retrieves all subtopics from the database
    * get_phase_by_id - retrieves a phase by its ID
    * get_topic_by_id - retrieves a topic by its ID
    * get_subtopic_by_id - retrieves a subtopic by its ID
    * get_topic_subtopics - retrieves all subtopics for a topic
    * get_phase_topics - retrieves all topics for a phase
"""
import sqlite3


def connect_to_db():
    """
    connects to the database
    """
    return sqlite3.connect('school.db')

def results_to_list(list_of_tuples, keys):
    """Converts results to a list of lists."""
    return  [dict(zip(keys, row)) for row in list_of_tuples]

def results_to_dict(tuple, keys):
    """Converts results to a dictionary."""
    return dict(zip(keys, tuple))

def get_table_columns(cursor):
    """
    retrieves the columns of a table
    """
    return [description[0] for description in cursor.description]

def get_all_phases():
    """
    retrieves all phases from the database
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM phases")
    keys = get_table_columns(cursor)
    phases = results_to_list(cursor.fetchall(), keys)
    conn.close()

    return phases

def get_all_topics():
    """
    retrieves all topics from the database
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM topics")
    topics = results_to_list(cursor.fetchall(), get_table_columns(cursor))
    conn.close()

    return topics

def get_all_subtopics():
    """
    retrieves all subtopics from the database
    """
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subtopics")
    subtopics = results_to_list(cursor.fetchall(), get_table_columns(cursor))
    conn.close()

    return subtopics

def get_phase_by_id(id):
    """
    retrieves a phase by its ID
    """
    id = str(id)
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM phases WHERE id = ?", (id,))
    phase = results_to_dict(cursor.fetchone(), get_table_columns(cursor))
    phase['topics'] = get_phase_topics(id)
    conn.close()

    return phase

def get_topic_by_id(id):
    """
    retrieves a topic by its ID
    """
    id = str(id)
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM topics WHERE id = ?", (id,))
    topic = results_to_dict(cursor.fetchone(), get_table_columns(cursor))
    conn.close()

    return topic

def get_subtopic_by_id(id):
    """
    retrieves a subtopic by its ID
    """
    id = str(id)
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subtopics WHERE id = ?", (id,))
    subtopic = results_to_dict(cursor.fetchone(), get_table_columns(cursor))
    conn.close()

    return subtopic

def get_topic_subtopics(topic_id):
    """
    retrieves all subtopics for a topic
    """
    topic_id = str(topic_id)
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM subtopics WHERE parent_topic_id = ?", (topic_id,))
    subtopics = results_to_list(cursor.fetchall(), get_table_columns(cursor))
    conn.close()

    return subtopics

def get_phase_topics(phase_id):
    """
    retrieves all topics for a phase
    """
    phase_id = str(phase_id)
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM topics WHERE phase_id = ?", (phase_id,))
    topics = results_to_list(cursor.fetchall(), get_table_columns(cursor))

    for topic in topics:
        topic['subtopics'] = get_topic_subtopics(topic['id'])

    conn.close()

    return topics