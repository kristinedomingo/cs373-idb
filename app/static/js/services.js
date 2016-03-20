'use strict';

/* Services */
angular.module('services',[])
	.factory('artistService', function($http){
		return {
			getArtists: function(){
				//since $http.get returns a promise,
		        //and promise.then() also returns a promise
		        //that resolves to whatever value is returned in it's 
		        //callback argument, we can return that.
		        return $http.get('/get_artists').then(function(result){
		        	return result.data;
		        });
	    	}
	    }})
	.factory('persistArtist', function(){
		//persist Artist data on routing so that we 
		//don't have to do another Http request
		var savedArtists = {};
		function saveArtists(data){
			savedArtists = data;
		}

		function getArtists(){
			return savedArtists;
		}

		return {
			set:saveArtists,
			get:getArtists
		}
	});
