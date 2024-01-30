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

	defaults: {
		updateInterval: 300000
	},

	start: function () {
		var self = this;
		self.getMensaJSON();
		self.scheduleUpdate();
	},

	scheduleUpdate: function () {
		var self = this;
		setInterval(function () {
			self.getMensaJSON();
		}, self.config.updateInterval);
	},

	// Request node_helper to get json from a mensa parser script
	getMensaJSON: function () {
		var self = this;
		self.sendSocketNotification("smartmirror-mensa-plan_GET_JSON", "");
	},

	socketNotificationReceived: function (notification, payload) {
		var self = this;
		if (notification === "smartmirror-mensa-plan_JSON_RESULT") {
			self.jsonData = payload;
			self.updateDom(10);
			//console.log(payload);
		}
	},

	getDom: function () {
		var wrapper = document.createElement("div");
		wrapper.className = "small";

		if (!this.jsonData) {
			wrapper.innerHTML = "Awaiting json data...";
		}else{

			var table = document.createElement("table");
			var tbody = document.createElement("tbody");
	
			table.className = "table";
			table.className = "tbody";
		
			for(var key in this.jsonData.mains){
				var menu_point = this.jsonData.mains[key].name;
				if (this.jsonData.mains[key].side.length > 0){
					menu_point = menu_point + " mit "
					if (this.jsonData.mains[key].side.length > 1){
						menu_point = menu_point + this.jsonData.mains[key].side.slice(0, -1).join(", ") + ' oder ' + this.jsonData.mains[key].side.slice(-1)
					} else {
						menu_point = menu_point + this.jsonData.mains[key].side
					}
				}
				var row = this.createMensaRow(key, menu_point);
				tbody.appendChild(row);
			}

			for(var key in this.jsonData.sides){
				if (this.jsonData.sides[key].length > 1){
					var menu_point = this.jsonData.sides[key].slice(0, -1).join(", ") + ' oder ' + this.jsonData.sides[key].slice(-1)
				}else{
					var menu_point =this.jsonData.sides[key].join(", ");
				}
				var row = this.createMensaRow(key,menu_point);
				tbody.appendChild(row);
			}
			table.appendChild(tbody);
			wrapper.appendChild(table);
		}
		return wrapper;		
	},

	notificationReceived: function(notification, payload) {
       	
    },

	createMensaRow:  function (name, value) {
		var row = document.createElement("tr");
		
		var namecell = document.createElement("namecellMensa");
		namecell.className = "namecellMensa";
		var cellText = document.createTextNode(name);
		cellText.className = "namecellMensa";
		namecell.appendChild(cellText);
		namecell.className =  "namecellMensa";
		row.appendChild(namecell);

		var valuecell = document.createElement("valuecellMensa");
		valuecell.className = "valuecellMensa";
		var cellText = document.createTextNode(value);
		cellText.className ="valuecellMensa";
		valuecell.appendChild(cellText);
		row.appendChild(valuecell);
		
		return row;
	},

	 getStyles: function () {
        return ['mensa_style.css'];
    }

});
