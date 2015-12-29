'use strict';

/* App Module */

var nurseApp = angular.module('nurseApp', [
  'ngRoute',
  'nurseControllers'
]);

nurseApp.config(['$routeProvider',
  function($routeProvider) {
    $routeProvider.
      when('/lab', {
        templateUrl: '../../static/lab.html',
        controller: 'LabCtrl'
      }).
      when('/drug', {
        templateUrl: '../../static/drug.html',
        controller: 'DrugCtrl'
      }).
      when('/exam', {
        templateUrl: '../../static/exam.html',
        controller: 'ExamCtrl'
      }).
      when('/doctor', {
        templateUrl: '../../static/pview.html',
        controller: 'DoctorCtrl'
      }).
    otherwise({
        redirectTo: '/lab'
      });
  }]);

nurseApp.directive('afterRender', ['$timeout', function ($timeout) {
    var def = {
        restrict: 'A',
        terminal: true,
        transclude: false,
        link: function (scope, element, attrs) {
            $timeout(scope.$eval(attrs.afterRender), 0);  //Calling a scoped method
        }
    };
    return def;
}]);