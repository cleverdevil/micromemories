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

Requirements
------------

Micro Memories is known to work on all of the standard themes in Micro.blog. If
you are using a custom theme, you need to ensure that your theme makes proper
use of [microformats](http://microformats.org/wiki/microformats2), especially
the [h-entry](http://microformats.org/wiki/microformats2#h-entry) microformat.
The [open source Micro.blog themes](https://github.com/microdotblog) are a good
place to look for guidance.
