from concurrent import futures

import json
import mf2py
import re


def handle_child(child):
    full_child = mf2py.parse(url=child['url'], html_parser='lxml')

    result = [
        item for item in full_child['items']
        if item['type'][0] == 'h-entry'
    ]

    if len(result):
        result = result[0]
        result['properties']['url'] = [child['url']]
        return result

    return None


def items_for(content, month=1, day=1, full_content=False):
    feed = json.loads(content)
    matching_date = re.compile(r'\d\d\d\d-%.2d-%.2d.*' % (month, day))

    results = []
    for child in feed.get('items', []):
        if matching_date.match(child['date_published']):
            results.append(child)

    # if we are to fetch full content, handle that in multiple
    # threads to speed things up
    if full_content:
        with futures.ThreadPoolExecutor() as executor:
            full_results = executor.map(handle_child, results)

        results = [
           result for result in full_results
           if result is not None
        ]

    return results
