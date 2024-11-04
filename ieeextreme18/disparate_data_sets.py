# Disparate Data Sets -> 100% of the test cases
# Time limit: 1250 ms
# Memory limit: 256 MB
#
# Given a mixed set of records containing "Parent Event", serialized events, and stand-alone events,
# the task is to sort and organize these records based on specific rules. The data comes in CSV format
# and may have missing fields. The goal is to connect serialized events to their respective parent 
# events, fill in missing data, and exclude events that don't meet certain criteria.
#
# Input format:
# - The input contains CSV records with columns:
#   Event ID,"Event Title","Acronym",Project Code,3 Digit Project Code,"Record Type"
# - Event ID: a unique identifier for each record.
# - Event Title: the event title, with any double quotes escaped.
# - Acronym: used to identify parent and serialized events within a set. Acronyms may not be unique.
# - Project Code: string for each conference (can be empty).
# - 3 Digit Project Code: the last 3 characters of Project Code, shared across events in a serialized set.
# - Record Type: either "Parent Event" or "IEEE Event".
#
# Exclusion Criteria:
# - Remove any parent event without children.
# - Remove serialized sets without a unique parent event.
# - Remove any record without an acronym.
# - Remove any child event without a parent.
#
# Output:
# - Print the serialized sets sorted by acronym. For each set, print the parent event first, followed by its
#   children sorted lexicographically by title (and by Event ID if titles are the same).
# - For each child event, append the parent Event ID to the end.
#
# Constraints and Notes:
# - Maximum of 360 records in the input.
# - Project Code and 3 Digit Project Code for parent events with children must be updated as follows:
#   - If all children have the same 3 Digit Project Code, the parent inherits it.
#   - Otherwise, the parent is assigned a 3 Digit Project Code of "???".
#
# Example:
# Input: (CSV rows)
#   EventID, "Event Title", "Acronym", Project Code, 3 Digit Project Code, "Record Type"
# Output:
#   Sorted serialized sets with structured output as per the requirements.


import csv
from collections import defaultdict
import sys

# Funzione per leggere e gestire i record degli eventi
def read_events(input_data):
    events = []
    reader = csv.reader(input_data)
    for row in reader:
        if not row:
            continue  # Gestisce il caso in cui la riga sia vuota
        event = {
            'id': row[0],
            'title': row[1],
            'acronym': row[2],
            'project_code': row[3],
            'three_digit_code': row[4],
            'record_type': row[5]
        }
        events.append(event)
    return events

# Funzione per elaborare i set serializzati
def process_events(events):
    parent_events = {}
    children_events = defaultdict(list)

    # Raggruppa eventi principali e figli
    for event in events:
        if event['acronym'] == "":
            continue  # Escludi eventi senza acronimo
        if event['record_type'] == "Parent Event":
            parent_events[event['id']] = event
        elif event['record_type'] == "IEEE Event":
            children_events[event['acronym']].append(event)

    # Associa i figli ai genitori e applica condizioni di esclusione
    serialized_sets = []
    used_parents = set()
    for acronym, children in children_events.items():
        parent_candidates = [p for p in parent_events.values() if p['acronym'] == acronym]
        if len(parent_candidates) != 1:
            continue  # Escludi set senza un unico evento principale

        parent = parent_candidates[0]
        used_parents.add(parent['id'])

        # Associa i figli all'evento principale
        valid_children = []
        for child in children:
            if parent['id']:
                child['parent_id'] = parent['id']
                valid_children.append(child)

        # Escludi eventi principali senza figli validi
        if not valid_children:
            continue

        # Determina il codice a 3 cifre dell'evento principale
        three_digit_codes = set(child['three_digit_code'] for child in valid_children)
        parent['three_digit_code'] = "???" if len(three_digit_codes) > 1 else three_digit_codes.pop()

        serialized_sets.append((parent, valid_children))

    # Escludi eventi principali non utilizzati (senza figli)
    serialized_sets = [s for s in serialized_sets if s[0]['id'] in used_parents]

    return serialized_sets

# Funzione per stampare i set serializzati ordinati
def print_serialized_sets(serialized_sets):
    serialized_sets.sort(key=lambda x: x[0]['acronym'])
    output = []

    for parent, children in serialized_sets:
        parent_title = parent["title"].replace('"', '""')
        output.append(",".join([parent['id'], f'"{parent_title}"', f'"{parent["acronym"]}"', "", parent['three_digit_code'], f'"{parent["record_type"]}"']))
        children.sort(key=lambda x: (x['title'], x['id']))
        for child in children:
            child_title = child["title"].replace('"', '""')
            output.append(",".join([child['id'], f'"{child_title}"', f'"{child["acronym"]}"', child['project_code'], child['three_digit_code'], f'"{child["record_type"]}"', child['parent_id']]))

    for line in output:
        print(line)

# Funzione principale
def main():
    input_data = sys.stdin
    events = read_events(input_data)
    if not events:
        print("Nessun evento trovato.")
        return
    serialized_sets = process_events(events)
    print_serialized_sets(serialized_sets)

if __name__ == "__main__":
    main()
