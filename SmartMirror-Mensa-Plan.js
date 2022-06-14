/**
 * @file smartmirror-mensa-plan.js
 *
 * @author nkucza
 * @license MIT
 *
 * @see  https://github.com/NKucza/smartmirror-mensa-plan
 */

'use strict';

Module.register("SmartMirror-Mensa-Plan", {

	jsonData: null,

	// Default module config.
	defaults: {
		mensa_parser: "",
		hour_offset: 10,
		updateInterval: 300000
	},

	start: function () {
		this.getJson();
		this.scheduleUpdate();
	},

	scheduleUpdate: function () {
		var self = this;
		setInterval(function () {
			self.getJson();
		}, this.config.updateInterval);
	},

	// Request node_helper to get json from a mensa parser script
	getJson: function () {
		this.sendSocketNotification("smartmirror-mensa-plan_GET_JSON", [this.config.mensa_parser, this.config.hour_offset]);
	},

	socketNotificationReceived: function (notification, payload) {
		if (notification === "smartmirror-mensa-plan_JSON_RESULT") {
			// Only continue if the notification came from the request we made
			if (payload.mensa_parser === this.config.mensa_parser)
			{
				this.jsonData = payload.data;
				this.updateDom(500);
				this.sendNotification('MENSA_PLAN', payload.data)
			}
		}
	},

	// Override dom generator.
	getDom: function () {
		var wrapper = document.createElement("div");
		wrapper.className = "xsmallMensa";


		if (!this.jsonData) {
			wrapper.innerHTML = "Awaiting json data...";
			return wrapper;
		}

		var table = document.createElement("table");
		var tbody = document.createElement("tbody");

		table.className = "table";
		table.className = "tbody";

		var items = this.jsonData[1];
		this.data.header = 'Mensa Menu - Uni Bielefeld (X building) - ' + this.jsonData[0];


		items.forEach(element => {
			var row = this.getTableRow(element);
			row.className = "tablerow";
			tbody.appendChild(row);
		});

		table.appendChild(tbody);
		wrapper.appendChild(table);
		return wrapper;
	},


	notificationReceived: function(notification, payload) {
       	
    },


	getTableRow: function (jsonObject) {
		var row = document.createElement("tr");

		var namecell = document.createElement("namecellMensa");
		namecell.className = "namecellMensa";
		var cellText = document.createTextNode(jsonObject['name']);
		cellText.className = "namecellMensa";
		namecell.appendChild(cellText);
		namecell.className =  "namecellMensa";
		row.appendChild(namecell);

		var valuecell = document.createElement("valuecellMensa");
		valuecell.className = "valuecellMensa";
		var cellText = document.createTextNode(jsonObject['value']);
		cellText.className ="valuecellMensa";
		valuecell.appendChild(cellText);
		row.appendChild(valuecell);

		return row;
	},

	 getStyles: function () {
        return ['mensa_style.css'];
    }

});
