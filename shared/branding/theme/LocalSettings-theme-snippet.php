<?php
// Put snap-theme.css in the same branding/ folder as the logos, then add to LocalSettings.php.
$wgResourceModules['snap.theme'] = [
    'localBasePath' => "$IP/branding",
    'remoteBasePath' => "$wgScriptPath/branding",
    'styles' => [ 'snap-theme.css' ],
];
$wgHooks['BeforePageDisplay'][] = static function ( OutputPage $out ) {
    $out->addModuleStyles( 'snap.theme' );
};
