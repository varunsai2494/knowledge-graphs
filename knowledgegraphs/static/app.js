var KnowledgeGraph = angular.module('KnowledgeGraph', ['ui.router', 'ui.select']);

KnowledgeGraph.config(function($stateProvider, $urlRouterProvider) {

    $urlRouterProvider.otherwise('/home');

    $stateProvider

        // HOME STATES AND NESTED VIEWS ========================================
        .state('home', {
            url: '/home',
            templateUrl: 'home.html',
            controller: 'HomeCtrl'
        })

        // ABOUT PAGE AND MULTIPLE NAMED VIEWS =================================
        .state('about', {
            // we'll get to this in a bit       
        })
});

KnowledgeGraph.controller('HomeCtrl', function($scope, $http, $q){
    $scope.saveStatus = false;
    $scope.sampleText = "Hello";
    $scope.sampleQuestion = {id: 0, text: 'Who is the Director of Interstellar?'};
    $scope.sampleAnswer = {id: 0, text: 'Christopher nolan directed this movie'};
    $scope.sampleQuestions = [
        {id: 0, text: 'Who is the Director of Interstellar?'},
        {id: 1, text: 'How did heath ledger act in Batman Begins?'}
    ];

    $scope.sampleAnswers = [
        {id: 0, text:"Christopher nolan directed this movie"},
        {id: 1, text:"Heath Ledger's Acting got 10 likes,3 dislikes and 2 neutral responses"}
    ];

    $scope.getAnswer = function(question){
        $http({
            method: 'POST',
            url: 'http://localhost:8000/qna',
            headers: {
                'content-type'  : 'application/json'
            },
            data: {
                'text': question
            }
        })
        .then(function(response) {
            console.log(response);
            $scope.userAnswer = response.data.text;
        }, function(error) {
            console.log("Submit works");
            console.log("Error in returning answer from database", error);
        });
    };

    $scope.updateKnowledge = function(text){
        $http({
            method: 'POST',
            url: 'http://localhost:8000/updategraph',
            headers: {
                'content-type'  : 'application/json'
            },
            data: {
                'text': text
            }
        }).then(function(response) {
            console.log(response);
            $scope.saveStatus = (response.data.text == "success") ? true : false;
        }, function(error) {
            console.log("Error in returning answer from database", error);
        });
    };




})