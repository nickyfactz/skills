/* Paste after the deck navigation (`secs`, `cur`, next/prev/go and maxStep).
   Call post() after navigation and reveals; bind N to openNotes().
   Only the window opened here may greet or command this deck. */
let notesWin = null;
const notesOrigin =
	window.location.protocol === "file:" ? "null" : window.location.origin;
// file: URLs have opaque origins; source identity remains mandatory there.
const notesTargetOrigin = notesOrigin === "null" ? "*" : notesOrigin;

function state() {
	const section = secs[cur];
	return {
		sf: "state",
		i: cur,
		step: Number(section.dataset.shown) || 0,
		max: maxStep(section),
	};
}

function post() {
	if (notesWin && !notesWin.closed) {
		notesWin.postMessage(state(), notesTargetOrigin);
	}
}

function openNotes() {
	if (notesWin && !notesWin.closed) {
		notesWin.focus();
		post();
		return;
	}
	// An unnamed window cannot collide with another presentation's notes window.
	notesWin = window.open(
		"speaker-notes.html",
		"_blank",
		"width=900,height=1000",
	);
	// The notes window sends hello once loaded. No timed, potentially early state.
}

window.addEventListener("message", (event) => {
	if (!notesWin || notesWin.closed || event.source !== notesWin) return;
	if (event.origin !== notesOrigin) return;
	const message = event.data;
	if (!message || typeof message !== "object" || Array.isArray(message)) return;

	if (message.sf === "hello") {
		post();
	} else if (message.sf === "cmd") {
		if (message.cmd === "next") next();
		else if (message.cmd === "prev") prev();
		else if (
			message.cmd === "go" &&
			Number.isInteger(message.i) &&
			message.i >= 0 &&
			message.i < secs.length
		) {
			go(message.i, 0);
		}
	}
});
