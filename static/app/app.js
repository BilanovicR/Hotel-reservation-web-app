
(function (angular) {
    var app = angular.module('HotelApp', ['ui.router', 'loginService', 'ui.bootstrap']);

    app.config(['$stateProvider', '$urlRouterProvider', function ($stateProvider, $urlRouterProvider) {
        $urlRouterProvider.otherwise('/');
        $stateProvider.state('app', {
            abstract: true,
            views: {
                //Navbar se prikazuje na svakoj stranici.
                navbar: {
                    templateUrl: 'app/navbar/navbar.tpl.html',
                    controller: 'NavbarCtrl',
                    controllerAs: 'nbctrl'
                },
                '': {
                    template: '<ui-view name=""></ui-view>'
                }
            }
        })
        $stateProvider.state('home', {
            url: '/',
            parent: 'app',
            views: {
                '': {
                    templateUrl: 'app/home/home.tpl.html',
                    controller: 'HomeCtrl',
                    controllerAs: 'homectrl'
                }
            }
        }).state('amenities', {            
            url: '/amenities',
            parent: 'app',
            views: {
                '': {
                    templateUrl: 'app/amenities/amenities.tpl.html'
                }
            }
        }).state('login', {
            parent: 'app',
            url: '/login',
            views: {
                '': {
                    templateUrl: 'app/login/login.tpl.html',
                    controller: 'LoginCtrl',
                    controllerAs: 'lc'
                }
            }
        }).state('membership', {            
            url: '/membership',
            parent: 'app',            
            views: {
                '': {
                    templateUrl: 'app/membership/membership.tpl.html',
                    controller: 'MembershipCtrl',
                    controllerAs: 'mctrl'
                }
            }
        }).state('reservations', {
            url: '/reservations',
            parent: 'app',            
            views: {
                '': {
                    templateUrl: 'app/reservations/reservations.tpl.html',
            controller: 'ReservationsCtrl',
            controllerAs: 'rctrl'
                }
            }
        }).state('guests', {
            url: '/guests',
            parent: 'app',            
            views: {
                '': {
                    templateUrl: 'app/guests/guests.tpl.html',
            controller: 'GuestsCtrl',
            controllerAs: 'gctrl'
                }
            }
        }).state('admin_res', {
            url: '/admin_res',
            parent: 'app',            
            views: {
                '': {
                    templateUrl: 'app/admin_res/admin_res.tpl.html',
            controller: 'AdminCtrl',
            controllerAs: 'actrl'
                }
            }
        });
    }]);
})(angular);