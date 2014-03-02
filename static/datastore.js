var Player = function(name, rank) {
	var _name = name;
	var _rank = rank;

	return {
		name: _name,
		rank: _rank,
	}
};

PLAYERS = [
	Player('Kyle Lady', 1),
	Player('Michael Benson', 2),
	Player('David Adrian', 3),
	Player('Sarah Paris', 4)
]

BRACKET = {
	players: PLAYERS,
	rounds: 2
	matchups: [
		[ // Round One
			[0, 1],
			[2, 3]
		],
		[ // Round Two, Index into round 1 games
			[0, 1]
		],
	]
}