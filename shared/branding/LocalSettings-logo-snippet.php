<?php
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
