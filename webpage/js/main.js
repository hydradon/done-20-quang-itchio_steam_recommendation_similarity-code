var column_names = [
	'Itch game',
	'Itch game url',
	'Steam game',
	'Steam game url'
];
//  itch_game,itch_game_url,steam_game,steam_game_index,steam_game_url,sim_scores

// draw the table

var table = d3.select(".table");
table.append('thead').attr('class', 'thead-dark').append('tr');

var headers = table
	.select('tr')
	.selectAll('th')
	.data(column_names)
	.enter()
	.append('th')
	.text(function (d) {
		return d;
	});

var rows,
	row_entries,
	row_entries_no_anchor,
	row_entries_with_anchor,
	steam_row;
var dataset;
// d3.csv('./data.csv', function (data) {
d3.csv('./data/df_5_recommendation_all.csv', function (data) {
	// d3.json('./data.json', function (data) {
	// loading data from server
	dataset = data;
	// draw table body with rows
	table.append('tbody');

	// data bind
	rows = table
		.select('tbody')
		.selectAll('tr')
		.data(data, function (d) {
			return d.row_id;
		});
	// .data(data);

	// enter the rows
	rows.enter().append('tr');

	// enter td's in each row
	row_entries = rows
		.selectAll('td')
		.data(function (d) {
			var arr = [];
			for (var k in d) {
				if (d.hasOwnProperty(k)) {
					arr.push(d[k]);
				}
			}
			return [arr[0], arr[1], arr[2], arr[4]];
		})
		.enter()
		.append('td');

	// draw row entries with no anchor
	row_entries_no_anchor = row_entries.filter(function (d) {
		return /https?:\/\//.test(d) == false;
	});
	row_entries_no_anchor.text(function (d) {
		return d;
	});

	// draw row entries with anchor, not steam link
	row_entries_with_anchor = row_entries.filter(function (d) {
		return (
			/https?:\/\//.test(d) == true &&
			/https?:\/\/.*steam.*/.test(d) == false
		);
	});
	row_entries_with_anchor
		.append('a')
		.attr('href', function (d) {
			return d;
		})
		.attr('target', '_blank')
		.text(function (d) {
			return d;
		});

	// draw Steam link as iframe
	steam_row = row_entries.filter(function (d) {
		return (
			/https?:\/\//.test(d) == true &&
			/https?:\/\/.*steam.*/.test(d) == true
		);
	});
	steam_row
		.append('iframe')
		.attr('src', function (d) {
			return get_steam_widget_url(d);
		})
		.attr('class', 'steam_iframe')
		// .attr('target', '_blank')
		.text(function (d) {
			return d;
		});

	/**  search functionality **/
	d3.select('#search').on('keyup', function () {
		// filter according to key pressed
		var searched_data = data,
			text = this.value.trim();

		var searchResults = searched_data.map(function (r) {
			var regex = new RegExp('^' + text + '.*', 'i');
			if (regex.test(r.itch_game)) {
				// if there are any results
				return regex.exec(r.itch_game)[0]; // return them to searchResults
			}
		});

		// filter blank entries from searchResults
		searchResults = searchResults.filter(function (r) {
			return r != undefined;
		});

		// filter dataset with searchResults
		searched_data = searchResults.map(function (r) {
			return data.filter(function (p) {
				return p.itch_game.indexOf(r) != -1;
			});
		});

		// flatten array
		searched_data = [].concat.apply([], searched_data);

		// data bind with new data
		rows = table
			.select('tbody')
			.selectAll('tr')
			.data(searched_data, function (d) {
				return d.row_id;
			});
		// .data(searched_data);

		// enter the rows
		rows.enter().append('tr');

		// enter td's in each row
		row_entries = rows
			.selectAll('td')
			.data(function (d) {
				var arr = [];
				for (var k in d) {
					if (d.hasOwnProperty(k)) {
						arr.push(d[k]);
					}
				}
				// return [arr[3], arr[1], arr[2], arr[0]];
				return [arr[0], arr[1], arr[2], arr[4]];
			})
			.enter()
			.append('td');

		// draw row entries with no anchor
		row_entries_no_anchor = row_entries.filter(function (d) {
			return /https?:\/\//.test(d) == false;
		});
		row_entries_no_anchor.text(function (d) {
			return d;
		});

		// draw row entries with anchor
		row_entries_with_anchor = row_entries.filter(function (d) {
			return (
				/https?:\/\//.test(d) == true &&
				/https?:\/\/.*steam.*/.test(d) == false
			);
		});
		row_entries_with_anchor
			.append('a')
			.attr('href', function (d) {
				return d;
			})
			.attr('target', '_blank')
			.text(function (d) {
				return d;
			});

		// draw Steam link as iframe
		steam_row = row_entries.filter(function (d) {
			return (
				/https?:\/\//.test(d) == true &&
				/https?:\/\/.*steam.*/.test(d) == true
			);
		});
		steam_row
			.append('iframe')
			.attr('src', function (d) {
				return get_steam_widget_url(d);
			})
			.attr('class', 'steam_iframe')
			.text(function (d) {
				return d;
			});

		// exit
		rows.exit().remove();
	});
});

d3.select(self.frameElement).style('height', '780px').style('width', '1150px');

function get_steam_widget_url(steam_url) {
	// Sample https://store.steampowered.com/app/519860/DUSK
	var app_id = steam_url.split('/')[4];
	return '//store.steampowered.com/widget/' + app_id;
}
