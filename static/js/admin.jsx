/*** @jsx React.DOM */
var defaultErrorLogger = function(url, xhr, status, err) {
  console.error(url, status, err.toString());
}

var playerById = function(id, player) {
  return player._id.$oid === id.$oid;
}

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
    this.props.addPlayer(player);
    this.refs.name.getDOMNode().value = '';
    this.refs.uniqname.getDOMNode().value = '';
    this.refs.rank.getDOMNode().value = '';
    return true;
  },

  handleClickDelete: function(player, url) {
    this.props.removePlayer(player, url);
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
          deleteCallback={this.handleClickDelete.bind(this, player, deleteUrl)}
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

var PlayerOption = React.createClass({

  render: function() {
    return (
      <option value={this.props.player._id}>
        {this.props.player.full_name + ' (' + this.props.player.uniqname + ')'}
      </option>
    );
  }

});

var MatchEntry = React.createClass({

  handleClickRemoveMatch: function(event) {
    this.props.removeCallback();
    return true;
  },

  render: function() {
    return (
      <tr>
        <td>{this.props.favorite.full_name}</td>
        <td>{this.props.underdog.full_name}</td>
        <td>
            <button className="btn btn-sm btn-danger" onClick={this.handleClickRemoveMatch} >
              <span className="glyphicon glyphicon-remove"></span>
            </button>
        </td>
      </tr>
    );
  }

});

var PlayerSelector = React.createClass({

  getSelectedPlayer: function() {
    var s = this.refs.pselect.getDOMNode();
    if (s.options.length == 0) {
      return null;
    }
    if (s.selectedIndex == -1) {
      return null;
    }
    console.log(s);
    var player = this.props.players[s.selectedIndex];
    return player;
  },

  render: function() {
    var playerOptions = this.props.players.map(function(player) {
      var key = this.props.which + player._id.$oid;
      return (
        <PlayerOption key={key} player={player} />
      );
    }.bind(this));
    return (
      <select ref="pselect" required="true" className="form-control">
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

  addMatch: function(match) {
    var favorite_id = match.favorite._id.$oid;
    var underdog_id = match.underdog._id.$oid;
    var body = {
      favorite: favorite_id,
      underdog: underdog_id
    };
    console.log(body);
    var url = '/api/matches/'
    $.ajax({
      url: url,
      dataType: 'json',
      type: 'POST',
      data: body,
      success: function(match) {
        var matches = this.state.matches;
        matches.push(match);
        this.setState({matches: matches});
        this.loadMatches();
      }.bind(this),
      error: defaultErrorLogger.bind(this, url)
    });  
  },

  removeMatch: function(match) {
    var url = '/api/matches/delete'
    var body = {
      match: match._id.$oid
    }
    $.ajax({
      url: url,
      dataType: 'json',
      type: 'POST',
      data: body,
      success: function(res) {
        this.loadMatches()
      }.bind(this),
      error: defaultErrorLogger.bind(this, url)
    })
  },

  componentWillMount: function() {
    this.loadMatches();
  },

  handleClickAddMatch: function() {
    var favorite = this.refs.fselect.getSelectedPlayer();
    var underdog = this.refs.uselect.getSelectedPlayer();
    console.log(favorite);
    console.log(underdog);
    if (!favorite || !underdog) {
      console.log('ruh roh');
      return false;
    }
    var match = {
      favorite: favorite,
      underdog: underdog
    };
    this.addMatch(match);
    return true;
  },

  render: function() {
    var matchRows = this.state.matches.map(function(match) {
      var favorite = this.props.players.find(playerById.bind(this, match.favorite));
      var underdog = this.props.players.find(playerById.bind(this, match.underdog));
      return (
        <MatchEntry
          key={match._id.$oid}
          favorite={favorite}
          underdog={underdog}
          removeCallback={this.removeMatch.bind(this, match)}
        />
      );
    }.bind(this));
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
              <PlayerSelector ref="fselect" which="favorite" players={this.props.players} />
            </td>
            <td>
              <PlayerSelector ref="uselect" which="underdog" players={this.props.players} />
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

  addPlayer: function(player) {
    var url = this.props.addUrl;
    $.ajax({
      url: url,
      dataType: 'json',
      type: 'POST',
      data: player,
      success: function(player) {
        var players = this.state.players;
        players.push(player);
        this.setState({players: players});
      }.bind(this),
      error: defaultErrorLogger.bind(this, url)
    });   
  },

  removePlayer: function(player, url) {
    var players = this.state.players;
    var trimmed_players = players.filter(function(p) {
      return p.uniqname != player.uniqname;
    });
    this.setState({players: trimmed_players});
    $.ajax({
      url: url,
      dataType: 'json',
      type: 'POST',
      data: { uniqname: player.uniqname },
      success: function() {
        this.loadPlayers();
      }.bind(this),
      error: defaultErrorLogger.bind(this, url)
    });
  },

  loadPlayers: function() {
    var url = this.props.loadUrl;
    $.ajax({
      url: url,
      dataType: 'json',
      success: function(data) {
        this.setState({players: data.players})
      }.bind(this),
      error: defaultErrorLogger.bind(this, url)
    });    
  },

  render: function() {
    return (
    <div>
      <div className="row">
        <h3 id="players">Players</h3>
        <PlayerTable
          addUrl="/api/players/"
          loadUrl="/api/players/"
          players={this.state.players}
          loadPlayers={this.loadPlayers}
          addPlayer={this.addPlayer}
          removePlayer={this.removePlayer} />,
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
  <AdminInterface loadUrl="/api/players/" addUrl="/api/players/" />,
  mountPoint
);