var app = angular.module('napuor', ['ui.bootstrap']); 

app.controller('list-products', function($scope, $http) {
    		$http.get('http://napuorapi.com/products/').
        	then(function(response) {
            $scope.products = response.data;
        });


});


app.controller('list-banners', function($scope, $http) {
    		$http.get('http://napuorapi.com/business/banners/').
        	then(function(response) {
            $scope.MyIntervals = 0;	
            $scope.banners = response.data
        });
});
  

app.controller('list-categories', function($scope, $http) {
            $http.get('http://napuorapi.com/products/category/').
            then(function(response) {
            $scope.categories = response.data;
        });
});
