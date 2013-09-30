App.EventFilterRoute = Em.Route.extend({
    renderTemplate: function() {
        this.render({outlet: 'sidebar'});   
    },
    model: function() {
	return ['red', 'yellow', 'blue'];
    }
});