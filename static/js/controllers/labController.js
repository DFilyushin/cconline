/**
 * Created by filyushin_dv on 08.12.2015.
 */

var myApp=angular.module('myApp').config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

myApp.controller('LabController',
    function LabController($scope, $http) {
        var curDate = new Date();
        curDate.setMilliseconds(0);
        curDate.setSeconds(0);
        $scope.id_history = 0;
        $scope.selectedPk=null;
        $scope.subTest= {};
        $scope.tableVisible = false;
        $scope.isCito = false;
        $scope.plan_date2 = curDate;
        $scope.plan_time2 = curDate;

        $http(
            {
                method: 'GET',
                url: '/json/test',
                cache: true
            }).success(function(data) {
                    $scope.tests=data;
                });

        $scope.getSubTest = function(){
            $http(
            {
                url: "/json/subtest/",
                method: "GET",
                params: {q: $scope.selectedPk}
            })
                .success(function(data){
                    $scope.subTest = data;
                    $scope.tableVisible = ($scope.subTest.length > 0);
                    $scope.subTest.fields.checked = false;
            }
            )
        };

        $scope.sendData = function(){
            var i;
            var listTests = [];

            for (i=0; i<$scope.subTest.length; i++){
                if ($scope.subTest[i].fields.checked == true){
                    listTests.push($scope.subTest[i].pk);
                };
            };

            var dataForSend = new Object();
            dataForSend.pk = $scope.selectedPk;
            dataForSend.selected = listTests;
            dataForSend.id_history = document.getElementsByName('id_history')[0].value;
            dataForSend.plan_year = $scope.plan_date2.getFullYear();
            dataForSend.plan_month = $scope.plan_date2.getMonth();
            dataForSend.plan_day = $scope.plan_date2.getDate();
            dataForSend.plan_hour = $scope.plan_time2.getHours();
            dataForSend.plan_min = $scope.plan_time2.getMinutes();
            if ($scope.isCito == true){
                dataForSend.is_cito = 1;
            }
            else
            {
                dataForSend.is_cito = 0;
            }

            $http(
                {
                    url: "/json/posttest/",
                    dataType: 'JSON',
                    method: 'POST',
                    data: dataForSend,
                    headers: {
                        "Content-Type": "application/json"
                    }
                });
            window.location.replace("/laboratory/list/" + dataForSend.id_history);
        }
    });
