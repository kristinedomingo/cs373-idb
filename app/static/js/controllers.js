'use strict';

/* Controllers */
angular.module('controllers', [])
    .controller('ArtistTableCtrl',['$scope', 'artistService', 'persistArtist', function($scope, artistService, persistArtist) {
        $scope.artists = []
        artistService.getArtists().then(function(data) {
            $scope.artists = data.artists;
            $scope.sortType = 'name';
            $scope.sortReverse = false;
            persistArtist.set(data.artists);
        });
    }])
    .controller('ArtistDetailsCtrl', ['persistArtist', function($scope, persistArtist) {
        $scope.artists = persistArtist.get();
        console.log("Scope");
        console.log($scope);
        console.log("Scope artist data");
        console.log($scope.artists);
    }])
    .controller('SplashCtrl', ['$scope' , function($scope) {

    }])
    .controller('AboutCtrl', ['$scope', function($scope) {

    }])
    .controller('AlbumTableCtrl',['$scope', 'albumService', 'persistAlbum', function($scope, albumService, persistAlbum) {
        $scope.albums = []
        albumService.getAlbums().then(function(data) {
            $scope.albums = data.albums;
            $scope.sortType = 'name';
            $scope.sortReverse = false;
            persistAlbum.set(data.albums);
        });
    }]);