App.EventsRoute = Ember.Route.extend({
    renderTemplate: function() {
	this.render('event_filter',{
            outlet:'sidebar'
        });
        this.render({outlet: 'main'});   
    },
    model: function() {
        this.controllerFor('events').set('selectedPage', 1);
//	return App.Event.find();
	return this.get( 'store' ).findAll('event');
//	console.log(App.Event.FIXTURES);
//	return App.Event.FIXTURES;
    }
});