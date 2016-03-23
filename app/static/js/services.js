'use strict';

/* Services */
angular.module('services',[])
    .factory('artistService', function($http) {
        return {
            getArtists: function() {
                //since $http.get returns a promise,
                //and promise.then() also returns a promise
                //that resolves to whatever value is returned in it's 
                //callback argument, we can return that.
                return $http.get('/get_artists').then(function(result) {
                    return result.data;
                });
            }
        }})
    .factory('albumService', function($http) {
        return {
            getAlbums: function() {
                return $http.get('/get_albums').then(function(result) {
                    return result.data;
                });
            }
        }
    })
    .factory('trackService', function($http) {
        return {
            getTracks: function() {
                return $http.get('/get_tracks').then(function(result) {
                    return result.data;
                });
            }
        }
    })
    .factory('trackMP3Service', function($http) {
        return {
            getMP3: function(trackURI) {
                return $http.get('http://developer.echonest.com/api/v4/track/profile?api_key=KY1N8FMAVNUGZY0WR&format=json&id=' + trackURI).then(function(result) {
                    return result.data;
                });
            }
        }
    })
    .factory('artistBioService', function($http) {
        return {
            getArtistDetails : function(artistURI){
                return $http.get('http://developer.echonest.com/api/v4/artist/biographies?api_key=KY1N8FMAVNUGZY0WR&id=' + artistURI + '&format=json').then(function(result){
                    return result.data;
                });
            }
        }
    })
    .factory('artistNewsService', function($http) {
        return {
            getArtistDetails : function(artistURI){
                return $http.get('http://developer.echonest.com/api/v4/artist/news?api_key=KY1N8FMAVNUGZY0WR&id=' + artistURI + '&format=json').then(function(result){
                    return result.data;
                });
            }
        }
    });