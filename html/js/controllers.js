var metadata = angular.module('metadata', ['ui.bootstrap', 'textAngular', 'jsTree.directive']);

var uploaddir = "../uploads/";

metadata.controller('metadataCtrl', ['$scope', '$http', '$timeout', function($scope, $http, $timeout){
    $scope.templateType = ['article', 'book'];


    $http.get("../cgi/getJSON.py").success(function(data){
        $scope.files = data;
    });


    // jsTree config
    $scope.typesConfig = {
        "book": {
            "icon": "glyphicon glyphicon-book"
        },
        "file": {
            "icon": "glyphicon glyphicon-file"
        }
    };
    $scope.changedCB = function(e, data){
        console.log("selected in tree: "+data.selected[0]+"\n");
        $timeout(function() {
            angular.element("button#"+data.selected[0]).triggerHandler('click');
        }, 0);
    };
    $scope.selectTree = function(treeid){
        angular.forEach($scope.files, function(value, i){
            if(value['id'] == treeid){
                value['selected'] = true;
            }else{
                value['selected'] = false;
            }
        });
    };


    /*
    $http.get("../cgi/getJSON.py").success(function(data){
        $scope.jsondata = data;
        $scope.journalid = $scope.jsondata['metadata']['journal-meta']['journal-id']['#text'];
        $scope.articletitle = $scope.jsondata['metadata']['article-meta']['title-group']['article-title'];
    });
    $scope.save = function() {
        $http.post("../uploads/"+$scope.book.text+"/metadata.json", $scope.jsondata);
    };
    */

}]);

