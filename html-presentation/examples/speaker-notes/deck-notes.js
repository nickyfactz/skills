/* Deck side of the speaker notes window. Paste into the deck's inline script,
   after the navigation code that defines `secs`, `cur`, `next()`, `prev()`
   and `go(i, dir)`. `maxStep(s)` returns the number of reveal steps a section
   has, or 0; `s.dataset.shown` holds how many are on screen.

   Protocol, both ways over postMessage, every payload tagged `sf`:
     notes -> deck   {sf:'hello'}                         the window has loaded
     deck  -> notes  {sf:'state', i, step, max}           the deck moved
     notes -> deck   {sf:'cmd', cmd:'next'|'prev'|'go', i} the presenter used the notes window
*/
var notesWin = null;

function state() {
  var s = secs[cur];
  return { sf: 'state', i: cur, step: +s.dataset.shown || 0, max: maxStep(s) };
}
function post() {
  if (notesWin && !notesWin.closed) { try { notesWin.postMessage(state(), '*'); } catch (e) {} }
}
function openNotes() {
  notesWin = window.open('speaker-notes.html', 'sf-notes', 'width=900,height=1000');
  setTimeout(post, 400);
}
window.addEventListener('message', function (e) {
  var d = e.data;
  if (!d || typeof d !== 'object') return;
  if (d.sf === 'hello') { notesWin = e.source; post(); }
  else if (d.sf === 'cmd') {
    if (d.cmd === 'next') next();
    else if (d.cmd === 'prev') prev();
    else if (d.cmd === 'go') go(+d.i, 0);
  }
});

/* Call post() at the end of go() and of every reveal step, so the notes follow.
   Bind the key in the deck's keydown handler:
     else if (k === 'n' || k === 'N') { openNotes(); }
*/
