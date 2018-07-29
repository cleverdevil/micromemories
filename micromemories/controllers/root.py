from pecan import expose, redirect, request
from pecan.hooks import PecanHook, HookController
from webob.exc import status_map
from datetime import datetime
from urllib.parse import urlparse

from .. import fetch

import pytz


JAVASCRIPT = '''var container = document.getElementById('on-this-day');

function renderPost(post) {
    var postEl = document.createElement('div');
    postEl.className = 'post';
    container.appendChild(postEl);

    if (post['properties']['name'] != null) {
        var titleEl = document.createElement('h2');
        titleEl.className = 'p-name';
        titleEl.innerText = post['properties']['name'][0];
        postEl.appendChild(titleEl);
    }

    var permalinkEl = document.createElement('a');
    permalinkEl.className = 'post-date u-url';
    permalinkEl.href = post['properties']['url'][0];
    postEl.appendChild(permalinkEl);

    var publishedEl = document.createElement('time');
    publishedEl.className = 'dt-published';
    publishedEl.datetime = post['properties']['published'][0];

    var published = post['properties']['published'][0];
    published = new Date(published.slice(0,-5).replace(' ', 'T'));

    publishedEl.innerText = published.toDateString();
    permalinkEl.appendChild(publishedEl);

    var contentEl = document.createElement('div');
    contentEl.className = 'e-content';
    contentEl.innerHTML = post['properties']['content'][0]['html'];
    postEl.appendChild(contentEl);
}

var xhr = new XMLHttpRequest();
xhr.responseType = "json";
xhr.open('GET', "https://micromemories.cleverdevil.io/posts?tz=%(timezone)s", true);
xhr.send();

xhr.onreadystatechange = function(e) {
    if (xhr.readyState == 4 && xhr.status == 200) {
        container.innerHTML = '';
        xhr.response.forEach(function(post) {
            renderPost(post);
        });
    }
}'''


class CorsHook(PecanHook):

    def after(self, state):
        state.response.headers['Access-Control-Allow-Origin'] = '*'
        state.response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        state.response.headers['Access-Control-Allow-Headers'] = 'origin, referer, authorization, accept'



class RootController(HookController):

    __hooks__ = [CorsHook()]

    @expose(template='index.html')
    def index(self):
        return dict()

    @expose('json')
    def posts(self, month=None, day=None, tz='US/Pacific', url=None):
        if url is None:
            referer = request.headers.get('Referer')
            if not referer:
                return []

            referer = urlparse(referer)
            url = '%s://%s/archive' % (
                referer.scheme,
                referer.netloc
            )

        print('Fetching ->', url)

        if not month:
            today = pytz.utc.localize(datetime.utcnow())
            today = today.astimezone(pytz.timezone(tz))
            month = today.month
            day = today.day

        items = fetch.items_for(url, month=month, day=day, full_content=True)

        return items

    @expose(content_type='application/javascript')
    def js(self, tz='US/Pacific'):
        return JAVASCRIPT % {'timezone': tz}

    @expose('error.html')
    def error(self, status):
        try:
            status = int(status)
        except ValueError:  # pragma: no cover
            status = 500
        message = getattr(status_map.get(status), 'explanation', '')
        return dict(status=status, message=message)
