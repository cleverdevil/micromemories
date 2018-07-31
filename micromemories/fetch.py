from dateutil.parser import parse as parse_dt
from concurrent import futures

import json
import mf2py
import re


def handle_child(child):
    full_child = mf2py.parse(url=child['properties']['url'][0], html_parser='lxml')
    full_child['items'][0]['properties']['url'] = child['properties']['url']
    return dict(full_child['items'][0])


def handle_child_json(child):
    full_child = mf2py.parse(url=child['url'], html_parser='lxml')
    result = full_child['items'][0]
    result['properties']['url'] = [child['url']]
    return result


def json_items_for(content, month=1, day=1, full_content=False):
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
            full_results = executor.map(handle_child_json, results)

        results = list(full_results)

    return results


def items_for(content, month=1, day=1, full_content=False):
    result = mf2py.parse(content, html_parser='lxml')

    # check for any found items
    items = result.get('items', [])
    if len(items) == 0:
        return []

    # we're looking for an h-feed
    feed = items[0]
    if len(feed.get('children', [])) == 0:
        return []

    # collect the results
    results = []
    for child in feed['children']:
        published = child.get('properties', {}).get('published')
        if not published:
            continue

        published = parse_dt(published[0])

        if (published.month == month and published.day == day):
            results.append(dict(child))

    # if we are to fetch full content, handle that in multiple
    # threads to speed things up
    if full_content:
        with futures.ThreadPoolExecutor() as executor:
            full_results = executor.map(handle_child, results)

        results = list(full_results)

    return results
