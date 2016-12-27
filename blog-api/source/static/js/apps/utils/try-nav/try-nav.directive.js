'use strict';

tryNavModule.directive('tryNav', function(Post, $cookies, $location){
  return {
    restrict: "E",
    templateUrl: "/api/templates/nav.html",
    link: function(scope, element, attr){
      scope.items = Post.query();
      scope.selectItem = function($item, $model, $label){
        // console.log($item); // resource
        // console.log($model);
        // console.log($label);
        $location.path("/blog/" + $item.id);
        scope.searchQuery = "";
      };
      scope.searchItem = function(){
        $location.path("/blog/").search("q", scope.searchQuery);
        scope.searchQuery = "";
      };
      scope.userLoggedIn = false;
      scope.$watch(function(){
        var token = $cookies.get("token");
        if(token){
          scope.userLoggedIn = true;
        }
        else {
          scope.userLoggedIn = false;
        } 
      });
    },
  };
});


