KeygenCtrl = ($scope, $window, pgp) ->
	$scope.generate = ->
		$scope.keys = pgp.generate_key_pair 1, 2048, "#{ $scope.name } <#{ $scope.email }>"

	blobProps = {"type": "text\/plain"}
	$scope.downloadPrivateKey = ->
		$window.location = $window.URL.createObjectURL(Blob([$scope.keys.privateKeyArmored], blobProps))
	$scope.downloadPublicKey = ->
		$window.location = $window.URL.createObjectURL(Blob([$scope.keys.publicKeyArmored], blobProps))
