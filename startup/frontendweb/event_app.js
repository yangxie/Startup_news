// Require.js allows us to configure shortcut alias
// Their usage will become more apparent futher along in the tutorial.
require.config({
    paths: {
	jquery: 'jquery/jquery-1.10.2.min',
	underscore: 'underscore/underscore-min',
	backbone: 'backbone/backbone-min',
    }
});

require([
  // Load our app module and pass it to our definition function
    'core/event_view',
], function(App){
  // The "app" dependency is passed in as "App"
  // Again, the other dependencies passed in are not "AMD" therefore don't pass a parameter to this function
    App.initialize();
});