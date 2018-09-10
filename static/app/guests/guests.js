(function (angular) {
    var app = angular.module('HotelApp');
    app.controller('GuestsCtrl', ['$http','loginService', '$state', function($http, loginService, $state) {
        var that = this;
        that.user ={};
        that.loggedIn = false;
        that.authorized = false;
        that.message = "";
        that.guests = []; //lista gostiju
        that.guest = {}; //konkretna gost

       
        loginService.isLoggedIn(function () {
            loginService.getLoggedIn(function (user) {                
                that.user = user; 
                loginService.authorized(that.user, function() {
                    that.authorized = true;
                    that.getGuests();
                },function (){
                });  
                that.loggedIn = true;
            },
            function (reason) {                
            })
        }, function() {
        that.loggedIn = false;
        });
        
        that.formatDate = function(date){
            var dateOut = new Date(date);
            return dateOut;
      };
      that.getGuests = function(){
          $http.get("/getGuests").then(function(response){
            if (response.data[1]["success"] == true) {
                that.guests = response.data[0];
                that.message = "Guests:";
            } else {
                that.message = "No registered guests"; 
            }  
          },function(reason){})
      }   
    }]);
})(angular);