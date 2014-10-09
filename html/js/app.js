/*
 * jQuery File Upload Plugin Angular JS Example 1.2.1
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2013, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://www.opensource.org/licenses/MIT
 */

/* jshint nomen:false */
/* global window, angular */

(function () {
    'use strict';

    var url = './php/';

    angular.module('demo', ['blueimp.fileupload', 'ui.bootstrap'])
    .config([
        '$httpProvider', 'fileUploadProvider',
        function ($httpProvider, fileUploadProvider) {
            delete $httpProvider.defaults.headers.common['X-Requested-With'];
            fileUploadProvider.defaults.redirect = window.location.href.replace(
                /\/[^\/]*$/,
                './redirect.html?%s'
            );
            angular.extend(fileUploadProvider.defaults, {
                // Enable image resizing, except for Android and Opera,
                // which actually support image resizing, but fail to
                // send Blob objects via XHR requests:
                disableImageResize: /Android(?!.*Chrome)|Opera/
                    .test(window.navigator.userAgent),
                maxFileSize: 5000000,
                acceptFileTypes: /(\.)(docx?|odt|jpe?g|png|gif|tiff|eps|wav|mp3|mp4)$/i,
                dataType: 'json'
            });
        }
    ])

    .controller('DemoFileUploadController', [
        '$scope', '$http', '$filter', '$window',
        function ($scope, $http) {
            $scope.options = {
                url: url
            };
            $scope.loadingFiles = true;
            $http.get(url)
                .then(
                function (response) {
                    $scope.loadingFiles = false;
                    $scope.queue = response.data.files || [];
                },
                function () {
                    $scope.loadingFiles = false;
                }
            );
        }
    ])

    .controller('FileDestroyController', [
        '$scope', '$http',
        function ($scope, $http) {
            var file = $scope.file,
                state;
            if (file.url) {
                file.$state = function () {
                    return state;
                };
                file.$destroy = function () {
                    state = 'pending';
                    return $http({
                        url: file.deleteUrl,
                        method: file.deleteType
                    }).then(
                        function () {
                            state = 'resolved';
                            $scope.clear(file);
                        },
                        function () {
                            state = 'rejected';
                        }
                    );
                };
            } else if (!file.$cancel && !file._index) {
                file.$cancel = function () {
                    $scope.clear(file);
                };
            }
        }
    ])

    // lock browser monitor during typesetting
    .controller('modalCtrl', [
        '$scope', '$modal', '$window',
        function($scope, $modal, $window) {
            $scope.open = function (path) {
                // redirect to the given path
                $window.location.href = path;
                // lock browser monitor
                $modal.open({
                    templateUrl: 'loading.html',
                    backdrop: 'static',
                    keyboard: false,
                    size: 'sm'
                });
            }
        }
    ]);

}());
