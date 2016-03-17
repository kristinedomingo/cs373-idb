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
	    }
});

