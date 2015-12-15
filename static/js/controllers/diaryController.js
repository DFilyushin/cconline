/**
 * Created by filyushin_dv on 08.12.2015.
 */

var myApp=angular.module('myApp').config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});

myApp.controller('DiaryController',
    function DiaryController($scope, $http) {
        $scope.id_history = 0;
        $scope.selectedTemplate=null;
        $scope.subTest= {};
        $scope.tableVisible = false;
        $scope.isCito = false;
        $scope.list_templates = {};

        $http.get('/json/templates/?g=11').success(function(data) {
            $scope.list_templates=data;
        });

        $scope.getTemplate = function(){
            $http(
            {
                url: "/json/templates/",
                method: "GET",
                params: {id: $scope.selectedTemplate}
            })
                .success(function(data){
                    //var target = document.getElementsById('id_diary_text');
                    str = data[0].fields.text
                    //alert(str);
                    document.getElementById('id_diary_text').value = str;

            }
            )

        }

    });
