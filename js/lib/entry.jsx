/** @jsx React.DOM */
var EntryBox = React.createClass({
	getInitialState: function() {
		return {
			team: "Kyle Lady",
		};
	},
	render: function() {
		return (
			<div className="entryBox">
				{this.state.team}
			</div>
		);
	}
});