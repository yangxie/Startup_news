define([
    'jquery',
    'underscore',
    'backbone', 
    "text!app/auth/templates/login.html",
    "text!app/auth/templates/login_successful.html"
], function($, _, Backbone, loginTemplate, loginSuccessfulTemplate) {

    var bindLogout = function() {
	$('#logout-link').click(function(event){
	    // Maybe show a loading indicator...
	    var form = $('#logout-form');
	    $.post(form.attr('action'), form.serialize(), function(res) {
		console.log(res);
		loginView();
	    });
	    return false; // prevent default action
	});
    };

    var logoutView = function() {
	var csrftoken = getCookie('csrftoken');
	var template =
	    _.template(
		loginSuccessfulTemplate,
		{csrftoken : csrftoken, username : 'edison'});
	$('#auth-div').html(template);
	bindLogout();
    }

    var bindLogin = function() {
	$('#login-form').submit(function(){
	    // Maybe show a loading indicator...
	    $.post($(this).attr('action'), $(this).serialize(), function(res){
		// Do something with the response `res`
		alert('sent.');
		console.log(res);
		logoutView();
		console.log(res);
		// Don't forget to hide the loading indicator!
	    });
	    return false; // prevent default action
	});
    };

    var loginView = function() {
	var csrftoken = getCookie('csrftoken');
	var template = _.template(loginTemplate, {csrftoken : csrftoken});
	$('#auth-div').html(template);
	bindLogin();
    }

    // using jQuery
    function getCookie(name) {
	var cookieValue = null;
	if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
		var cookie = jQuery.trim(cookies[i]);
		// Does this cookie string begin with the name we want?
		if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
		}
            }
	}
	return cookieValue;
    }

    var initialize = function(){
	loginView();
    };

    return { 
	initialize: initialize
    };
});