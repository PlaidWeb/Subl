# Subl

Subl is an attempt at making a lightweight, self-hostable, social-oriented feed reader.

It's intended as a companion to [Publ](https://github.com/PlaidWeb/Publ) but neither has a dependency on the other.

## Goals

Things I definitely want:

* Easy to host (anywhere you can host a Python/Flask app, including locally on your own computer)
* Data portability (import/export via OPML et al)
* Lightweight built-in UX with support for external clients (protocol support TBD, probably [Microsub](https://indieweb.org/Microsub) at least)
* Lightweight server requirements (e.g. support for SQLite, no need for websockets etc.)
* Support for authenticated (i.e. private content/friends-only) feeds via a number of emergent quasi-standards, such as:
    * shared cookies
    * bearer tokens (ad-hoc, [TicketAuth](https://indieweb.org/IndieAuth_Ticket_Auth), ...)
* Support for [Micropub](https://indieweb.org/Micropub) for quick replies/responses
* User-configurable "channels" with different behaviors appropriate to the types of content in those channels (blogs, news, comics, social, etc.)
* Support for unloved-but-useful Atom standards (RFC5005 archive feeds, category tags, deletions, etc.)
* Support for WebSub/PuSH

Non-goals:

* being a "web app" (see [rant](http://beesbuzz.biz/blog/2934-Advice-to-young-web-developers))
* native ActivityPub support (maybe eventually but that's a very very long-term thing)
* immediate updates/notifications, algorithmic suggestions, infinite scroll UI, etc.; it's okay to have a stopping point!

## More information

* [Authenticated feed token grant proposal](http://beesbuzz.biz/blog/5711-Access-token-grants-for-feed-readers)
* [One of many disconnected/obsolete rambles about Subl](http://beesbuzz.biz/blog/8118-So-what-is-Subl-anyway)
* [indieweb](https://indieweb.org/)
* [Feed on Feeds](https://github.com/fluffy-critter/Feed-on-Feeds), the reader this is meant to replace (but is still quite good in its own right)
