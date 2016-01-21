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
        $scope.datavalue = {};
        $scope.datavalue.mode = 'today';
        $scope.nurseWork = [];
        $scope.dates = [
            {value: 'yesterday', label: 'Вчера'},
            {value: 'today', label: 'Сегодня'},
            {value: 'tomorrow', label: 'Завтра'}
        ];

        $scope.init = function(id)
        {
            $scope.id_history = id;
        };

        $scope.setDateValue = function(val){
          $scope.datavalue.mode = val;
        };

        $scope.getRefreshData = function(){
            $http(
                {
                    url: "/json/nurse/",
                    method: "GET",
                    params: {period: $scope.datavalue.mode, id: $scope.id_history}
                })
                    .success(function(data){
                        $scope.nurseWork = data;
                }
                );
        };
        $scope.executeNurse = function (idx, typeAssign) {
            $http(
                {
                    url: "/json/nurse_execute/",
                    method: 'POST',
                    data: { t: typeAssign, id:$scope.nurseWork[idx].pk  }
                });
            $scope.nurseWork.splice(idx, 1);

        };


    });
