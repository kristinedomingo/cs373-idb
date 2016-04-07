'use strict';

/* App Module */
var sweetMusicApp = angular.module('sweetMusicApp', [
    'controllers',
    'filters',
    'services',
    'ngRoute',
    'door3.css'
]);

sweetMusicApp
.config(['$routeProvider',
    function($routeProvider){
        $routeProvider.
            when('/', {
                templateUrl : '/partials/splash.html',
                controller : 'SplashCtrl',
                css : {
                    href: 'css/splash.css',
                    bustCache: true
                }
            }).
            when('/artists', {
                templateUrl : '/partials/artists.html',
                controller : 'ArtistTableCtrl',
                css : {
                    href: 'css/artists.css',
                    bustCache: true
                }
            }).
            when('/artists/:artistID', {
                templateUrl : '/partials/artist-details.html',
                controller : 'ArtistDetailsCtrl',
                css : {
                    href: 'css/artist-details.css',
                    bustCache: true
                }
            }).
            when('/albums', {
                templateUrl : '/partials/albums.html',
                controller : 'AlbumTableCtrl',
                css : {
                    href: 'css/albums.css',
                    bustCache: true
                }
            }).
            when('/albums/:albumID', {
                templateUrl : '/partials/album-details.html',
                controller : 'AlbumDetailsCtrl',
                css : {
                    href: 'css/album-details.css',
                    bustCache: true
                }
            }).
            when('/tracks', {
                templateUrl : '/partials/tracks.html',
                controller : 'TrackTableCtrl',
                css : {
                    href: 'css/tracks.css',
                    bustCache: true
                }
            }).

            when('/tracks/:trackID', {
                templateUrl : '/partials/track-details.html',
                controller : 'TrackDetailsCtrl',
                css : {
                    href: 'css/track-details.css',
                    bustCache: true
                }
            }).
            when('/about', {
                templateUrl : 'partials/about.html',
                controller : 'AboutCtrl',
                css : {
                    href: 'css/about.css',
                    bustCache: true
                }
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