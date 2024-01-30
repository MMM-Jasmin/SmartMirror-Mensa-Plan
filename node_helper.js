var NodeHelper = require('node_helper');
var request = require('request');
const {PythonShell} = require('python-shell');

module.exports = NodeHelper.create({
	start: function () {
		console.log('MMM-JsonTable helper started...');
	},

	getMensaJSON: function (){
		const self = this;

		console.log("Mensa request to Studierendenwerk!");
		self.pyshell = new PythonShell('modules/' + this.name + '/mensa_requests/mensa_json.py', { pythonPath: 'python3', mode: 'json'});

		self.pyshell.on('message', function (message) {
			//console.log(message)
			self.sendSocketNotification("smartmirror-mensa-plan_JSON_RESULT", message);
        });
	},

	//Subclass socketNotificationReceived received.
	socketNotificationReceived: function (notification, arg) {
		console.log("socketNotification");
		if (notification === "smartmirror-mensa-plan_GET_JSON") {
			console.log("smartmirror-mensa-plan_GET_JSON got called");
			this.getMensaJSON();
		}
	},

	stop: function() {
		const self = this;
		self.pyshell.childProcess.kill('SIGKILL');
		self.pyshell.end(function (err) {
           	if (err){
        		//throw err;
    		};
    		console.log('finished');
		});
	}
});
