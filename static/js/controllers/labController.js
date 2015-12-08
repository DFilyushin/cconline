/**
 * Created by filyushin_dv on 08.12.2015.
 */

var myApp=angular.module('myApp');

myApp.controller('LabController',
    function LabController($scope, $http) {
        $scope.selectedPk=null;
        $scope.subTest= {};
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
                    $scope.subTest.fields.checked = false;
            }

            )
        }

        $scope.sendData = function(){

        }

    });