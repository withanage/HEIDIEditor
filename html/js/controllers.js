'use strict';

var components = ['ui.bootstrap', 'textAngular', 'jsTree.directive'];
var metadata = angular.module('metadata', components);

/* Shared Searvice (global variable) */
metadata.factory('JsonData', function(){
    return {
        files: null
    };
});

/* articleMetadata directive */
metadata.directive('articleMetadata', function(){
    return {
        restrict: "E",
        scope: {src: '='},
        templateurl: './articlemetadata.html',
        compile: function(element, attrs){
            if(attrs.src === ''){

            }
            return function(scope, element, attrs){
                // link function
            }
        }
    };
});

/* bookMetadata directive */
metadata.directive('bookMetadata', function(){
    return {
        restrict: "E",
        scope: {src: '='},
        templateurl: './bookmetadata.html'
    };
});

/* main controller */
metadata.controller('metadataCtrl',
    ['$scope', 'JsonData', function($scope, JsonData){
        $scope.files = JsonData.files;


    }]
);

/* jstree controller */
metadata.controller('jstreeCtrl',
    ['$scope', '$http', '$timeout', 'JsonData', function($scope, $http, $timeout, JsonData) {
        $http.get("../cgi/createJSON.py").success(function(data){
            $scope.files = data;
            JsonData.files = data;
        });

        $scope.isArray = function(obj){
            if(obj){
                return angular.isArray(obj);
            }
            return false;
        };

        // Check if json has key
        $scope.hasOwnProperty = function(json, key){
            if(json){
                return json.hasOwnProperty(key);
            }
            return false;
        };

        $scope.htmlVariable = 'test';

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


    }]
);

metadata.controller('modalCtrl',
    ['$scope', '$modal', function($scope, $modal) {
        $scope.open = function () {
            $modal.open({
                templateUrl: 'checkSource.html',
                windowTemplateUrl: 'aside.template.html',
                controller: 'asideCtrl'
            });
        }
    }]
);

metadata.controller('asideCtrl',
    ['$scope', '$modalInstance', 'JsonData', function($scope, $modalInstance, JsonData) {
        $scope.contents = JsonData.files;

        $scope.close = function(){
            JsonData.files = $scope.contents;
            $modalInstance.close();
        };
        $scope.cancel = function(){
            $modalInstance.dismiss('cancel');
        };
    }]
);
