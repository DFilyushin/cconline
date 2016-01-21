/**
 * Created by DFilyushin on 19.12.2015.
 */
'use strict';

var nurseControllers = angular.module('nurseControllers', []).config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

nurseControllers.controller('LabCtrl', ['$scope', '$http', '$rootScope',
    function($scope, $http, $rootScope) {
        $rootScope.labClass = "active";
        $rootScope.examClass = "";
        $rootScope.drugClass = "";
        $rootScope.doctorClass = "";
        $scope.labWork = [];
        $scope.dayView = 'today';
        $scope.delete = function (idx) {
            $http(
                {
                    url: "/json/nurse_execute/",
                    method: 'POST',
                    data: { t: 2, id:$scope.labWork[idx].pk  }
                });
            $scope.labWork.splice(idx, 1);

        };
        $scope.getRefreshData = function(){
            $http(
                {
                    url: "/json/nurse_work_lab/",
                    method: "GET",
                    params: {p: $rootScope.datavalue.mode}
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
        $scope.delete = function (idx) {
            $http(
                {
                    url: "/json/nurse_execute/",
                    method: 'POST',
                    data: { t: 3, id:$scope.examens[idx].pk  }
                });
            $scope.examens.splice(idx, 1);

        };
        $scope.getRefreshData = function(){
            $http(
                {
                    url: "/json/nurse_work_exam/",
                    method: "GET",
                    params: {p: $rootScope.datavalue.mode}
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
        $scope.delete = function (idx) {
            $http(
                {
                    url: "/json/nurse_execute/",
                    method: 'POST',
                    data: { t: 1, id:$scope.drugs[idx].pk  }
                });
            $scope.drugs.splice(idx, 1);
        };

        $scope.getRefreshData = function(){
            $http(
                {
                    url: "/json/nurse_work_med/",
                    method: "GET",
                    params: {p: $rootScope.datavalue.mode}
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
        $scope.dayView = 'today';
        $scope.profview = [];
        $scope.delete = function (idx) {
            $http(
                {
                    url: "/json/nurse_execute/",
                    method: 'POST',
                    data: { t: 4, id:$scope.profview[idx].pk  }
                });
            $scope.profview.splice(idx, 1);

        };
        $scope.getRefreshData = function(){
            $http(
                {
                    url: "/json/nurse_work_doc/",
                    method: "GET",
                    params: {p: $scope.dayView}
                })
                    .success(function(data){
                        $scope.profview = data;
                }
                );
        }
    }]);
