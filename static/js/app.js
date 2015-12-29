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
