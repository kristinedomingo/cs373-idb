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
    .controller('ArtistDetailsCtrl', ['$scope','persistArtist', function($scope, persistArtist) {
        $scope.artists = persistArtist.get();
    }])
    .controller('SplashCtrl', ['$scope' , function($scope) {

    }])
    .controller('AboutCtrl', ['$scope', function($scope) {
        // Team member information
        $scope.teamMembers =
         [{name: "Daniel Abrego",
           commits: 99,
           issues: 99,
           unitTests: 99,
           responsibilities: "Responsibility1, Responsibility 2, Responsibility 3",
           bio: "This is an example biography. Here is some more sample text for this person's biography."
          },
          {name: "Ragan Behrens",
           commits: 99,
           issues: 99,
           unitTests: 99,
           responsibilities: "Responsibility1, Responsibility 2, Responsibility 3",
           bio: "This is an example biography. Here is some more sample text for this person's biography."
          },
          {name: "Kristine Domingo",
           commits: 99,
           issues: 99,
           unitTests: 99,
           responsibilities: "Responsibility1, Responsibility 2, Responsibility 3",
           bio: "This is an example biography. Here is some more sample text for this person's biography."
          },
          {name: "Jorge Munoz",
           commits: 99,
           issues: 99,
           unitTests: 99,
           responsibilities: "Responsibility1, Responsibility 2, Responsibility 3",
           bio: "This is an example biography. Here is some more sample text for this person's biography."
          },
          {name: "Micah Ramirez",
           commits: 99,
           issues: 99,
           unitTests: 99,
           responsibilities: "Responsibility1, Responsibility 2, Responsibility 3",
           bio: "This is an example biography. Here is some more sample text for this person's biography."
          },
          {name: "Firstname LastName",
           commits: 99,
           issues: 99,
           unitTests: 99,
           responsibilities: "Responsibility1, Responsibility 2, Responsibility 3",
           bio: "This is an example biography. Here is some more sample text for this person's biography."
          }];

        // Get the total number of commits, issues, and unit tests
        $scope.totalCommits = 0;
        $scope.totalIssues = 0;
        $scope.totalUnitTests = 0;
        $scope.teamMembers.forEach(function(member) {
            $scope.totalCommits += member.commits;
            $scope.totalIssues += member.issues;
            $scope.totalUnitTests += member.unitTests;
        });
    }])
    .controller('AlbumTableCtrl',['$scope', 'albumService', function($scope, albumService) {
        $scope.albums = []
        albumService.getAlbums().then(function(data) {
            $scope.albums = data.albums;
            $scope.sortType = 'name';
            $scope.sortReverse = false;
            localStorage.setItem('albumTable', JSON.stringify(data.albums));
        });
    }])
    .controller('AlbumDetailsCtrl', ['$scope', '$routeParams', function($scope, $routeParams) {
        $scope.albums = JSON.parse(localStorage.getItem('albumTable'));
        $scope.targetAlbum = $scope.albums.find(function(album) {
            return album.id == $routeParams.albumID;
        });

        // Get album cover
        $scope.albumCover = $scope.targetAlbum.images[1].url;

        // Get tracks
        $scope.tracks = $scope.targetAlbum.tracks.items;

        // Convert ms to minutes and seconds
        $scope.tracks.forEach(function(track) {
            var minutes = Math.floor(track.duration_ms / 60000);
            var seconds = ((track.duration_ms % 60000) / 1000).toFixed(0);
            track.duration_ms = minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
        });
    }])
    .controller('TrackTableCtrl',['$scope', 'trackService', 'persistTrack', function($scope, trackService, persistTrack) {
        $scope.tracks = []
        trackService.getTracks().then(function(data) {
            $scope.tracks = data.tracks;
            $scope.sortType = 'name';
            $scope.sortReverse = false;
            persistTrack.set(data.tracks);
        });
    }])
    .controller('NavCtrl', ['$scope', '$location', function($scope, $location){
        $scope.isActive = function(viewLocation) {
            return $location.path().indexOf(viewLocation) == 0;
        }
    }]);