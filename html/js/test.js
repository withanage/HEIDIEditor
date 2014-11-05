'use strict';

var components = ['textAngular', 'jsTree.directive', 'xeditable', 'ui.bootstrap'];
var metadata = angular.module('metadata', components);


// xeditable config
metadata.run(function(editableOptions, editableThemes) {
    // set `default` theme
    editableOptions.theme = 'bs3';

    // overwrite button templates
    editableThemes['bs3'].submitTpl = '<button type="submit" class="btn btn-primary">save</button>';
    editableThemes['bs3'].cancelTpl = '<button type="button" class="btn btn-default" ng-click="$form.$cancel()">cancel</button>';
});



metadata.factory('JsonData', function(){
    return {
        tree: null,
        selected: null,
        pubType : ['pdf', 'epub', 'html'],
        dateType : ['created', 'reviewed', 'updated'],
        idType : [
            { name: 'archive', info: 'Identifier assigned by an archive or other repository for articles' },
            { name: 'aggregator', info: 'Identifier assigned by a data aggregator' },
            { name: 'doaj', info: 'Directory of Open Access Journals'},
            { name: 'doi', info: 'Digital Object Identifier for the entire journal, not just for the article (rare)' },
            { name: 'index', info: 'Identifier assigned by an abstracting or indexing service' },
            { name: 'publisher-id', info: 'Identifier assigned by the content publisher, for example, "HeiPUB"'},
            { name: 'other', info: ''}
        ],
        contribType : ['author', 'editor', 'translator', 'designer']

    };
});

metadata.controller('textCtrl',
    ['$scope', '$http', '$filter', 'JsonData', function($scope, $http, $filter, JsonData){
        console.log('textCtrl');
        // json data
        $http.get("../cgi/bookJson.py").success(function(data){
            $scope.tree = data;
            JsonData.tree = data;
        });

        // initial values
        $scope.pubType = JsonData.pubType;
        $scope.dateType = JsonData.dateType;
        $scope.today = $filter('date')(new Date(),'yyyy-MM-dd');
        $scope.idType = JsonData.idType;
        $scope.contribType = JsonData.contribType;


        // validation
        $scope.isEmpty = function(data){
          if(!data){
              return "required!"
          }
        };

        $scope.booktree = {selected : ''};


        $scope.$watch('booktree', function(newVal, oldVal) {
            console.log('watch!'+newVal.selected);
        },true);

    }]
);


/* jstree controller */
metadata.controller('jstreeCtrl',
    ['$scope','$timeout', 'JsonData', function($scope, $timeout, JsonData) {
        console.log('jstreeCtrl');
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
            $scope.booktree.selected = data.selected[0];
            $timeout(function() { //dummy function!
            }, 0);
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
        $scope.contents = JsonData.tree;

        $scope.close = function(){
            JsonData.tree = $scope.contents;
            $modalInstance.close();
        };
        $scope.cancel = function(){
            $modalInstance.dismiss('cancel');
        };
    }]
);

