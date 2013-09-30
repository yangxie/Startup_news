App.MenuItem = DS.Model.extend({
    name: DS.attr('string'),
    url: DS.attr('string')
});

App.MENU_FIXTURES = [
    {
	name: 'events',
	url: 'events',
	isactive: false
    },
    {
	name: 'event admin',
	url: 'eventadmin',
	isactive: false
    }
];