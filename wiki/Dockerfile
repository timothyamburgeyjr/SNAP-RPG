# SNAP wiki: the official MediaWiki image, with the program files moved to /w
# so pages can live at /wiki/Page_name (Wikipedia-style short URLs, item 3).
FROM mediawiki:1.43.11

RUN set -eux; \
    mv /var/www/html /var/www/w; \
    mkdir /var/www/html; \
    mv /var/www/w /var/www/html/w

RUN a2enmod headers

COPY apache-snap.conf /etc/apache2/conf-enabled/snap.conf
COPY php-snap.ini /usr/local/etc/php/conf.d/snap.ini

# Extensions are added here, each at a pinned commit (see extensions.md).

# RandomSelection (item 10): the "new pick each visit" boxes on the Main Page. REL1_43 branch.
RUN set -eux; \
    mkdir /var/www/html/w/extensions/RandomSelection; \
    curl -fsSL "https://gerrit.wikimedia.org/r/plugins/gitiles/mediawiki/extensions/RandomSelection/+archive/d559bf2f49f1b39fd407a56ceeabbb3845ea0364.tar.gz" \
        | tar -xz -C /var/www/html/w/extensions/RandomSelection; \
    test -f /var/www/html/w/extensions/RandomSelection/extension.json
