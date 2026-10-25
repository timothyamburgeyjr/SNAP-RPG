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

# OAuth (item 12): lets the MCP connector sign in as a wiki account. Official 1.43 bundle
# (includes its vendor libraries), checked against the checksum recorded when it was chosen.
RUN set -eux; \
    curl -fsSL -o /tmp/OAuth.tar.gz "https://extdist.wmflabs.org/dist/extensions/OAuth-REL1_43-ce3cc80.tar.gz"; \
    echo "a404374a72c8c3a8a93504cd2405cc0a27472b799a8bc27eec919c3867ec94e5  /tmp/OAuth.tar.gz" | sha256sum -c -; \
    tar -xzf /tmp/OAuth.tar.gz -C /var/www/html/w/extensions; \
    rm /tmp/OAuth.tar.gz
