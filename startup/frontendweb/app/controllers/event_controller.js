App.EventController = Ember.ObjectController.extend({
    sameday: function(){
	var model = this.get('model');
	return model.start_date == model.end_date;
    }.property('model.sameday')
});
