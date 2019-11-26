var listener = new window.keypress.Listener()

var my_list = listener.register_many([
	{
		"keys": "w",
		"is_exclusive": true,
		"on_keydown" : function() {
			console.log("up");
			$.ajax({
				dataType: "json",
				url: "up"
			})
		},
	},
	{
		"keys": "s",
		"is_exclusive": true,
		"on_keydown" : function() {
			$.ajax({
				dataType: "json",
				url: "down"
			})
			console.log("down");
		},
	},
	{
		"keys": "a",
		"is_exclusive": true,
		"on_keydown" : function() {
			$.ajax({
				dataType: "json",
				url: "left"
			})
			console.log("left");
		},
	},
	{
		"keys": "d",
		"is_exclusive": true,
		"on_keydown" : function() {
			$.ajax({
				dataType: "json",
				url: "right"
			})
			console.log("right");
		},
	},
	{
		"keys": "f",
		"is_exclusive": true,
		"on_keydown" : function() {
			$.ajax({
				dataType: "json",
				url: "z_up"
			})
			console.log("z_up");
		},
	},
	{
		"keys": "h",
		"is_exclusive": true,
		"on_keydown" : function() {
			$.ajax({
				dataType: "json",
				url: "z_down"
			})
			console.log("z_down");
		},
	},
	{
		"keys": "i",
		"is_exclusive": true,
		"on_keydown" : function() {
			$.ajax({
				dataType: "json",
				url: "swipe_up"
			})
			console.log("swipe_up");
		},
	},
	{
		"keys": "k",
		"is_exclusive": true,
		"on_keydown" : function() {
			$.ajax({
				dataType: "json",
				url: "swipe_down"
			})
			console.log("swipe_down");
		},
	},
	{
		"keys": "j",
		"is_exclusive": true,
		"on_keydown" : function() {
			$.ajax({
				dataType: "json",
				url: "swipe_left"
			})
			console.log("swipe_left");
		},
	},
	{
		"keys": "l",
		"is_exclusive": true,
		"on_keydown" : function() {
			$.ajax({
				dataType: "json",
				url: "swipe_right"
			})
			console.log("swipe_right");
		},
	},
	{
		"keys": "p",
		"is_exclusive": true,
		"on_keydown" : function() {
			$.ajax({
				dataType: "json",
				url: "power_tap"
			})
			console.log("power_tap");
		},
	},
	{
		"keys": "delete",
		"is_exclusive": true,
		"on_keydown" : function() {
			$.ajax({
				dataType: "json",
				url: "power_hold"
			})
			console.log("power_hold");
		},
	},
	{
		"keys": "space",
		"is_exclusive": true,
		"on_keydown" : function() {
			$.ajax({
				dataType: "json",
				url: "tap"
			})
			console.log("tap");
		},
	},
]);
	
