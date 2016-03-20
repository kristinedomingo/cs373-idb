'use strict';

/* App Module */
var sweetMusicApp = angular.module('sweetMusicApp', [
    'controllers',
    'services',
    'ngRoute',
    'door3.css'
]);

sweetMusicApp.config(['$routeProvider',
    function($routeProvider){
        console.log("trying to route");
        console.log($routeProvider);
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
            when('/albums', {
                templateUrl : '/partials/albums.html',
                controller : 'AlbumTableCtrl',
                css : 'css/albums.css'
            }).
            when('/test/:artistID', {
                templateUrl : '/partials/artist-details.html',
                controller : 'ArtistDetailsCtrl'
            }).
            when('/about', {
                templateUrl : 'partials/about.html',
                controller : 'AboutCtrl',
                css : 'css/about.css'
            }).
            otherwise({
                redirectTo: '/'
            });
        console.log("trying to configure");
}]);

console.log("App loaded");
console.log(sweetMusicApp);