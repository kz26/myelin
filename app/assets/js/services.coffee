app = angular.module('app', ['ngCookies'])
app.factory 'pgp', ->
	openpgp.init()
	return openpgp
app.run ($cookies) ->
	app.config ($httpProvider) ->
		$httpProvider.defaults.headers.post['X-CSRFToken'] = $cookies['csrftoken']
