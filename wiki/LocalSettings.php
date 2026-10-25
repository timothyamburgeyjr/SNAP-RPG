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
$wgLanguageCode = 'en';
$wgLocaltimezone = 'America/New_York';

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
	'styles' => [ 'snap-theme.css' ],
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

## Extensions: none yet beyond the bundled ones above (see extensions.md)
