(function (angular) {
    var app = angular.module('HotelApp');
    app.controller('NavbarCtrl', ['loginService', '$state', '$scope', function(loginService, $state, $scope) {
        var that = this;
        that.loggedIn = false;
        that.authorized = false;

        var onLogin = function() {
            that.loggedIn = true;
            loginService.getLoggedIn(function (user) {
                that.user = user;
                loginService.authorized(user, function() {
                    that.authorized = true;
                },function (){}
            )
            },
            function (errorReason) {
            })
        }

        var onLogout = function() {
            that.loggedIn = false;
            that.authorized = false;
        }
        var authorized = function(){
            that.authorized = true;
        }
        
        loginService.addLoginListener($scope, onLogin);
        loginService.addLogoutListener($scope, onLogout);
 
        that.logout = function() {
            loginService.logout(function(){
                $state.go('home');
            }, function(){});
        }

        loginService.isLoggedIn(function() {
            that.loggedIn = true;
            loginService.getLoggedIn(function (user) {
                that.user = user;
                loginService.authorized(user, function() {
                    that.authorized = true;
                },function (){}
            )
            },
            function (errorReason) {
            })
        },
        function() {
            that.loggedIn = false;
        });
    }]);
})(angular);