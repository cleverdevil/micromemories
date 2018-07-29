from dateutil.parser import parse as parse_dt

import mf2py


def items_for(url, month=1, day=1, full_content=False):
    month = int(month)
    day = int(day)

    result = mf2py.parse(url=url)

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
            if full_content:
                full_child = mf2py.parse(url=child['properties']['url'][0])
                full_child['items'][0]['properties']['url'] = child['properties']['url']
                child = full_child['items'][0]
            results.append(child)

    return results


#results = get_items_for('http://cleverangel.org/archive', month=8, day=19, full_content=True)
#
#
#import json
#print(json.dumps(results, indent=2))
