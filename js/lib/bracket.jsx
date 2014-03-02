/** @jsx React.DOM */
var Team = function(name, rank) {
  var _name = name;
  var _rank = rank;

  var team = {};
  Object.defineProperty(team, "name", {
    value: _name,
    writable: false,
  });
  Object.defineProperty(team, "rank", {
    value: _rank,
    writable: false,
  });
  return team;
};

var Match = function(upperParent, lowerParent, edge) {
  var _upper = upperParent;
  var _lower = lowerParent;
  var _edge = edge;
  var _winner = null;
  var _child = null;

  var match = {

    setChild: function(child) {
      _child = child;
    },

    hasFirst: function() {
      if (_edge) {
        return upperParent.hasWinner();
      }
      return true;
    },

    hasSecond: function() {
      if (_edge) {
        return lowerParent.hasWinner();
      }
      return true;
    },

    hasWinner: function() {
      return (this.hasFirst() && this.hasSecond() && _winner != null)
    },

    getWinner: function() {
      if (_edge) {
        return _winner;
      }
      return upperParent.getWinner();
    },

    setFirstWins: function() {
      if (_edge) {
        _winner = upperParent;
      } else {
        _winner = upperParent.winner();
      }
    },

    setSecondWin: function() {
      if (_edge) {
        _winner = lowerParent;
      } else {
        _winner = lowerParent.winner();
      }
    },

    getFirst: function() {
      if (edge) {
        return _upper;
      } else {
        return _upper.getWinner();
      }
    },

    getSecond: function() {
      if (edge) {
        return _lower;
      } else {
        return _lower.getWinner();
      }
    },

  };

  if (!edge) {
    _upper.setChild(match);
    _lower.setChild(match);
  }

  return match;
};

var Bracket = function(tournament) {

  return {
    getLeftMatches: function() {

    },

    getRightMatches: function() {

    },

  };
}

var EntryBox = React.createClass({

  render: function() {
    var entryClasses = "col-md-12 " + this.props.status;
    return (
      <div className="row entry-row">
        <div className={entryClasses}>
          {this.props.team.name}
        </div>
      </div>
    );
  }
});

var MatchBox = React.createClass({

  render: function() {
    return (
      <div className="row match">
        <EntryBox status="favorite" team={this.props.favorite} />
        <EntryBox status="underdog" team={this.props.underdog} />
      </div>
    );
  }
});

var RoundBox = React.createClass({

  render: function() {
    var classes = "col-md-2 round " + this.props.roundClass;
    var matches = this.props.matches.map(function(match) {
      return (
        <MatchBox 
          favorite={match.getFirst()}
          underdog={match.getSecond()} 
        />
      );
    });
    return (
      <div className={classes}>
        <div className="row round-header">
          <b>{this.props.roundName}</b>
        </div>
        {matches}
      </div>
    );
  }
})

var TEAMS = [
  Team('Kyle Lady', 0),
  Team('Michael Benson', 1),
  Team('David Adrian', 2),
  Team('Sarah Paris', 3),
  Team('Ryan Landay', 4),
  Team('Angie Zhang', 5),
  Team('Rob Goeddel', 6),
  Team('Alyssa Kornyolo', 7)
];

var BracketHolder = React.createClass({

  matches: [
    Match(TEAMS[0], TEAMS[1], true),
    Match(TEAMS[2], TEAMS[3], true),
  ],

  roundNames: [
    'Round One',
    'Round Two',
    'Round Three',
    'Round Four',
    'Round Five',
    'Round Six',
  ],

  render: function() {
    var dummyRounds = [1, 2, 3, 4, 5, 6];
    var rounds = dummyRounds.map(function(elt, idx) {
      return (
        <RoundBox
          roundClass={'r' + idx} 
          roundName={this.roundNames[idx]}
          matches={this.matches}
        />
      )
    }.bind(this));
    return (
      <div className="row bracket">
        {rounds}
      </div>
    );
  }
});
