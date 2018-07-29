from dateutil.parser import parse as parse_dt
from concurrent import futures

import mf2py


def handle_child(child):
    full_child = mf2py.parse(url=child['properties']['url'][0], html_parser='lxml')
    full_child['items'][0]['properties']['url'] = child['properties']['url']
    return dict(full_child['items'][0])


def items_for(url, month=1, day=1, full_content=False):
    month = int(month)
    day = int(day)

    result = mf2py.parse(url=url, html_parser='lxml')

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

        return list(full_results)

    return results
