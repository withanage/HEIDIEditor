

/* metadataFields directive */
metadata.directive('metadataFields', function(){
    return {
        restrict: "E",
        templateUrl: './tpls/metadataFields.html'
    };
});

/* bookMeta directive*/
metadata.directive('bookMeta', function(){
    return{
        restrict: "E",
        templateUrl: './tpls/bookMeta.html'
    };
});

/* bookChapter directive*/
metadata.directive('bookChapter', function(){
    return{
        restrict: "E",
        templateUrl: './tpls/bookChapter.html'
    };
});

/* bookPart directive*/
metadata.directive('bookPart', function(){
    return{
        restrict: "E",
        templateUrl: './tpls/bookPart.html'
    };
});

metadata.directive('header', function(){
    return {
        restrict: "E",
        scope: {
            step: '='
        },
        templateUrl: './tpls/header.html'
    };
});

metadata.directive('footer', function(){
    return {
        restrict: "E",
        templateUrl: './tpls/footer.html',
        controller : ['$scope','JsonData', function($scope, JsonData) {
            $scope.contents = JsonData.tree;
        }]
    };
});

metadata.filter('range', function() {
    return function(arr, lower, upper) {
        for (var i = lower; i <= upper; i++){
            arr.push(i);
        }
        return arr;
    };
});