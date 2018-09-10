(function (angular) {
    var app = angular.module('HotelApp');
    app.controller('LoginCtrl', ['loginService', '$state', function(loginService, $state) {
        var that = this;
        that.showLogin = false;
        that.failed = false;
        that.user = {
            //'username': '',
            //'password': ''
        };
        that.authorized = false;

        that.login = function() {
            loginService.login(that.user, function() {
                $state.go('membership');
                console.log("success login");
            },
            function() {
                that.failed = true;
            })
        }

        loginService.isLoggedIn(function() {
            $state.go('home');
        },
        function() {
            that.showLogin = true;
        });
    }]);
})(angular);