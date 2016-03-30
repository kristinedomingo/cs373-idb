'use strict';

/* Controllers */
angular.module('controllers', [])
    .controller('ArtistTableCtrl',['$scope', 'artistService', function($scope, artistService) {
        $scope.sortType = 'name';
        $scope.sortReverse = false;
        $scope.artists = JSON.parse(localStorage.getItem('artistTable'));
        if($scope.artists == null) {
            artistService.getArtists().then(function(data) {
                $scope.artists = data.artists;
                localStorage.setItem('artistTable', JSON.stringify(data.artists));
            });
        }
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
    .controller('SplashCtrl', ['$scope', 'artistService', 'albumService', 'trackService', function($scope, artistService, albumService, trackService) {
        artistService.getArtists().then(function(data) {
            localStorage.setItem('artistTable', JSON.stringify(data.artists));
        });
        albumService.getAlbums().then(function(data) {
            localStorage.setItem('albumTable', JSON.stringify(data.albums));
        });
        trackService.getTracks().then(function(data) {
            localStorage.setItem('trackTable', JSON.stringify(data.tracks));
        });
    }])
    .controller('AboutCtrl', ['$scope', 'unitTestService', function($scope, unitTestService) {
        // Team member information
        $scope.teamMembers =
         [{name: "Daniel Abrego",
           commits: 13,
           issues: 0,
           unitTests: 4,
           imgSrc: "imgs/dabrego-headshot.png",
           responsibilities: "Designed RESTful API, Documentation",
           bio: "Avid swimmer and social video gamer"
          },
          {name: "Ragan Behrens",
           commits: 0,
           issues: 0,
           unitTests: 0,
           imgSrc: "imgs/ragan_behrens.jpg",
           responsibilities: "Back End",
           bio: "Fourth year computer science student. I'm from South Padre Island. Avid gamer, and moderate car enthusiast."
          },
          {name: "Kristine Domingo",
           commits: 88,
           issues: 28,
           unitTests: 0,
           imgSrc: "imgs/kristine.jpg",
           responsibilities: "Front-end, AngularJS, Wiki",
           bio: "Third-year CS major who enjoys good food and cute puppies."
          },
          {name: "Jorge Munoz",
           commits: 13,
           issues: 4,
           unitTests: 5,
           imgSrc: "imgs/jorge_munoz.jpg",
           responsibilities: "Back end, SQLAcademy, Database",
           bio: "Take everything into moderation including Burrito Factory."
          },
          {name: "Micah Ramirez",
           commits: 44,
           issues: 10,
           unitTests: 0,
           imgSrc: "imgs/micah.jpg",
           responsibilities: "Full Stack, AngularJS, Wiki",
           bio: "Austin Native who enjoys good coffee and great IPAs."
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

        // Run unit tests
        $scope.runTests = function() {
            $scope.testOutput = "Running tests..."
            unitTestService.runUnitTests().then(function(output) {
                $scope.testOutput = output.output;
            });
        }
    }])
    .controller('AlbumTableCtrl',['$scope', 'albumService', function($scope, albumService) {
        $scope.sortType = 'name';
        $scope.sortReverse = false;
        $scope.albums = JSON.parse(localStorage.getItem('albumTable'));
        if($scope.albums == null) {
            albumService.getAlbums().then(function(data) {
                $scope.albums = data.albums;
                localStorage.setItem('albumTable', JSON.stringify(data.albums));
            });
        }
    }])
    .controller('AlbumDetailsCtrl', ['$scope', '$routeParams', function($scope, $routeParams) {
        // Find the correct album
        $scope.albums = JSON.parse(localStorage.getItem('albumTable'));
        $scope.targetAlbum = $scope.albums.find(function(album) {
            return album.id == $routeParams.albumID;
        });

        // Get 300px album cover
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

        // Get iframe src
        $scope.widget = 'https://embed.spotify.com/?uri=' + $scope.targetAlbum.uri;
    }])
    .controller('TrackTableCtrl',['$scope', 'trackService',  function($scope, trackService) {
        $scope.sortType = 'name';
        $scope.sortReverse = false;
        $scope.tracks = JSON.parse(localStorage.getItem('trackTable'));
        if($scope.tracks == null) {
            trackService.getTracks().then(function(data) {
                $scope.tracks = data.tracks;
                localStorage.setItem('trackTable', JSON.stringify(data.tracks));
            });
        }
    }])
    .controller('TrackDetailsCtrl', ['$scope', '$routeParams', '$sce', function($scope, $routeParams, $sce) {
        // Find the correct track
        $scope.tracks = JSON.parse(localStorage.getItem('trackTable'));
        $scope.targetTrack = $scope.tracks.find(function(track) {
            return track.id == $routeParams.trackID;
        });

        // Get iframe src
        $scope.widget = 'https://embed.spotify.com/?uri=' + $scope.targetTrack.uri;

        // Get 300px album cover
        $scope.albumCover = $scope.targetTrack.album.images[1].url;
    }])
    .controller('NavCtrl', ['$scope', '$location', function($scope, $location){
        $scope.isActive = function(viewLocation) {
            return $location.path().indexOf(viewLocation) == 0;
        }
    }]);