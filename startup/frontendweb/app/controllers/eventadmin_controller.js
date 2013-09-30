App.EventadminController = Ember.ArrayController.extend({
    actions: {
	parseEvent: function () {
	    var url = "http://blizrd.com/event-url/?event-url=" + this.get('event-url');
	    var self = this;
	    var store = this.store;
	    jQuery.getJSON(url, function(json) {
		// Create the new Todo model
		console.log(json[0]);
		var event = store.createRecord('event', json[0]);
		event.save();
		self.transitionToRoute('events');
	    });	 
	}
    }
});

