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
    }])
    .controller('NavCtrl', ['$scope', '$location', function($scope, $location){
        $scope.isActive = function(viewLocation) {
            return $location.path().indexOf(viewLocation) == 0;
        }
    }]);