$('[lang="th"]').hide();

$('#switch-lang').click(function() {
  $('[lang="th"]').toggle();
  $('[lang="en"]').toggle();
});