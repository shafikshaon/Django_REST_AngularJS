'use strict';

confirmClickModule.directive('confirmClick', function(){
  return {
    restrict: "A",
    link: function(scope, element, attr){
      var msg = attr.confirmClick || "Are you sure?";
      var clickAction = attr.confirmedClick;
      element.bind('click', function(){
        if (window.confirm(msg)){
          event.stopImmediatePropagation();
          event.preventDefault();
          scope.$eval(clickAction);
        }
        else {
          console.log('cancelled')
        }
      });
    },
  };
});



// confirmClickModule.directive('confirmClick', function($rootScope, $location){
//   return {
//     scope: {
//       message: "@message",
//       eq: "=eq",
//       post: "=post",
//     },
//     restrict: "E",
//     template: "<a ng-href='#'>{{ post.title }}</a>",
//     link: function(scope, element, attr){
// 
//       var msg = scope.message || "Are you sure?";
//       element.bind('click', function(){
//         if (window.confirm(msg)){
//           console.log("/blog/" + scope.post.id)
//           $rootScope.$apply(function(){
//             $location.path("/blog/" + scope.post.id);
//           });
//         }
//       });
// 
//       // console.log(scope.eq); // resolve a expressão e retorna o resultado
//       // console.log(element);
//       // console.log(attr.eq); // retorna o atributo
//     },
//   };
// });
