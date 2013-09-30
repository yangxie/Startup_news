App.MenuController = Ember.ArrayController.extend({
    loginFailed: false,
    isProcessing: false,
    actions : {
	login: function() {
	    var self=this;
	    self.setProperties({
		loginFailed: false,
		isProcessing: true
	    });

	    var username=this.get("email");
	    var password=this.get("password");
	    var token = getCookie('csrftoken');

	    $.post("login/", {
		username: username,
		password: password,
		csrfmiddlewaretoken: token
	    }).then(this.success.bind(this),
		    this.failure.bind(this));
	}
    },
    success: function() {
	this.reset();
//	document.location = "/welcome";
    },
    failure: function() {
	this.reset();
	this.set("loginFailed", true);
    },
    slowConnection: function() {
	this.set("isSlowConnection", true);
    },
    reset: function() {
	clearTimeout(this.get("timeout"));
	this.setProperties({
	    isProcessing: false,
	    isSlowConnection: false
	});
    }
});
