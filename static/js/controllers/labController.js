/**
 * Created by filyushin_dv on 08.12.2015.
 */

var myApp=angular.module('myApp').config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

myApp.controller('LabController',
    function LabController($scope, $http) {
        var months =
            ["январь", "февраль", "март", "апрель", "май", "июнь", "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"];
        var curDate = new Date();

        $scope.id_history = 0;
        $scope.currentYear=curDate.getFullYear();
        $scope.currentMonth = months[ curDate.getMonth()];
        $scope.currentDay=curDate.getDate();
        $scope.currentHour=curDate.getHours();
        $scope.currentMin=curDate.getMinutes();
        $scope.selectedPk=null;
        $scope.subTest= {};
        $scope.listMonths = months;
        $scope.tableVisible = false;

        $http.get('/json/test').success(function(data) {
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
        }

        $scope.sendData = function(){
            listTests = [];
            for (i=0; i<$scope.subTest.length; i++){
                if ($scope.subTest[i].fields.checked == true){
                    listTests.push($scope.subTest[i].pk);
                }
            };
            var dataForSend = new Object();
            dataForSend.pk = $scope.selectedPk;
            dataForSend.selected = listTests;
            dataForSend.id_history = 100;
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
        }
    });
