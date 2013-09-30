App.LoginView = Ember.View.extend({
    templateName: 'login',

    csrftoken : function() {
	var token = getCookie('csrftoken');
	return token;
    }.property()
});