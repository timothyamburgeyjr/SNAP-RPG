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

# TemplateStyles (item 13): Wikipedia's templates keep their CSS in template-style pages.
# Official 1.43 bundle, checked against the checksum recorded when it was chosen.
RUN set -eux; \
    curl -fsSL -o /tmp/TemplateStyles.tar.gz "https://extdist.wmflabs.org/dist/extensions/TemplateStyles-REL1_43-e74200b.tar.gz"; \
    echo "8df19ca49dd7abfcd9e1dfe7bc1daf82c129337b04bfd95b2825bb0d6887d6f7  /tmp/TemplateStyles.tar.gz" | sha256sum -c -; \
    tar -xzf /tmp/TemplateStyles.tar.gz -C /var/www/html/w/extensions; \
    rm /tmp/TemplateStyles.tar.gz

# ShortDescription 4.0.2 (item 13): the {{SHORTDESC:}} magic word Wikipedia's {{Short description}}
# uses, shown under the page title. No release tags upstream, so pinned to a commit + checksum.
RUN set -eux; \
    curl -fsSL -o /tmp/ShortDescription.tar.gz "https://codeload.github.com/StarCitizenTools/mediawiki-extensions-ShortDescription/tar.gz/8d348a84a2e337b777525daeea2ff01707785171"; \
    echo "4370ea694c802413bf58b174398aef09bba63fe9907732fc96716116e551bb6d  /tmp/ShortDescription.tar.gz" | sha256sum -c -; \
    mkdir /var/www/html/w/extensions/ShortDescription; \
    tar -xzf /tmp/ShortDescription.tar.gz -C /var/www/html/w/extensions/ShortDescription --strip-components=1; \
    rm /tmp/ShortDescription.tar.gz

# GeoData (item 13): the {{#coordinates:}} function Wikipedia's coordinate templates call.
# Official 1.43 bundle, checked against the checksum recorded when it was chosen.
RUN set -eux; \
    curl -fsSL -o /tmp/GeoData.tar.gz "https://extdist.wmflabs.org/dist/extensions/GeoData-REL1_43-fe2da93.tar.gz"; \
    echo "d906a47cc8495d0b3d77fdcc3227581695cfc5294fd01811521cc526f8c1c5f1  /tmp/GeoData.tar.gz" | sha256sum -c -; \
    tar -xzf /tmp/GeoData.tar.gz -C /var/www/html/w/extensions; \
    rm /tmp/GeoData.tar.gz

# TimedMediaHandler and Phonos (item 13): Wikipedia's audio/video player and pronunciation buttons.
# Official 1.43 bundles, checked against the checksums recorded when they were chosen.
RUN set -eux; \
    curl -fsSL -o /tmp/TimedMediaHandler.tar.gz "https://extdist.wmflabs.org/dist/extensions/TimedMediaHandler-REL1_43-768731a.tar.gz"; \
    echo "144cc4340d6085b55f56b240faa7de0a2429107e525020a0dc4efcef0d000825  /tmp/TimedMediaHandler.tar.gz" | sha256sum -c -; \
    curl -fsSL -o /tmp/Phonos.tar.gz "https://extdist.wmflabs.org/dist/extensions/Phonos-REL1_43-d1d5069.tar.gz"; \
    echo "7cc8c4b94a0cf92c4b1bbdcdeaad06cbff199bbafc0cfcf977a07ee771363168  /tmp/Phonos.tar.gz" | sha256sum -c -; \
    tar -xzf /tmp/TimedMediaHandler.tar.gz -C /var/www/html/w/extensions; \
    tar -xzf /tmp/Phonos.tar.gz -C /var/www/html/w/extensions; \
    rm /tmp/TimedMediaHandler.tar.gz /tmp/Phonos.tar.gz

# Programs Wikipedia's extensions run: EasyTimeline (Ploticus + FreeSans) and PdfHandler (Ghostscript).
# Score's programs are left out: sheet music is switched off, as on Wikipedia (see LocalSettings.php).
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends ploticus fonts-freefont-ttf ghostscript; \
    rm -rf /var/lib/apt/lists/*

# EasyTimeline, LabeledSectionTransclusion, WikiHiero, CharInsert, Score, Kartographer + JsonConfig
# (item 13 parity with Wikipedia). Official 1.43 bundles, checked against recorded checksums.
RUN set -eux; \
    cd /tmp; \
    for b in \
        "timeline-REL1_43-770f0c9 de884d6bf078848d0faf32b8a7ffd58d683abeb8fdc8f18665cde2f02426f89a" \
        "LabeledSectionTransclusion-REL1_43-923701b 79d7febb97bc96bdc3a8347ccbebcba3605932ae034937abce4d71eac65945ad" \
        "wikihiero-REL1_43-824d535 f756481e6c8598bd6ff4bb4977c961d906104edbea6a2d8d7f28b00f02694e04" \
        "CharInsert-REL1_43-16747a7 39fbc0c50272bc96dd0e4651a0934de17307bf88d9a8b8fc3fbf3f5925926365" \
        "Score-REL1_43-97e74a7 9bcd419477f40e9e0bc531c27ab2dd8d54c6230502fe91147629101db8539316" \
        "Kartographer-REL1_43-9d4f18d e28d475367d000ac7112da67431f5639a16a02aa1d9aa7bd463ba29059341883" \
        "JsonConfig-REL1_43-e094b36 4dffc35529fec41354df1a84a650e8e69668f1b5d6daef3b98344276ecc2c943"; \
    do \
        set -- $b; \
        curl -fsSL -o "$1.tar.gz" "https://extdist.wmflabs.org/dist/extensions/$1.tar.gz"; \
        echo "$2  $1.tar.gz" | sha256sum -c -; \
        tar -xzf "$1.tar.gz" -C /var/www/html/w/extensions; \
        rm "$1.tar.gz"; \
    done

# WikibaseStub (ours, local-extensions/): mw.wikibase for Wikipedia's Lua modules, answering "no Wikidata item".
COPY local-extensions/WikibaseStub /var/www/html/w/extensions/WikibaseStub
