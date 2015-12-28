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
    }]);

nurseControllers.controller('ExamCtrl', ['$scope', '$http', '$rootScope',
    function($scope, $http, $rootScope) {
        $rootScope.labClass = "";
        $rootScope.examClass = "active";
        $rootScope.drugClass = "";
        $rootScope.doctorClass = "";
        $scope.examens = [];

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

    }]);

nurseControllers.controller('DrugCtrl', ['$scope', '$http', '$rootScope',
    function($scope, $http, $rootScope) {
        $rootScope.labClass = "";
        $rootScope.examClass = "";
        $rootScope.drugClass = "active";
        $rootScope.doctorClass = "";
        $scope.drugs = [];

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

    }]);

nurseControllers.controller('DoctorCtrl', ['$scope', '$http', '$rootScope',
    function($scope, $http, $rootScope) {
        $rootScope.todayClass = "";
        $rootScope.tomorrowClass = "";
        $rootScope.monthClass = "";
        $rootScope.annivClass = "active";
        $scope.employers = [];
        $http.get('employers/employers.json').success(function(data) {
            var date1;
            var curDate = new Date();
            $scope.dayTitle = curDate;
            angular.forEach(data, function(value, key) {
                date1 = new Date(value.dob);
                if (date1.getMonth()+1 == curDate.getMonth()+1){
                    var age = new Date(new Date - date1).getFullYear()-1970;
                    if (date1.getDate() < curDate.getDate()){
                        if ((age % 5 == 0) || (age % 10 == 0)){
                            value['age'] = age;
                            value['sign'] = getZodiacSign(date1);
                            $scope.employers.push(value);
                        }
                    }
                }
            });
        });
    }]);