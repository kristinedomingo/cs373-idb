'use strict';

/* Controllers */
angular.module('controllers', ['ui.bootstrap'])

/**
 * Splash Page Controller
 */
.controller('SplashCtrl', ['$scope', function($scope) {
}])

/**
 * About Page Controller
 * Contains information about team members in the form on a JSON object, and
 * dynamically calculates the team statistics from this object. Also contains
 * a function to run the unit tests on the About page.
 */
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
       bio: "Get schwifty"
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

/**
 * Artist Table Page Controller
 * Loads and populates the rows of the Artist table. Also contains variables to
 * handle sorting and pagination in the table.
 */
.controller('ArtistTableCtrl',['$scope', 'artistService', function($scope, artistService) {
    $scope.sortType = 'name';
    $scope.sortReverse = false;
    $scope.maxSize = 5;
    $scope.numPerPage = 10;

    // Handle case where user just clicks on "Artists"
    if(!$scope.pageNumber) {
        $scope.pageNumber = 1;
    }

    // Get albums upon page load
    artistService.getArtists($scope.pageNumber).then(function(data) {
        $scope.all_artists = data.artists;
        $scope.totalArtists = data.total_artists;
        $scope.displayed_artists = $scope.all_artists.slice(0, $scope.numPerPage);
    });

    // Update displayed_artists upon page change
    $scope.changePage = function() {
        var begin = (($scope.pageNumber - 1) * $scope.numPerPage);
        var end = begin + $scope.numPerPage;
        $scope.displayed_artists = $scope.all_artists.slice(begin, end);
    }

    // Sort based on sortType
    $scope.sort = function() {
      $scope.all_artists.sort(function(x, y) {
          // If the sortType is number of albums, don't sort using string
          // comparison, parse to integers and compare those instead
          if($scope.sortType == 'num_albums' || $scope.sortType == 'popularity') {
              return parseInt(x[$scope.sortType]) - parseInt(y[$scope.sortType]);
          }
          // Case-insensitive string comparison
          else {
              return x[$scope.sortType].localeCompare(y[$scope.sortType]);
          }
      });

      // If reverse, reverse the rows
      if($scope.sortReverse) {
          $scope.all_artists.reverse();
      }

      // Finally, reset page to 1 and update displayed_artists
      $scope.pageNumber = 1;
      $scope.displayed_artists = $scope.all_artists.slice(0, $scope.numPerPage);
    }
}])

/**
 * Artist Details Page Controller
 * Parses and stores information to be displayed on an Artist's details page.
 */
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

/**
 * Album Table Page Controller
 * Loads and populates the rows of the Album table. Also contains variables to
 * handle sorting and pagination in the table.
 */
.controller('AlbumTableCtrl',['$scope', 'albumService', function($scope, albumService) {
    $scope.sortType = 'name';
    $scope.sortReverse = false;
    $scope.maxSize = 5;
    $scope.numPerPage = 10;

    // Handle case where user just clicks on "Albums"
    if(!$scope.pageNumber) {
        $scope.pageNumber = 1;
    }

    // Get albums upon page load
    albumService.getAlbums($scope.pageNumber).then(function(data) {
        $scope.all_albums = data.albums;
        $scope.totalAlbums = data.total_albums;
        $scope.displayed_albums = $scope.all_albums.slice(0, $scope.numPerPage);
    });

    // Update displayed_albums upon page change
    $scope.changePage = function() {
        var begin = (($scope.pageNumber - 1) * $scope.numPerPage);
        var end = begin + $scope.numPerPage;
        $scope.displayed_albums = $scope.all_albums.slice(begin, end);
    }

    // Sort based on sortType
    $scope.sort = function() {
      $scope.all_albums.sort(function(x, y) {
          // If the sortType is number of tracks, don't sort using string
          // comparison, parse to integers and compare those instead
          if($scope.sortType == 'num_tracks') {
              return parseInt(x[$scope.sortType]) - parseInt(y[$scope.sortType]);
          }
          // If the sortType is the album duration, compare converting the
          // String length to a number representing seconds
          else if($scope.sortType == 'length') {
              var xTimes = x['length'].split(':');
              var yTimes = y['length'].split(':');
              return (xTimes[0] * 60 + xTimes[1]) - (yTimes[0] * 60 + yTimes[1]);
          }
          // Case-insensitive string comparison
          else {
              return x[$scope.sortType].localeCompare(y[$scope.sortType]);
          }
      });

      // If reverse, reverse the rows
      if($scope.sortReverse) {
          $scope.all_albums.reverse();
      }

      // Finally, reset page to 1 and update displayed_albums
      $scope.pageNumber = 1;
      $scope.displayed_albums = $scope.all_albums.slice(0, $scope.numPerPage);
    }
}])

/**
 * Album Details Page Controller
 * Parses and stores information to be displayed on an Album's details page.
 */
.controller('AlbumDetailsCtrl', ['$scope', '$routeParams', 'albumDetailsService', function($scope, $routeParams, albumDetailsService) {
    // Find the correct album
    albumDetailsService.getAlbumDetails($routeParams.albumID).then(function(data) {
        $scope.targetAlbum = data.albums[0];
        console.log($scope.targetAlbum);

        // Get 300px album cover
        $scope.albumCover = $scope.targetAlbum.images;

        // Get tracks
        $scope.tracks = $scope.targetAlbum.tracks;

        // Get artist IDs
        $scope.artists = $scope.targetAlbum.artists;

        // Convert ms to minutes and seconds
        $scope.tracks.forEach(function(track) {
            var minutes = Math.floor(track.duration_ms / 60000);
            var seconds = ((track.duration_ms % 60000) / 1000).toFixed(0);
            track.duration_ms = minutes + ":" + (seconds < 10 ? '0' : '') + seconds;
        });

        // Get iframe src
        $scope.widget = 'https://embed.spotify.com/?uri=' + $scope.targetAlbum.spotify_uri;
    });
}])

/**
 * Track Table Page Controller
 * Loads and populates the rows of the Track table. Also contains variables to
 * handle sorting and pagination in the table.
 */
.controller('TrackTableCtrl',['$scope', 'trackService',  function($scope, trackService) {
    $scope.sortType = 'name';
    $scope.sortReverse = false;
    $scope.maxSize = 5;
    $scope.numPerPage = 10;

    // Handle case where user just clicks on "Tracks"
    if(!$scope.pageNumber) {
        $scope.pageNumber = 1;
    }

    // Get albums upon page load
    trackService.getTracks($scope.pageNumber).then(function(data) {
        $scope.all_tracks = data.tracks;
        $scope.totalTracks = data.total_count;
        $scope.displayed_tracks = $scope.all_tracks.slice(0, $scope.numPerPage);
    });

    // Update displayed_tracks upon page change
    $scope.changePage = function() {
        var begin = (($scope.pageNumber - 1) * $scope.numPerPage);
        var end = begin + $scope.numPerPage;
        $scope.displayed_tracks = $scope.all_tracks.slice(begin, end);
    }

    // Sort based on sortType
    $scope.sort = function() {
      $scope.all_tracks.sort(function(x, y) {
          // If the sortType is the track duration, compare using duration_ms
          if($scope.sortType == 'duration') {
              return parseInt(x['duration_ms']) - parseInt(y['duration_ms']);
          }
          // Case-insensitive string comparison
          else {
              return x[$scope.sortType].localeCompare(y[$scope.sortType]);
          }
      });

      // If reverse, reverse the rows
      if($scope.sortReverse) {
          $scope.all_tracks.reverse();
      }

      // Finally, reset page to 1 and update displayed_tracks
      $scope.pageNumber = 1;
      $scope.displayed_tracks = $scope.all_tracks.slice(0, $scope.numPerPage);
    }
}])

/**
 * Track Details Page Controller
 * Parses and stores information to be displayed on an Track's details page.
 */
.controller('TrackDetailsCtrl', ['$scope', '$routeParams', 'trackDetailsService', function($scope, $routeParams, trackDetailsService) {
    // Find the correct track
    trackDetailsService.getTrackDetails($routeParams.trackID).then(function(data) {
        $scope.targetTrack = data.tracks[0];

        // Get iframe src
        $scope.widget = 'https://embed.spotify.com/?uri=' + $scope.targetTrack.spotify_uri;

        // Get 300px album cover
        $scope.albumCover = $scope.targetTrack.album_cover_url;
    });
}])

/**
 * Navigation Controller
 * Underlines the link to the page the user is currently on.
 */
.controller('NavCtrl', ['$scope', '$location', function($scope, $location){
    $scope.isActive = function(viewLocation) {
        return $location.path().indexOf(viewLocation) == 0;
    }
}]);