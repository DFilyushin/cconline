/**
 * Created by Filyushin_DV on 20.01.2016.
 */
var vikingApp=angular.module('vikingApp').config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

vikingApp.controller('NurseController',
    function NurseController($scope, $http) {
        $scope.id_history = 0;
        $scope.selectedTemplate=null;
        $scope.tableVisible = false;
        $scope.isCito = false;
        $scope.dayView = 'today';
        $scope.nurseWork = [];

        $scope.init = function(id)
        {
            $scope.id_history = id;
        };

        $scope.getRefreshData = function(){
            $http(
                {
                    url: "/json/nurse/",
                    method: "GET",
                    params: {p: $scope.dayView, id: $scope.id_history}
                })
                    .success(function(data){
                        $scope.nurseWork = data;
                }
                );
        };



    });
