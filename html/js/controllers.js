

var metadata = angular.module('metadata', []);

var uploaddir = "../uploads/";

metadata.controller('metadataCtrl', ['$scope', '$http', function($scope, $http){
    $http.get("../cgi/listDocs.py").success(function(data){
        $scope.books = data;
    });
    $http.get("../cgi/getMetadata.py").success(function(data){
        $scope.journalid = data.metadata['journal-meta']['journal-id']['#text'];
        $scope.articletitle = data.metadata['article-meta']['title-group']['article-title'];
    });
    $scope.save = function() {
        $http.post("../uploads/Bookname/metadata.json", $scope.jsondata);
    }
}]);
