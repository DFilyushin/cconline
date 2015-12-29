/**
 * Created by DFilyushin on 19.12.2015.
 */
'use strict';

var nurseControllers = angular.module('nurseControllers', []);

nurseControllers.controller('LabCtrl', ['$scope', '$http', '$rootScope',
    function($scope, $http, $rootScope) {
        $rootScope.labClass = "active";
        $rootScope.examClass = "";
        $rootScope.drugClass = "";
        $rootScope.doctorClass = "";
        $scope.labWork = [];
        $scope.dayTitle = new Date();

        /*$http(
            {
                url: "/json/nurse_work_lab/",
                method: "GET",
                params: {d: 19, p: 'today'}
            })
                .success(function(data){
                    $scope.labWork = data;
            }
            );
        */
        $scope.getRefreshData = function(){
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
        }

    }]);

nurseControllers.controller('ExamCtrl', ['$scope', '$http', '$rootScope',
    function($scope, $http, $rootScope) {
        $rootScope.labClass = "";
        $rootScope.examClass = "active";
        $rootScope.drugClass = "";
        $rootScope.doctorClass = "";
        $scope.examens = [];

        $scope.getRefreshData = function(){
            $http(
                {
                    url: "/json/nurse_work_exam/",
                    method: "GET",
                    params: {d: 19, p: 'today'}
                })
                    .success(function(data){
                        $scope.examens = data;
                }
                );
        }

    }]);

nurseControllers.controller('DrugCtrl', ['$scope', '$http', '$rootScope',
    function($scope, $http, $rootScope) {
        $rootScope.labClass = "";
        $rootScope.examClass = "";
        $rootScope.drugClass = "active";
        $rootScope.doctorClass = "";
        $scope.drugs = [];

        $scope.getRefreshData = function(){
            $http(
                {
                    url: "/json/nurse_work_med/",
                    method: "GET",
                    params: {d: 19, p: 'today'}
                })
                    .success(function(data){
                        $scope.drugs = data;
                }
                );
        }



    }]);

nurseControllers.controller('DoctorCtrl', ['$scope', '$http', '$rootScope',
    function($scope, $http, $rootScope) {
        $rootScope.labClass = "";
        $rootScope.examClass = "";
        $rootScope.drugClass = "";
        $rootScope.doctorClass = "active";
        $scope.profview = [];


        $scope.getRefreshData = function(){
            $http(
                {
                    url: "/json/nurse_work_doc/",
                    method: "GET",
                    params: {d: 19, p: 'today'}
                })
                    .success(function(data){
                        $scope.profview = data;
                }
                );

        }
    }]);