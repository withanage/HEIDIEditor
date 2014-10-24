'use strict';

var components = ['ui.bootstrap', 'textAngular', 'jsTree.directive'];
var metadata = angular.module('metadata', components);

metadata.factory('JsonData', function(){
    return {
        files: null,
        pubType : ['pdf', 'epub', 'html'],
        idType : [
            { name: 'archive', info: 'Identifier assigned by an archive or other repository for articles' },
            { name: 'aggregator', info: 'Identifier assigned by a data aggregator' },
            { name: 'doaj', info: 'Directory of Open Access Journals'},
            { name: 'doi', info: 'Digital Object Identifier for the entire journal, not just for the article (rare)' },
            { name: 'index', info: 'Identifier assigned by an abstracting or indexing service' },
            { name: 'publisher-id', info: 'Identifier assigned by the content publisher, for example, "HeiPUB"'}
        ]
    };
});


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

        $scope.pubType = JsonData.pubType;
        $scope.idType = JsonData.idType;



        $scope.duplicate = function(obj, key){
            if(obj.hasOwnProperty(key)){
                if(!angular.isArray(obj[key])){
                    var tmp = obj[key];
                    obj[key] = [tmp];
                }
                obj[key].push(obj[key][0])
            }
        };

        // jsTree config
        $scope.typesConfig = {
            "book": {
                "icon": "glyphicon glyphicon-folder-open"
            },
            "file": {
                "icon": "glyphicon glyphicon-file"
            }
        };
        $scope.changedCB = function(e, data){
            console.log(data);
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
