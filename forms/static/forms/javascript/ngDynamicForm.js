var app = angular.module('ngDynamicForms',[]);
// this is needed for posting data to django, to avoid csrftoken error
app.config(function($httpProvider) {
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
app.controller('FormBuilderCtrl',function FormBuilderCtrl($scope, $http, $location, $window)
{
	$scope.newField = {};
	$scope.fields = [ {
		type : 'text',
		name : 'Name',
		placeholder : 'Please enter your name'
	} ];
	$scope.editing = false;
	$scope.tokenize = function(slug1, slug2) {
		var result = slug1;
		result = result.replace(/[^-a-zA-Z0-9,&\s]+/ig, '');
		result = result.replace(/-/gi, "_");
		result = result.replace(/\s/gi, "-");
		if (slug2) {
			result += '-' + $scope.token(slug2);
		}
		return result;
	};
	$scope.saveField = function() {
		console.log("entered save");
		if ($scope.newField.type == 'checkboxes') {
			$scope.newField.value = {};
		}
		if ($scope.editing !== false) {
			$scope.fields[$scope.editing] = $scope.newField;
			$scope.editing = false;
		} else {
			$scope.fields.push($scope.newField);
		}
		$scope.newField = {
		};
	};
	$scope.editField = function(field) {
		$scope.editing = $scope.fields.indexOf(field);
		$scope.newField = field;
	};
	$scope.splice = function(field, fields) {
		fields.splice(fields.indexOf(field), 1);
	};
	$scope.addOption = function() {
		if ($scope.newField.options === undefined) {
			$scope.newField.options = [];
		}
		$scope.newField.options.push({
		});
	};
	$scope.typeSwitch = function(type) {
		/*if (angular.Array.indexOf(['checkboxes','select','radio'], type) === -1)
			return type;*/
		if (type == 'checkboxes')
			return 'multiple';
		if (type == 'select')
			return 'multiple';
		if (type == 'radio')
			return 'multiple';

		return type;
	};
	
	$scope.createForm = function() {
	    console.log('create form');
	    $http({
            method: 'POST',
            url: '/accounts/createform/',
            data: $scope.fields,
            headers: {
                'Content-Type': 'application/json; charset=utf-8'
            }
          }).success(function (data) {
              $window.location.href = '/accounts';
            //$location.path('^/accounts');
          });
	   //$http.post('/accounts/createform/', $scope.fields).then(function(data) {
	   //    $location.path
	   //})
	   ////.then(function(data){
	   //    console.log('created the form');
	   //    $location.path("/accounts")
	   // });
	}
});

app.directive('ngDynamicForm', function () { 
    return { 
        // We limit this directive to attributes only.
         restrict : 'A',

        // We will not replace the original element code
        replace : false,
        
        // We must supply at least one element in the code 
        templateUrl : '/static/forms/javascript/dynamicForms.html'
    } 
});

// app.controller('FormDisplayCtrl', ['$scope', '$http', '$location', '$window', function ($scope, $http, $location, $window)
// {
	
// 	console.log($scope.fields);
	
// 	$scope.$watch('fields', function(newvalue) {
// 	}, true);
	
// 	$scope.submitForm = function(isValid){
// 		console.log('inside the submit form');
// 		if(isValid) {
// 			console.log('submit form');
// 	    $http({
//             method: 'POST',
//             url: '/accounts/shareform/'+$scope.id + '/',
//             data: $scope.fields,
//             headers: {
//                 'Content-Type': 'application/json; charset=utf-8'
//             }
//           }).success(function (data) {
//               $window.location.href = '/accounts/thanks';
//             //$location.path('^/accounts');
//           });

// 		} else {
// 			console.log('not valid');
// 		}
// 	}
	
// }]);
