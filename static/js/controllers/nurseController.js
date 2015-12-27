/**
 * Created by filyushin_dv on 08.12.2015.
 */

var myApp=angular.module('myApp').config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

myApp.controller('NurseController',
    function NurseController($scope, $http) {
        var curDate = new Date();

        $scope.labWork = {};
        $scope.medWork = {};
        $http(
            {
                url: "/json/nurse_work_lab/",
                method: "GET",
                params: {d: 19, p: 'today'}
            })
                .success(function(data){
                    $scope.labWork = data;
            }
            );

        $http(
            {
                url: "/json/nurse_work_med/",
                method: "GET",
                params: {d: 19, p: 'today'}
            })
                .success(function(data){
                    $scope.medWork = data;
            }
            );

    });
