'use strict';

/* Controllers */
angular.module('controllers', ['ui.bootstrap', 'chart.js'])

/**
 * Splash Page Controller
 */
.controller('SplashCtrl', ['$scope', '$location', function($scope, $location) {
    $scope.search = function() {
        $location.path("/results/all/" + $scope.searchTerm);
    }
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
       commits: 40,
       issues: 1,
       unitTests: 4,
       imgSrc: "imgs/dabrego-headshot.png",
       responsibilities: "Designed RESTful API, Documentation",
       bio: "Avid swimmer and social video gamer"
      },
      {name: "Ragan Behrens",
       commits: 0,
       issues: 2,
       unitTests: 0,
       imgSrc: "imgs/ragan_behrens.jpg",
       responsibilities: "Back End",
       bio: "Fourth year computer science student. I'm from South Padre Island. Avid gamer, and moderate car enthusiast."
      },
      {name: "Kristine Domingo",
       commits: 164,
       issues: 27,
       unitTests: 0,
       imgSrc: "imgs/kristine.jpg",
       responsibilities: "Front-end, AngularJS, Wiki",
       bio: "Get schwifty"
      },
      {name: "Jorge Munoz",
       commits: 45,
       issues: 20,
       unitTests: 5,
       imgSrc: "imgs/jorge_munoz.jpg",
       responsibilities: "Back end, SQLAcademy, Database",
       bio: "Take everything into moderation including Burrito Factory."
      },
      {name: "Micah Ramirez",
       commits: 72,
       issues: 48,
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
    $scope.sortType = 'artist_name';
    $scope.sortReverse = false;
    $scope.sortOrder = $scope.sortReverse ? 'desc' : 'asc';
    $scope.maxSize = 5;
    $scope.numPerPage = 10;
    $scope.pageNumber = 1;

    // Get albums upon page load
    artistService.getArtists($scope.pageNumber, $scope.numPerPage, $scope.sortType,
                           $scope.sortOrder).then(function(data) {
        $scope.all_artists = data.artists;
        $scope.totalArtists = data.total_artists;
    });

    // Update displayed_artists upon page change
    $scope.changePage = function() {
        artistService.getArtists($scope.pageNumber, $scope.numPerPage, $scope.sortType,
                               $scope.sortOrder).then(function(data) {
          $scope.all_artists = data.artists;
          $scope.totalArtists = data.total_artists;
        });
    }

    // Sort based on sortType
    $scope.sort = function() {
        $scope.sortOrder = $scope.sortReverse ? 'desc' : 'asc';
        artistService.getArtists($scope.pageNumber, $scope.numPerPage, $scope.sortType,
                               $scope.sortOrder).then(function(data) {
          $scope.all_artists = data.artists;
          $scope.totalArtists = data.total_artists;
        });
    }
}])

/**
 * Artist Details Page Controller
 * Parses and stores information to be displayed on an Artist's details page.
 */
.controller('ArtistDetailsCtrl', ['$scope', '$routeParams', 'artistBioService','artistNewsService','artistDetailsService', function($scope, $routeParams, artistBioService, artistNewsService, artistDetailsService) {
    artistDetailsService.artistDetailsInfo($routeParams.artistID).then(function(data) {
      
        $scope.currentArtist = data.artists[0];
        artistBioService.getArtistDetails($scope.currentArtist.spotify_uri).then(function(data){
            $scope.bios = data.response.biographies;
            if(!$scope.bios[0]){
              $scope.bios = {0:{text:"No data available!"}};
            }
            var idx = 0;
            var bioLength = false;
            //Find a reasonably sized bio that is not null
            while(idx < $scope.bios.length && $scope.bios[idx] && !bioLength){
              //to short move on
              if($scope.bios[idx].text.length < 100){
                idx++;
              }else{
                //found a reasonably sized one so terminate loop
                bioLength = true;
                $scope.bios = [$scope.bios[idx]];
              }
            }
        });

        artistNewsService.getArtistDetails($scope.currentArtist.spotify_uri).then(function(data){
            $scope.news = data.response.news;
        });
        //grab the medium sized image
        $scope.artistPhoto = $scope.currentArtist.artists_image;
        $scope.name = $scope.currentArtist.name;
    });
}])

/**
 * Album Table Page Controller
 * Loads and populates the rows of the Album table. Also contains variables to
 * handle sorting and pagination in the table.
 */
.controller('AlbumTableCtrl',['$scope', 'albumService', function($scope, albumService) {
    $scope.sortType = 'album_name';
    $scope.sortReverse = false;
    $scope.sortOrder = $scope.sortReverse ? 'desc' : 'asc';
    $scope.maxSize = 5;
    $scope.numPerPage = 10;
    $scope.pageNumber = 1;

    // Get albums upon page load
    albumService.getAlbums($scope.pageNumber, $scope.numPerPage, $scope.sortType,
                           $scope.sortOrder).then(function(data) {
        $scope.all_albums = data.albums;
        $scope.totalAlbums = data.total_albums;
    });

    // Update displayed_albums upon page change
    $scope.changePage = function() {
        albumService.getAlbums($scope.pageNumber, $scope.numPerPage, $scope.sortType,
                               $scope.sortOrder).then(function(data) {
          $scope.all_albums = data.albums;
          $scope.totalAlbums = data.total_albums;
        });
    }

    // Sort based on sortType
    $scope.sort = function() {
        $scope.sortOrder = $scope.sortReverse ? 'desc' : 'asc';
        albumService.getAlbums($scope.pageNumber, $scope.numPerPage, $scope.sortType,
                               $scope.sortOrder).then(function(data) {
          $scope.all_albums = data.albums;
          $scope.totalAlbums = data.total_albums;
        });
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
    $scope.sortType = 'track_title';
    $scope.sortReverse = false;
    $scope.sortOrder = $scope.sortReverse ? 'desc' : 'asc';
    $scope.maxSize = 5;
    $scope.numPerPage = 10;
    $scope.pageNumber = 1;

    // Get albums upon page load
    trackService.getTracks($scope.pageNumber, $scope.numPerPage, $scope.sortType,
                           $scope.sortOrder).then(function(data) {
        $scope.all_tracks = data.tracks;
        $scope.totalTracks = data.total_count;
    });

    // Update displayed_tracks upon page change
    $scope.changePage = function() {
        trackService.getTracks($scope.pageNumber, $scope.numPerPage, $scope.sortType,
                               $scope.sortOrder).then(function(data) {
          $scope.all_tracks = data.tracks;
          $scope.totalTracks = data.total_count;
        });
    }

    // Sort based on sortType
    $scope.sort = function() {
        $scope.sortOrder = $scope.sortReverse ? 'desc' : 'asc';
        trackService.getTracks($scope.pageNumber, $scope.numPerPage, $scope.sortType,
                               $scope.sortOrder).then(function(data) {
          $scope.all_tracks = data.tracks;
          $scope.totalTracks = data.total_count;
        });
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
        $scope.widget = 'https://embed.spotify.com/?uri=' + $scope.targetTrack.spotify_uri + "&view=coverart";

        // Get 300px album cover
        $scope.albumCover = $scope.targetTrack.album_cover_url;
    });
}])

/**
 * Search Results Page Controller
 * Parses and displays search result information.
 */
.controller('SearchCtrl', ['$scope', '$routeParams', 'searchService', function($scope, $routeParams, searchService) {
    // Perform the search
    searchService.performSearch($routeParams.table, $routeParams.searchTerm).then(function(data) {
        $scope.searchTerm = $routeParams.searchTerm;
        $scope.table = $routeParams.table;
        $scope.results = data;
        $scope.switch = 'and';

        $scope.displayed_artists = $scope.results[$scope.switch]['artists'];
        $scope.displayed_albums = $scope.results[$scope.switch]['albums'];
        $scope.displayed_tracks = $scope.results[$scope.switch]['tracks'];

        // Switch between displaying "and" and "or" results
        $scope.toggleSwitch = function(toggle) {
            $scope.switch = toggle;
            $scope.displayed_artists = $scope.results[$scope.switch]['artists'];
            $scope.displayed_albums = $scope.results[$scope.switch]['albums'];
            $scope.displayed_tracks = $scope.results[$scope.switch]['tracks'];
        }
    });
}])

/**
 * ILDB Page Controller
 * Exercises the API of the Internet Legislative Database project.
 */
.controller('ILDBCtrl', ['$scope', '$routeParams', 'ILDBService', function($scope, $routeParams, ILDBService) {
    $scope.error = "It looks like ILDB's API is down.";
    ILDBService.getLegislators().then(function(data) {
        var allLegislators = data.legislators;
        if(allLegislators) {
            $scope.error = undefined;
        }

        // Separate Legislators by state
        var states = {};
        allLegislators.forEach(function(person) {
            if(person.state in states) {
                states[person.state].push(person);
            }
            else {
                states[person.state] = [];
                states[person.state].push(person);
            }
        });

        // Seaparate Legislators by party (within each state)
        $scope.partiesByState = {};
        for(var state in states) {
            if(states.hasOwnProperty(state)) {
                var state_legislators = states[state];
                $scope.partiesByState[state] = {"Democrats": [], "Republicans": []};
                state_legislators.forEach(function(person) {
                    if(person.party === "Democrat") {
                        $scope.partiesByState[state]["Democrats"].push(person);
                    }
                    if(person.party === "Republican") {
                        $scope.partiesByState[state]["Republicans"].push(person);
                    }
                });
            }
        }

        // A function that returns legislator information about a specific state
        $scope.getStateLegislators = function(state) {
            $scope.currentState = state;
            $scope.displayedInfo = $scope.partiesByState[state];
            $scope.labels = ["Democrats", "Republicans"];
            $scope.colors = ['#97BBCD', '#F7464A'];

            // Calculate donut percentages
            var totalDemocrats = $scope.displayedInfo["Democrats"].length;
            var totalRepublicans = $scope.displayedInfo["Republicans"].length;
            $scope.data = [totalDemocrats, totalRepublicans];
        };
    });
}])

/**
 * Navigation Controller
 * Underlines the link to the page the user is currently on.
 */
.controller('NavCtrl', ['$scope', '$location', function($scope, $location) {
    $scope.isActive = function(viewLocation) {
        return $location.path().indexOf(viewLocation) == 0;
    }

    $scope.$on('$routeChangeSuccess', function(){
      $scope.isSplash = function(){
        return !($location.path() == "/");
      }
    });

    $scope.isSplash = function(){
        return !($location.path() == "/");
    }

    $scope.search = function() {
        $location.path("/results/all/" + $scope.searchTerm);
    }
}]);