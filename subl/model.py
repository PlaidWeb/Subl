""" Database schema for subscriptions """

# pylint: disable=too-few-public-methods

import datetime
import logging
from enum import Enum

from pony import orm

db = orm.Database()  # pylint: disable=invalid-name

DbEntity: orm.core.Entity = db.Entity

LOGGER = logging.getLogger(__name__)

# schema version; bump this number if it changes
SCHEMA_VERSION = 1


class User(DbEntity):
    """ A user of the system """
    self_id = orm.Required(str)
    profile = orm.Required(str)

    subscriptions = orm.Set("Subscription")
    channels = orm.Set("Channel")
    collections = orm.Set("Collection")


class Collection(DbEntity):
    """ User collections of items, for sharing/bookmarking/etc. """
    user = orm.Required(User)
    name = orm.Required(str)
    public = orm.Required(bool)
    items = orm.Set("Item")


class Feed(DbEntity):
    """ A feed known to the system """
    feed_url = orm.Required(str, unique=True)
    self_url = orm.Required(str)
    title = orm.Required(str)

    links = orm.Set("FeedLink")

    # URL to obtain feed authorization
    auth_url = orm.Optional(str)

    last_update = orm.Optional(datetime.datetime)
    next_update = orm.Optional(datetime.datetime)

    websub_hub = orm.Optional(str)
    websub_secret = orm.Optional(str)
    websub_lease = orm.Optional(datetime.datetime)

    subscriptions = orm.Set("Subscription")
    items = orm.Set("Item")  # public items only


class FeedLink(DbEntity):
    """ A feed link """
    feed = orm.Required(Feed)
    href = orm.Required(str)
    rel = orm.Optional(str)
    content_type = orm.Optional(str)

    orm.composite_index(feed, rel)


class ExpirationPolicy(Enum):
    """ The item expiration policy for a channel """
    NEVER = 1       # keep items forever
    BACKFILL = 2    # backfill items via RFC5005
    EXPIRE = 3      # allow items to expire after a certain time


class Subscription(DbEntity):
    """ A user's subscription to a feed """
    user = orm.Required(User)
    feed = orm.Required(Feed)

    auth_cookie = orm.Optional(str)
    auth_token = orm.Optional(str)
    auth_error_code = orm.Optional(int)
    auth_error_string = orm.Optional(str)
    last_update = orm.Optional(datetime.datetime)

    # the last time an RFC5005 backfill was performed
    last_backfill = orm.Optional(datetime.datetime)

    items = orm.Set("Item")
    unread = orm.Set("Item")
    channels = orm.Set("Channel")

    tags = orm.Set("Tag")

    orm.composite_key(user, feed)


class Item(DbEntity):
    """ A feed/subscription item """
    feed = orm.Optional(Feed)  # Only set if there's no auth involved
    subscription = orm.Set(Subscription, reverse="items")
    unread = orm.Set(Subscription, reverse="unread")
    collections = orm.Set(Collection)

    links = orm.Set("ItemLink")
    guid = orm.Required(str)

    published = orm.Required(datetime.datetime)
    updated = orm.Optional(datetime.datetime)
    title = orm.Optional(str)
    summary = orm.Optional(str)
    content = orm.Optional(str)
    link = orm.Optional(str)

    # Last time seen in a feed (for expiration)
    last_seen = orm.Required(datetime.datetime)

    orm.composite_key(subscription, guid)


class SubscriptionItem(DbEntity):
    """ An item that exists within a subscription """
    subscription = orm.Required(Subscription)
    item = orm.Required(Item)
    unread = orm.Required(bool, default=True)

    orm.composite_key(subscription, item)


class ItemLink(DbEntity):
    """ A link within an item """
    item = orm.Required(Item)
    href = orm.Required(str)
    rel = orm.Optional(str)
    content_type = orm.Optional(str)

    orm.composite_index(item, rel)


class SortOrder(Enum):
    """ The order in which to sort items in a channel """
    OLDEST = 1
    NEWEST = 2


class Channel(DbEntity):
    """ A channel of subscription items """
    user = orm.Required(User)
    name = orm.Required(str)
    sort_order = orm.Required(int)

    subscriptions = orm.Set(Subscription)

    # the expiration policy for this channel
    expiration_policy = orm.Required(int)

    # If policy is EXPIRE, the time after which an item should be removed if
    # unread and no longer visible in the feed; if policy is BACKFILL, how
    # frequently feeds should be re-crawled
    expiration_time = orm.Optional(datetime.timedelta)


class Tag(DbEntity):
    """ A subscription's category/tag information """
    subscription = orm.Required(Subscription)
    term = orm.Required(str)
    label = orm.Optional(str)

    orm.composite_key(subscription, term)
