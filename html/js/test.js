'use strict';

var components = ['ui.bootstrap', 'textAngular', 'jsTree.directive', 'xeditable'];
var metadata = angular.module('metadata', components);

metadata.run(function(editableOptions) {
    editableOptions.theme = 'bs3'; // bootstrap3 theme.
});



metadata.factory('JsonData', function(){
    return {
        tree: null,
        pubType : ['pdf', 'epub', 'html'],
        idType : [
            { name: 'archive', info: 'Identifier assigned by an archive or other repository for articles' },
            { name: 'aggregator', info: 'Identifier assigned by a data aggregator' },
            { name: 'doaj', info: 'Directory of Open Access Journals'},
            { name: 'doi', info: 'Digital Object Identifier for the entire journal, not just for the article (rare)' },
            { name: 'index', info: 'Identifier assigned by an abstracting or indexing service' },
            { name: 'publisher-id', info: 'Identifier assigned by the content publisher, for example, "HeiPUB"'}
        ],
        contribType : ['author', 'editor', 'translator', 'designer']
    };
});

metadata.controller('textCtrl',
    ['$scope', '$http', '$timeout', 'JsonData', function($scope, $http, $timeout, JsonData){
        $http.get("../cgi/bookJson.py").success(function(data){
            $scope.tree = data;
            JsonData.tree = data;
        });
        $scope.pubType = JsonData.pubType;
        $scope.idType = JsonData.idType;
        $scope.contribType = JsonData.contribType;

        $scope.dummydate = new Date();
        $scope.resetDate = function(){
            $scope.dummydate.setFullYear($scope.tree['book']['book-meta']['pub-date']['year']);
            $scope.dummydate.setMonth(parseInt($scope.tree['book']['book-meta']['pub-date']['month'])-1);
            $scope.dummydate.setDate($scope.tree['book']['book-meta']['pub-date']['date']);
        };
        $scope.saveDate = function(data){
            $scope.tree['book']['book-meta']['pub-date']['year'] = data.getYear().toString();
            $scope.tree['book']['book-meta']['pub-date']['month'] = (data.getMonth() + 1).toString();
            $scope.tree['book']['book-meta']['pub-date']['date'] = data.getDate().toString();
        };

        // validation
        $scope.isEmpty = function(data){
          if(!data){
              return "required!"
          }
        };

        // Check Array
        $scope.isArray = function(obj){
            if(obj){
                return angular.isArray(obj);
            }
            return false;
        };

        // Check Object's Key
        $scope.hasOwnProperty = function(obj, key){
            if(obj){
                return obj.hasOwnProperty(key);
            }
            return false;
        };

        $scope.date = function(obj){
             new Date
        }

    }]
);


/* jstree controller */
metadata.controller('jstreeCtrl',
    ['$scope', '$timeout', 'JsonData', function($scope, $timeout, JsonData) {
        $scope.tree = JsonData.tree;

        // jsTree config
        $scope.typesConfig = {
            "book": {
                "icon": "glyphicon glyphicon-folder-open"
            },
            "part": {
                "icon": "glyphicon glyphicon-folder-open"
            },
            "chapter": {
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
            angular.forEach($scope.tree, function(value, i){
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

