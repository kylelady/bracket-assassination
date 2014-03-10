/*** @jsx React.DOM */
var PlayerEntry = React.createClass({

  handleClickDelete: function() {
    return this.props.deleteCallback();
  },

  getDefaultProps: function() {
    return {
      rank: ''
    }
  },

  render: function() {
    return (
      <tr>
        <td>{this.props.name}</td>
        <td>{this.props.uniqname}</td>
        <td>{this.props.rank}</td>
        <td>
          <button className="btn btn-sm btn-danger" onClick={this.handleClickDelete}>
            <span className="glyphicon glyphicon-remove"></span>
          </button>
        </td>
      </tr>
    );
  }
});

var PlayerTable = React.createClass({

  addPlayer: function(player) {
    $.ajax({
      url: this.props.addUrl,
      dataType: 'json',
      type: 'POST',
      data: player,
      success: function(player) {
        this.props.loadPlayers();
      }.bind(this)
    });
  },

  removePlayer: function(player, url) {
    var players = this.state.players;
    var trimmed_players = players.filter(function(p) {
      return p.uniqname != player.uniqname;
    });
    $.ajax({
      url: url,
      dataType: 'json',
      type: 'POST',
      data: { uniqname: player.uniqname },
      success: function() {
        this.props.loadPlayers();
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.deleteUrl, status, err.toString());
      }.bind(this)
    });
  },

  handleClickAdd: function() {
    var name = this.refs.name.getDOMNode().value.trim();
    var uniqname = this.refs.uniqname.getDOMNode().value.trim();
    var rank = parseInt(this.refs.rank.getDOMNode().value.trim(), 10);
    if (!name || !uniqname) {
      return false;
    }
    var player = {
      full_name: name,
      uniqname: uniqname
    }
    if (rank) {
      player.rank = rank;
    }
    this.addPlayer(player);
    this.refs.name.getDOMNode().value = '';
    this.refs.uniqname.getDOMNode().value = '';
    this.refs.rank.getDOMNode().value = '';
    return true;
  },

  render: function() {
    var playerRows = this.props.players.map(function(player) {
      var deleteUrl = this.props.loadUrl + encodeURIComponent(player.uniqname) + '/delete/'
      return (
        <PlayerEntry 
          name={player.full_name}
          uniqname={player.uniqname}
          rank={player.rank}
          key={player.uniqname}
          deleteCallback={this.removePlayer.bind(this, player, deleteUrl)}
          />
      );
    }.bind(this));
    return (
      <table className="table">
       <thead>
        <th>Name</th>
        <th>Uniqname</th>
        <th>Rank</th>
       </thead>
       <tbody>
        {playerRows}
        <tr>
          <td>
            <input type="text" placeholder="Name" ref="name" className="form-control"></input>
          </td>
          <td>
            <input type="text" placeholder="Uniqname" ref="uniqname" className="form-control"></input>
          </td>
          <td>
            <input type="text" placeholder="Rank (Optional)" ref="rank" className="form-control"></input>
          </td>        
          <td>
            <button className="btn btn-sm btn-success" onClick={this.handleClickAdd}>
              <span className="glyphicon glyphicon-ok"></span>
            </button>
          </td>                
        </tr>
       </tbody>
      </table>
    );
  }
});

var MatchEntry = React.createClass({

  handleClickRemoveMatch: function(event) {
    console.log('remove match');
  },

  render: function() {
    return (
      <tr>
        <td>{this.props.favorite}</td>
        <td>{this.props.underdog}</td>
        <td>
            <button className="btn btn-sm btn-danger" onClick={this.handleClickRemoveMatch}>
              <span className="glyphicon glyphicon-remove"></span>
            </button>
        </td>
      </tr>
    );
  }

});

var PlayerSelector = React.createClass({

  render: function() {
    var playerOptions = this.props.players.map(function(player) {
      return (
        <option value={player._id}>{player.full_name + ' (' + player.uniqname + ')'}</option>
      );
    })
    return (
      <select required="true" className="form-control">
        {playerOptions}
      </select>
    );
  }
});

var MatchTable = React.createClass({

  getInitialState: function() {
    return {
      matches: []
    };
  },

  loadMatches: function() {
    $.ajax({
      url: this.props.loadUrl,
      dataType: 'json',
      success: function(data) {
        this.setState({matches: data.matches})
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.loadUrl, status, err.toString());
      }.bind(this)
    });
  },

  componentWillMount: function() {
    this.loadMatches();
  },

  handleClickAddMatch: function() {
    console.log('add match');
  },

  render: function() {
    var matchRows = this.state.matches.map(function(match) {
      return (
        <MatchEntry
          favorite={match.favorite}
          underdog={match.underdog}
        />
      );
    });
    return (
      <table className="table">
        <thead>
          <th>Favorite</th>
          <th>Underdog</th>
        </thead>
        <tbody>
          {matchRows}
          <tr>
            <td>
              <PlayerSelector players={this.props.players} />
            </td>
            <td>
              <PlayerSelector players={this.props.players} />
            </td>
            <td>
              <button className="btn btn-sm btn-success" onClick={this.handleClickAddMatch}>
                <span className="glyphicon glyphicon-ok"></span>
              </button>              
            </td>    
          </tr>
        </tbody>
      </table>
    )
  }

});

var AdminInterface = React.createClass({

  getInitialState: function() {
    return {
      players: []
    };
  },

  componentWillMount: function() {
    this.loadPlayers();
  },

  loadPlayers: function() {
    $.ajax({
      url: this.props.loadUrl,
      dataType: 'json',
      success: function(data) {
        this.setState({players: data.players})
      }.bind(this),
      error: function(xhr, status, err) {
        console.error(this.props.loadUrl, status, err.toString());
      }.bind(this)
    });    
  },

  render: function() {
    return (
    <div>
      <div className="row">
        <h3 id="players">Players</h3>
        <PlayerTable addUrl="/api/players/" loadUrl="/api/players/" players={this.state.players} loadPlayers={this.loadPlayers} />,
      </div>
      <div className="row">
        <h3 id="matches">Matches</h3>
        <MatchTable loadUrl="/api/matches/" players={this.state.players} loadPlayers={this.loadPlayers} />
      </div>
    </div>
    );
  }
})

var mountPoint = document.getElementById('react-adminInterface');
React.renderComponent(
  <AdminInterface loadUrl="/api/players/" />,
  mountPoint
);