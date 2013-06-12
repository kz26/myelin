showMessages = ->

LoginCtrl = ($scope, $http, $window, pgp) ->
	$scope.login = ->
		fr1 = new FileReader()
		privateKeyFile = angular.element('#inputPrivateKeyFile').get(0).files[0]
		fr1.onload = ->
			privateKeyText = fr1.result
			sessionStorage.setItem('privateKeyText', privateKeyText)
			privateKey = pgp.read_privateKey(privateKeyText)
			if privateKey == null
				$scope.error_privateKey = true
				return
			privateKey = privateKey[0]
			$scope.privateKey = privateKey
			sessionStorage.setItem('privateKey', privateKey)

			fr2 = new FileReader()
			publicKeyFile = angular.element('#inputPublicKeyFile').get(0).files[0]
			fr2.onload = ->
				publicKeyText = fr2.result
				sessionStorage.setItem('publicKey', publicKeyText)
				publicKey = pgp.read_publicKey(publicKeyText)
				if publicKey == null
					$scope.error_publicKey = true
					return
				publicKey = publicKey[0]
				$scope.publicKey = publicKey
				$scope.publicKeyFingerprint = util.hexstrdump($scope.publicKey.getFingerprint()).toUpperCase()
				sessionStorage.setItem('publicKey', publicKey)

				$http.post("/pgp/login/challenge/", {pubkey_fingerprint: $scope.publicKeyFingerprint})
					.success (data) ->
						messages = pgp.read_message(data.challenge)
						keymat = {key: $scope.privateKey, keymaterial: $scope.privateKey.privateKeyPacket}
						if not keymat.keymaterial.decryptSecretMPIs($scope.privateKeyPassword)
							return
						challengeStr = messages[0].decrypt(keymat, messages[0].sessionKeys[0])
						$http.post("/pgp/login/response/", {pubkey_fingerprint: $scope.publicKeyFingerprint, response: challengeStr})
							.success (data) ->
								console.log "Login success"
			fr2.readAsText(publicKeyFile)
		fr1.readAsText(privateKeyFile)

		return false
