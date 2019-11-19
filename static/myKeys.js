var listener = new window.keypress.Listener()

var my_list = listener.register_many([
	{
		"keys": "up",
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
		"keys": "down",
		"is_exclusive": true,
		"on_keydown" : function() {
			console.log("down");
		},
	},
	{
		"keys": "left",
		"is_exclusive": true,
		"on_keydown" : function() {
			console.log("left");
		},
	},
	{
		"keys": "right",
		"is_exclusive": true,
		"on_keydown" : function() {
			console.log("right");
		},
	}
]);
	
