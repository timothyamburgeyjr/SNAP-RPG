<?php

namespace SnapWiki\WikibaseStub;

class Hooks {

	/**
	 * Register mw.wikibase for Lua, so Wikipedia's modules find the library they expect.
	 */
	public static function onScribuntoExternalLibraries( string $engine, array &$extraLibraries ) {
		if ( $engine === 'lua' ) {
			$extraLibraries['mw.wikibase'] = WikibaseStubLibrary::class;
		}
	}

	/**
	 * {{#property:}} and {{#statements:}}: no Wikidata item, so no value (an empty string).
	 */
	public static function onParserFirstCallInit( $parser ) {
		$parser->setFunctionHook( 'property', static fn () => '' );
		$parser->setFunctionHook( 'statements', static fn () => '' );
	}
}
