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
