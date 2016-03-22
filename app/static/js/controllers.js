'use strict';

/* Controllers */
angular.module('controllers', [])
    .controller('ArtistTableCtrl',['$scope', 'artistService', function($scope, artistService) {
        $scope.artists = []
        artistService.getArtists().then(function(data) {
            $scope.artists = data.artists;
            $scope.sortType = 'name';
            $scope.sortReverse = false;
            localStorage.setItem('artistTable', JSON.stringify(data.artists));
        });
    }])
    .controller('ArtistDetailsCtrl', ['$scope', '$routeParams', 'artistBioService','artistNewsService', function($scope, $routeParams, artistBioService, artistNewsService) {
        $scope.artists = JSON.parse(localStorage.getItem('artistTable'));
        //finds the artist obj that was clicked on
        $scope.currentArtist = $scope.artists.find(function(artist){
            return artist.id == $routeParams.artistID;
        });
        artistBioService.getArtistDetails($scope.currentArtist.uri).then(function(data){
          $scope.bios = data.response.biographies;
          if(!$scope.bios[0]){
            $scope.bios = {0:{text:"No data available!"}};
          }
        });

        artistNewsService.getArtistDetails($scope.currentArtist.uri).then(function(data){
          $scope.news = data.response.news;
        });
        //grab the medium sized image
        $scope.artistPhoto = $scope.currentArtist.images[1].url;
        $scope.name = $scope.currentArtist.name;

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
        // Find the correct album
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

        // Get individal artists and their ids
        $scope.artistIDs = [];
        $scope.targetAlbum.artists.forEach(function(artist) {
            $scope.artistIDs.push({name: artist.name, id: artist.id});
        });
    }])
    .controller('TrackTableCtrl',['$scope', 'trackService',  function($scope, trackService) {
        $scope.tracks = []
        trackService.getTracks().then(function(data) {
            $scope.tracks = data.tracks;
            $scope.sortType = 'name';
            $scope.sortReverse = false;
            localStorage.setItem('trackTable', JSON.stringify(data.tracks));
        });
    }])

    .controller('TrackDetailsCtrl', ['$scope', '$routeParams', 'trackLyricsService', function($scope, $routeParams, trackLyricsService) {
        // Find the correct track
        $scope.tracks = JSON.parse(localStorage.getItem('trackTable'));
        $scope.targetTrack = $scope.tracks.find(function(track) {
            return track.id == $routeParams.trackID;
        });
    }])
    .controller('NavCtrl', ['$scope', '$location', function($scope, $location){
        $scope.isActive = function(viewLocation) {
            return $location.path().indexOf(viewLocation) == 0;
        }
    }]);