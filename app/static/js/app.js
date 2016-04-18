'use strict';

/* App Module */
var sweetMusicApp = angular.module('sweetMusicApp', [
    'controllers',
    'filters',
    'services',
    'ngRoute',
    'door3.css',
    'ngSanitize'
]);

sweetMusicApp
.config(['$routeProvider',
    function($routeProvider){
        $routeProvider.
            when('/', {
                templateUrl : '/partials/splash.html',
                controller : 'SplashCtrl',
                css : 'css/splash.css'
            }).
            when('/artists', {
                templateUrl : '/partials/artists.html',
                controller : 'ArtistTableCtrl',
                css : 'css/artists.css'
            }).
            when('/artists/:artistID', {
                templateUrl : '/partials/artist-details.html',
                controller : 'ArtistDetailsCtrl',
                css : 'css/artist-details.css'
            }).
            when('/albums', {
                templateUrl : '/partials/albums.html',
                controller : 'AlbumTableCtrl',
                css : 'css/albums.css'
            }).
            when('/albums/:albumID', {
                templateUrl : '/partials/album-details.html',
                controller : 'AlbumDetailsCtrl',
                css : 'css/album-details.css'
            }).
            when('/tracks', {
                templateUrl : '/partials/tracks.html',
                controller : 'TrackTableCtrl',
                css : 'css/tracks.css'
            }).

            when('/tracks/:trackID', {
                templateUrl : '/partials/track-details.html',
                controller : 'TrackDetailsCtrl',
                css : 'css/track-details.css'
            }).
            when('/about', {
                templateUrl : 'partials/about.html',
                controller : 'AboutCtrl',
                css : 'css/about.css'
            }).
            when('/results/:table/:searchTerm', {
                templateUrl : 'partials/search.html',
                controller : 'SearchCtrl',
                css : 'css/search.css'
            }).
            when('/ildb', {
                templateUrl : 'partials/ildb.html',
                controller : 'ILDBCtrl',
                css : 'css/ildb.css'
            }).
            otherwise({
                redirectTo: '/'
            });
}])
.config(['$sceDelegateProvider',
    function($sceDelegateProvider) {
        $sceDelegateProvider.
            resourceUrlWhitelist(
                ['self',
                 'https://*.spotify.com/**'
                ]);
}]);