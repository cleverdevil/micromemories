Micro Memories
==============

Code used for creating an "On This Day" page for a Micro.blog hosted website.

Currently used on [my wife's site](http://cleverangel.org/on-this-day).

To use, simply create a page on your Micro.blog website with the following
content:

```html
<div id="on-this-day">
  Loading...
</div>

<script src="https://micromemories.cleverdevil.io/js?tz=US/Pacific"></script>
```

This will inject some JavaScript into the page, which will then discover and
crawl your `/archive` page, and populate the content for you.

Make sure to pass the appropriate time zone. If none is specified in the request
for the JavaScript, then 'US/Pacific' will be assumed. For a full listing of
available time zone strings, refer to [the IANA time zone
database](https://www.iana.org/time-zones).

Note: this is still relatively experimental, and has some assumptions baked in
that need to be made configurable on a per-website basis.
