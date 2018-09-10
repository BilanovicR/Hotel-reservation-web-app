(function (angular) {
    var app = angular.module('HotelApp');
    app.controller('MembershipCtrl', ['$http','loginService', '$state', function($http, loginService, $state) {
        var that = this;
        that.user = {
            'id': '',
            'first_name': '',
            'last_name': '',
            'date_of_birth': '',
            'gender': '',
            'email': '',
            'username': '',
            'password': '',
            'role_id': ''
        };
        that.loggedIn = false;
        that.failed = false;

        loginService.isLoggedIn(function () {
                loginService.getLoggedIn(function (user) {
                    that.user = user;
                    that.loggedIn = true;
                    that.user.date_of_birth = new Date(user.date_of_birth);
                },
                function (reason) {
                })
            },function() {that.loggedIn = false;}
        );

            that.register = function () {
                $http.post("/register", that.user).then(function(response){
                    that.loggedIn = true;
                    that.login();
                },
                function(reason){
                    console.log(reason);
                })
            };
            that.login = function() {
                loginService.login(that.user, function() {
                    that.user.password = ""
                    $state.go('home');
                },
                function() {
                    that.failed = true;
                    that.loggedIn = false;
                })
            };
            that.updateProfile = function() {
                $http.put("/updateProfile", that.user).then(function(response){
                    that.loggedIn = true;
                    that.login();
                },
                function(reason){
                    console.log(reason);
                })
            };

    }]);
})(angular);