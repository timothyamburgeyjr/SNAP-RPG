--[[
	mw.wikibase on a wiki without Wikidata.

	Wikipedia's modules use this library to fill in values from Wikidata. Here every page behaves
	like a Wikipedia article that has no Wikidata item: lookups find nothing, so the modules show
	only what the page itself provides. Function names follow Wikibase Client's Lua library.
]]

local wikibase = {}

local function nothing()
	return nil
end

local function noneList()
	return {}
end

local function emptyText()
	return ''
end

for _, name in ipairs( {
	'getEntity', 'getEntityObject', 'getEntityIdForCurrentPage', 'getEntityIdForTitle',
	'getEntityUrl', 'getLabel', 'getLabelByLang', 'getLabelWithLang', 'getDescription',
	'getDescriptionByLang', 'getDescriptionWithLang', 'getSitelink', 'getReferencedEntityId',
	'resolvePropertyId'
} ) do
	wikibase[name] = nothing
end

for _, name in ipairs( { 'getBestStatements', 'getAllStatements', 'getBadges', 'getPropertyOrder', 'orderProperties' } ) do
	wikibase[name] = noneList
end

for _, name in ipairs( { 'renderSnak', 'renderSnaks', 'formatValue', 'formatValues' } ) do
	wikibase[name] = emptyText
end

function wikibase.isValidEntityId()
	return false
end

function wikibase.entityExists()
	return false
end

function wikibase.getGlobalSiteId()
	return 'snapwiki'
end

function wikibase.setupInterface()
	wikibase.setupInterface = nil
	mw.wikibase = wikibase
	package.loaded['mw.wikibase'] = wikibase
end

return wikibase
