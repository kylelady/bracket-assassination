var saveData = {
  teams : [
    ["Team 1", "Team 2"], /* first matchup */
    ["Team 3", "Team 4"]  /* second matchup */
  ],
  results : [[1,0], [2,7]]
}
 
$(document).ready(function() {
  var container = $('#bracket-holder')
  container.bracket({
    init: saveData,
  });
  /* You can also inquiry the current data */
  var data = container.bracket('data')
  $('#dataOutput').text(jQuery.toJSON(data))
})