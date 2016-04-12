'use strict';

/* Services */
angular.module('services',[])
    .factory('artistService', function($http) {
        return {
            getArtists: function(page, pageSize, sortBy, order) {
                return $http.get('/artists/' + page +
                                 '?psize=' + pageSize +
                                 '&sort=' + sortBy +
                                 '&order=' + order).then(function(result) {
                    return result.data;
                });
            }
        }
    })
    .factory('artistDetailsService', function($http){
        return {
            artistDetailsInfo: function(artist_id){
                return $http.get('/artists?ids=' + artist_id).then(function(result) {
                        return result.data;
                });
            }
        }
    })
    .factory('albumService', function($http) {
        return {
            getAlbums: function(page, pageSize, sortBy, order) {
                return $http.get('/albums/' + page +
                                 '?psize=' + pageSize +
                                 '&sort=' + sortBy +
                                 '&order=' + order).then(function(result) {
                    return result.data;
                });
            }
        }
    })
    .factory('albumDetailsService', function($http) {
        return {
            getAlbumDetails: function(album_id) {
                return $http.get('/albums?ids=' + album_id).then(function(result) {
                    return result.data;
                });
            }
        }
    })
    .factory('trackService', function($http) {
        return {
            getTracks: function(page, pageSize, sortBy, order) {
                return $http.get('/tracks/' + page +
                                 '?psize=' + pageSize +
                                 '&sort=' + sortBy +
                                 '&order=' + order).then(function(result) {
                    return result.data;
                });
            }
        }
    })
    .factory('trackDetailsService', function($http) {
        return {
            getTrackDetails: function(track_id) {
                return $http.get('/tracks?ids=' + track_id).then(function(result) {
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
            getArtistDetails : function(artistURI) {
                return $http.get('http://developer.echonest.com/api/v4/artist/news?api_key=KY1N8FMAVNUGZY0WR&id=' + artistURI + '&format=json').then(function(result){
                    return result.data;
                });
            }
        }
    })
    .factory('unitTestService', function($http) {
        return {
            runUnitTests : function() {
                return $http.get('/run_tests').then(function(result){
                    return result.data;
                });
            }
        }
    });