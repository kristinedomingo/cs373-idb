'use strict';

/* Controllers */
angular.module('controllers', [])
	.controller('ArtistTableCtrl',['$scope', 'artistService', function($scope, artistService){
		$scope.artists = []
		artistService.getArtists().then(function(data){
			$scope.artists = data.artists;
		});
}]);