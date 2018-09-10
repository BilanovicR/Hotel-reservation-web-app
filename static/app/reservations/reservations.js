(function (angular) {
    var app = angular.module('HotelApp');
    app.controller('ReservationsCtrl', ['$http', 'loginService', '$state', function ($http, loginService, $state) {
        var that = this;
        that.user = {};
        that.loggedIn = false;
        that.authorized = false;
        that.message = "";
        that.reservations = []; //lista rezervacija
        that.reservation = {}; //konkretna rezervacija
        that.bill = {};


        loginService.isLoggedIn(function () {
            loginService.getLoggedIn(function (user) {
                that.user = user;
                loginService.authorized(that.user, function () {
                    that.authorized = true;
                }, function () {
                });
                if (that.authorized) {
                    that.getReservations();
                } else {
                    that.getMyReservations(that.user.id);
                };
                that.loggedIn = true;
            },
                function (reason) {
                })
        }, function () {
            that.loggedIn = false;
        });
        that.getMyReservations = function (id) {
            $http.get("/getMyReservations/" + id).then(function (response) {
                if (response.data[1]["success"] == true) {
                    that.reservations = response.data[0];
                    that.reservations.forEach(reservation => {
                        that.formatDate(reservation["arrival"]);
                        //console.log(reservation["arrival"]);
                        that.formatDate(reservation["departure"]);
                        //console.log(reservation["departure"]);
                    });
                    that.message = "Your reservations:";
                } else {
                    that.message = "No reservations";
                }
            },
                function (reason) {
                    console.log(reason);
                })
        };
        that.cancelReservation = function (id) {
            if (confirm("Are you sure you want to cancel this reservation?")) {
                $http.post("/cancelReservation/" + id).then(function (response) {
                    if (response.data["status"] == "done") {
                        console.log("reservation successfully cancelled");
                        $state.go("reservations");
                    } else {
                        console.log("error trying to cancel reservation");
                    }
                }, function (reason) {
                    console.log(reason);
                })
            }

        };
        that.formatDate = function (date) {
            var dateOut = new Date(date);
            return dateOut;
        };
        that.getReservations = function () {
            $http.get("/getReservations").then(function (response) {
                if (response.data[1]["success"] == true) {
                    that.reservations = response.data[0];
                    that.reservations.forEach(reservation => {
                        that.formatDate(reservation["arrival"]);
                        //console.log(reservation["arrival"]);
                        that.formatDate(reservation["departure"]);
                       // console.log(reservation["departure"]);
                    });
                    that.message = "Reservations:";
                } else {
                    that.message = "No reservations";
                }
            }, function (reason) { })
        };
        that.viewBill = function (bid) {
            $http.get("/getBill/" + bid).then(function (response) {
                that.bill = response.data[0];
                console.log(that.bill);
    
             }, function (reason) { })
    
        };
    }]);

    
})(angular);