App.Event = DS.Model.extend({
    name: DS.attr('string'),
    description: DS.attr('string'),
    category: DS.attr('string'),
    start_date: DS.attr('string'),
    start_time: DS.attr('string'),
    end_date: DS.attr('string'),
    end_time: DS.attr('string'),
    event_address: DS.attr('string'),
    place: DS.attr('string'),
    address_line1: DS.attr('string'),
    address_line2: DS.attr('string'),
    city: DS.attr('string'),
    state: DS.attr('string'),
    postal_code: DS.attr('string'),
    URL: DS.attr('string'),
    coupon: DS.attr('string'),
    status: DS.attr('string')
});

App.Event.FIXTURES = [
    {
	id: 1,
	name: 'test',
	category: 'a',
	address_line1: 'b',
	address_line2: 'test_address',
	city: 'mountain view',
	state: 'CA',
	start_date: 'today',
	start_time: '3:00',
	end_date: 'today',
	end_time: '3:00'
    },
    {
	id: 2,
	name: 'test2',
	category: 'a',
	address_line1: 'b',
	address_line2: 'c',
	city: 'mountain view',
	state: 'CA',
	start_date: 'today',
	start_time: '3:00',
	end_date: 'today',
	end_time: '3:00'
    },
    {
	id: 3,
	name: 'test3',
	event_address: 'test_address',
	category: 'a',
	address_line1: 'b',
	city: 'mountain view',
	state: 'CA',
	start_date: 'today',
	start_time: '3:00',
	end_date: 'today',
	end_time: '3:00'
    }
];