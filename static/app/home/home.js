(function (angular) {
    var app = angular.module('HotelApp');
    app.controller('HomeCtrl', ['$http', 'loginService', '$state', '$scope', function ($http, loginService, $state, $scope) {
        var that = this;
        that.reservation = {
            arrival: '',
            departure: '',
            num_of_guests: '',
            guest_id: ''
        };
        that.user = {};
        that.loggedIn = false;
        that.authorized = false;
        arrivalId.min = new Date().toISOString().split("T")[0]; //ogranicavanje dolaska na najranije danasnji dan
        that.message = "";
        that.availableRooms = {};


        loginService.isLoggedIn(function () {
            loginService.getLoggedIn(function (user) {
                that.user = user;
                that.loggedIn = true;
                that.reservation.guest_id = that.user.id;
            },
                function (reason) {
                })
        }, function () { that.loggedIn = false; }
        );

        that.getReservation = function () {
            $http.get("/getReservation").then(function (reservation) {
                that.reservation = reservation.data;
                that.reservation.arrival = new Date(reservation.data.arrival);
                that.reservation.departure = new Date(reservation.data.departure);
            },
                function (reason) {
                    console.log("no pending reservation");
                });
        };

        that.checkAvailability = function () {
            if (that.reservation.arrival >= new Date() && that.reservation.arrival < that.reservation.departure) {
                $http.put("/requestedReservation", that.reservation).then(function (response) {
                    //console.log(response.data["success"]);
                    if (response.data["success"]) {
                        if (that.loggedIn) {
                            if (confirm("Confirm your request for a reservation")) {
                                that.makeReservation(that.reservation);
                            } else {
                                $state.go('home');
                            }

                        } else {
                            confirm("To proceed with your reservation please login or register");
                            $state.go('login');
                        }
                    } else {
                        that.message = "No available rooms, please try with different dates";
                        $state.go('home');
                    }
                }, function (reason) {
                    confirm("No available rooms for given dates, please try with different dates");
                    console.log(reason);
                    $state.go('home');
                })
            } else {
                that.message = "Invalid dates";
            };
        };

        that.makeReservation = function () {
            if (that.reservation.arrival >= new Date() || that.reservation.arrival < that.reservation.departure) {
                $http.post("/makeReservation", that.reservation).then(function (response) {
                    confirm("You have successfully made a reservation");
                    $state.go('reservations');
                },
                    function (reason) {
                        console.log(reason);
                    })
            } else {
                that.message = "Invalid dates";
            };
        };
        that.getReservation();

    }]);
})(angular);