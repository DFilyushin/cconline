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
        $scope.currentMonth = months[ curDate.getMonth() ];
        $scope.currentMonthI = 0;
        $scope.currentDay=curDate.getDate();
        $scope.currentHour=curDate.getHours();
        $scope.currentMin=curDate.getMinutes();
        $scope.selectedPk=null;
        $scope.subTest= {};
        $scope.listMonths = months;
        $scope.tableVisible = false;
        $scope.isCito = false;

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
            var i;
            var listTests = [];
            for (i=0; i<$scope.subTest.length; i++){
                if ($scope.subTest[i].fields.checked == true){
                    listTests.push($scope.subTest[i].pk);
                }
            };
            for(i=0; i<months.length; i++){
                if (months[i]==$scope.currentMonth){
                    $scope.currentMonthI = i+1;
                    break;
                }
            }

            var dataForSend = new Object();
            dataForSend.pk = $scope.selectedPk;
            dataForSend.selected = listTests;
            dataForSend.id_history = document.getElementsByName('id_history')[0].value;
            dataForSend.plan_year = $scope.currentYear;
            dataForSend.plan_month = $scope.currentMonthI;
            dataForSend.plan_day = $scope.currentDay;
            dataForSend.plan_hour = $scope.currentHour;
            dataForSend.plan_min = $scope.currentMin;
            if ($scope.isCito == true){
                dataForSend.is_cito = 1;
            }
            else
            {
                dataForSend.is_cito = 0
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
