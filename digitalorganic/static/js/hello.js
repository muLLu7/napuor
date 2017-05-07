angular.module('demo', [])
.controller('Hello', function($scope, $http) {
    $http.get('http://http://52.88.88.50/products/').
        then(function(response) {
            $scope.products = response.data;
        });
});