<?php
# SNAP wiki settings. This file is in git, so it holds NO secrets:
# passwords and keys come from environment variables that Docker fills in from wiki/.env.
if ( !defined( 'MEDIAWIKI' ) ) {
	exit;
}

## Site
$wgSitename = 'SNAP';
$wgMetaNamespace = 'SNAP';
# Public address. wiki/.env overrides it with http://localhost:8180 until the tunnel is up (item 7).
$wgServer = getenv( 'MW_SERVER' ) ?: 'https://snap.amburgey.dev';
# Send every plain-http visit to https (Cloudflare tells us the protocol in X-Forwarded-Proto).
$wgForceHTTPS = true;
$wgLanguageCode = 'en';
$wgLocaltimezone = 'America/New_York';

## Behind the Cloudflare tunnel: requests arrive from Docker's gateway, and the visitor's
## real address is in X-Forwarded-For (set by Cloudflare). Trust that header only from
## this machine and Docker's own networks (the wiki port is bound to 127.0.0.1).
$wgUsePrivateIPs = true;
$wgCdnServersNoPurge = [ '127.0.0.1', '172.16.0.0/12' ];

## Short URLs: program files at /w, pages at /wiki/Page_name
$wgScriptPath = '/w';
$wgArticlePath = '/wiki/$1';
$wgUsePathInfo = true;
$wgResourceBasePath = $wgScriptPath;

## Database
$wgDBtype = 'mysql';
$wgDBserver = 'db';
$wgDBname = 'snapwiki';
$wgDBuser = 'snapwiki';
$wgDBpassword = getenv( 'MW_DB_PASSWORD' );
$wgDBprefix = '';
$wgDBTableOptions = 'ENGINE=InnoDB, DEFAULT CHARSET=binary';

## Secrets
$wgSecretKey = getenv( 'MW_SECRET_KEY' );
$wgUpgradeKey = getenv( 'MW_UPGRADE_KEY' );
$wgAuthenticationTokenVersion = '1';

## Caching (APCu is in the image; sessions go to the database so they survive restarts)
$wgMainCacheType = CACHE_ACCEL;
$wgSessionCacheType = CACHE_DB;

## Email is off for now
$wgEnableEmail = false;
$wgEnableUserEmail = false;

## Uploads
$wgEnableUploads = true;
$wgUseImageMagick = true;
$wgImageMagickConvertCommand = '/usr/bin/convert';
$wgFileExtensions = array_unique( array_merge( $wgFileExtensions, [ 'png', 'gif', 'jpg', 'jpeg', 'webp', 'svg', 'pdf' ] ) );
$wgSVGConverter = 'rsvg';
$wgMaxUploadSize = 100 * 1024 * 1024;

## Skin
wfLoadSkin( 'Vector' );
$wgDefaultSkin = 'vector-2022';
# Phones get the real screen width instead of a shrunken 1120 px desktop page.
$wgVectorResponsive = true;
# Light / Dark / Automatic switch in the Appearance menu, for everyone (like Wikipedia).
$wgVectorNightMode['logged_out'] = true;
$wgVectorNightMode['logged_in'] = true;
# Logged-in accounts see the same layout as visitors: Tools behind ⋮, Main menu behind ☰.
$wgDefaultUserOptions['vector-page-tools-pinned'] = 0;
$wgDefaultUserOptions['vector-main-menu-pinned'] = 0;
# Default Appearance (Tim's choice): Wide width. Small text and Light colour are Vector's own defaults.
$wgDefaultUserOptions['vector-limited-width'] = 0;

## Branding: the A icon, SNAP wordmark and tagline (Vector 2022 lays them out), favicon
$wgLogos = [
	'icon' => "$wgScriptPath/branding/icon.svg",
	'wordmark' => [
		'src' => "$wgScriptPath/branding/wordmark.svg",
		'width' => 102,
		'height' => 34,
	],
	'tagline' => [
		'src' => "$wgScriptPath/branding/tagline.svg",
		'width' => 102,
		'height' => 11,
	],
	// legacy fallback for skins that still use a single logo
	'1x' => "$wgScriptPath/branding/logo-135.png",
];
$wgFavicon = "$wgScriptPath/branding/favicon.ico";
$wgAppleTouchIcon = "$wgScriptPath/branding/apple-touch-icon.png";

## Cream theme: loaded on every page as a ResourceLoader style module
$wgResourceModules['snap.theme'] = [
	'localBasePath' => "$IP/theme",
	'remoteBasePath' => "$wgScriptPath/theme",
	'styles' => [ 'snap-theme.css', 'snap-mainpage.css' ],
];
$wgHooks['BeforePageDisplay'][] = static function ( $out ) {
	$out->addModuleStyles( 'snap.theme' );
};

## Permissions
## Anyone can read and create an account. Accounts can discuss on talk pages.
## Only the "writer" group and admins can edit content, upload or move pages.
$wgGroupPermissions['*']['edit'] = false;
$wgGroupPermissions['*']['createpage'] = false;
$wgGroupPermissions['*']['createtalk'] = false;
$wgGroupPermissions['*']['createaccount'] = true;

# Content namespaces (everything that isn't a talk page) need the editcontent right.
# When an extension adds a namespace, add it here too.
$wgNamespaceProtection[NS_MAIN] = [ 'editcontent' ];
$wgNamespaceProtection[NS_USER] = [ 'editcontent' ];
$wgNamespaceProtection[NS_PROJECT] = [ 'editcontent' ];
$wgNamespaceProtection[NS_FILE] = [ 'editcontent' ];
$wgNamespaceProtection[NS_TEMPLATE] = [ 'editcontent' ];
$wgNamespaceProtection[NS_HELP] = [ 'editcontent' ];
$wgNamespaceProtection[NS_CATEGORY] = [ 'editcontent' ];
$wgNamespaceProtection[828] = [ 'editcontent' ];   # Module: (Scribunto; its NS_MODULE constant isn't defined yet here)

# Ordinary accounts: talk pages only, no uploads, no moves.
foreach ( [ 'upload', 'reupload', 'reupload-own', 'move', 'move-subpages', 'move-rootuserpages',
	'move-categorypages', 'movefile', 'editcontentmodel', 'changetags' ] as $right ) {
	$wgGroupPermissions['user'][$right] = false;
}

# Writers (and admins) do everything content-related.
foreach ( [ 'editcontent', 'upload', 'reupload', 'reupload-own', 'move', 'move-subpages',
	'move-rootuserpages', 'move-categorypages', 'movefile' ] as $right ) {
	$wgGroupPermissions['writer'][$right] = true;
	$wgGroupPermissions['sysop'][$right] = true;
}
$wgAddGroups['sysop'][] = 'writer';
$wgRemoveGroups['sysop'][] = 'writer';

## Anti-spam: a question at sign-up, and when a talk-page edit adds a web link (ConfirmEdit, bundled)
wfLoadExtensions( [ 'ConfirmEdit', 'ConfirmEdit/QuestyCaptcha' ] );
$wgCaptchaClass = 'QuestyCaptcha';
$wgCaptchaQuestions = [
	'What is the name of this game? (Four letters, in the logo at the top left.)' => 'snap',
	'Finish the tagline in the logo: "A free tabletop ___"' => 'rpg',
	'How many sides does an ordinary cube-shaped die have? (Use digits.)' => [ '6', 'six' ],
	'What color is the bar across the A in the SNAP logo?' => 'orange',
];

## Extensions (see extensions.md for where each comes from and its pinned version)
# Visual editor (bundled): "Edit" opens the visual editor, "Edit source" the wikitext editor,
# as on Wikipedia. Also available on SNAP: project pages.
wfLoadExtension( 'VisualEditor' );
$wgDefaultUserOptions['visualeditor-enable'] = 1;
$wgVisualEditorAvailableNamespaces['Project'] = true;

# Wikipedia's article toolkit (item 13): infoboxes, sidebars, navboxes, hatnotes, timelines and
# citations are imported from Wikipedia (tools/import-wikipedia.py) and need these extensions.
# All ship with 1.43 except TemplateStyles (pinned in the Dockerfile).
wfLoadExtensions( [ 'ParserFunctions', 'Scribunto', 'TemplateStyles', 'TemplateData', 'Cite', 'WikiEditor', 'CodeEditor' ] );
$wgScribuntoDefaultEngine = 'luasandbox';
$wgScribuntoUseCodeEditor = true;
# {{SHORTDESC:}} for Wikipedia's {{Short description}}: used in search suggestions. Like Wikipedia's
# desktop site, the line under the title stays "From SNAP" rather than showing the description.
wfLoadExtension( 'ShortDescription' );
$wgShortDescriptionEnableTagline = false;

# <choose uncached> on the Main Page: a new featured pick on every visit.
wfLoadExtension( 'RandomSelection' );

# OAuth: lets the MCP connector sign in as a wiki account (item 12). Only admins can register
# and approve apps. The signing keys live in wiki/secrets/ (gitignored), mounted read-only.
wfLoadExtension( 'OAuth' );
$wgOAuth2EnabledGrantTypes = [ 'authorization_code', 'refresh_token' ];
$wgOAuth2PrivateKey = file_get_contents( '/var/www/secrets/oauth2-private.key' );
$wgOAuth2PublicKey = file_get_contents( '/var/www/secrets/oauth2-public.key' );
foreach ( [ 'mwoauthproposeconsumer', 'mwoauthupdateownconsumer', 'mwoauthmanageconsumer', 'mwoauthviewprivate' ] as $right ) {
	$wgGroupPermissions['sysop'][$right] = true;
}
# Apps only keep the rights their grants list. Our custom "editcontent" (see Permissions) is in no
# built-in grant, so add it to "Edit existing pages"; without it a connected app can't edit content.
$wgGrantPermissions['editpage']['editcontent'] = true;
