const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const test = require("node:test");
const vm = require("node:vm");

const deckScript = fs.readFileSync(
	path.join(__dirname, "deck-notes.js"),
	"utf8",
);
const notesScript = fs
	.readFileSync(path.join(__dirname, "notes.tpl.html"), "utf8")
	.match(/<script>([\s\S]*?)<\/script>/)[1];

function peer() {
	return {
		closed: false,
		sent: [],
		postMessage(data, origin) {
			this.sent.push({ data, origin });
		},
		focus() {},
	};
}

function locationFor(origin) {
	return { origin, protocol: origin.startsWith("https:") ? "https:" : "file:" };
}

function messageOrigin(origin) {
	return locationFor(origin).protocol === "file:" ? "null" : origin;
}

function deck(origin) {
	const handlers = {};
	const opened = [];
	const calls = [];
	const window = {
		location: locationFor(origin),
		addEventListener(type, fn) {
			handlers[type] = fn;
		},
		open() {
			const p = peer();
			opened.push(p);
			return p;
		},
	};
	const context = vm.createContext({
		window,
		secs: [{ dataset: {} }, { dataset: {} }],
		cur: 0,
		maxStep: () => 0,
		next: () => calls.push("next"),
		prev: () => calls.push("prev"),
		go: (i) => calls.push(i),
	});
	vm.runInContext(deckScript, context);
	return {
		context,
		opened,
		calls,
		send(source, data, eventOrigin = messageOrigin(origin)) {
			handlers.message({ source, data, origin: eventOrigin });
		},
	};
}

function element() {
	return {
		dataset: {},
		textContent: "",
		children: [],
		listeners: {},
		classList: { toggle() {} },
		querySelector: () => null,
		querySelectorAll() {
			return this.children;
		},
		appendChild(child) {
			this.children.push(child);
		},
		addEventListener(type, fn) {
			this.listeners[type] = fn;
		},
		setAttribute() {},
		removeAttribute() {},
	};
}

function notes(origin, opener = peer()) {
	const handlers = {};
	const elements = Object.fromEntries(
		["toc", "link", "main", "clock", "startstop", "reset", "pos", "target"].map(
			(id) => [id, element()],
		),
	);
	elements.main.dataset.end = "30:00";
	const slides = ["one", "two"].map((id, i) =>
		Object.assign(element(), { id, dataset: { title: id, min: `${i}:00` } }),
	);
	const window = {
		opener,
		location: locationFor(origin),
		addEventListener(type, fn) {
			handlers[type] = fn;
		},
	};
	const document = {
		querySelectorAll: () => slides,
		getElementById: (id) => elements[id],
		createElement: () => element(),
		addEventListener(type, fn) {
			handlers[type] = fn;
		},
	};
	vm.runInNewContext(notesScript, {
		window,
		document,
		location: { hash: "" },
		setInterval() {},
		Date,
	});
	return {
		elements,
		opener,
		send(source, data, eventOrigin = messageOrigin(origin)) {
			handlers.message({ source, data, origin: eventOrigin });
		},
		key(key) {
			handlers.keydown({ key, preventDefault() {} });
		},
	};
}

for (const origin of ["https://slides.example", "null", "file://"]) {
	test(`deck binds commands to its actual popup (${origin})`, () => {
		const d = deck(origin),
			stranger = peer();
		d.send(stranger, { sf: "hello" });
		d.send(stranger, { sf: "cmd", cmd: "next" });
		assert.deepEqual(d.calls, []);
		vm.runInContext("openNotes()", d.context);
		const popup = d.opened[0];
		d.send(stranger, { sf: "hello" });
		d.send(popup, { sf: "hello" }, "https://evil.example");
		assert.equal(popup.sent.length, 0);
		d.send(popup, { sf: "hello" });
		assert.equal(
			popup.sent[0].origin,
			messageOrigin(origin) === "null" ? "*" : origin,
		);
		d.send(popup, { sf: "cmd", cmd: "next" });
		d.send(popup, { sf: "cmd", cmd: "prev" });
		d.send(popup, { sf: "cmd", cmd: "go", i: 1 });
		for (const i of [-1, 2, 0.5, "1", null, NaN, Infinity])
			d.send(popup, { sf: "cmd", cmd: "go", i });
		d.send(stranger, { sf: "cmd", cmd: "next" });
		assert.deepEqual(d.calls, ["next", "prev", 1]);
		vm.runInContext("openNotes()", d.context);
		assert.equal(d.opened.length, 1);
		popup.closed = true;
		vm.runInContext("openNotes()", d.context);
		d.send(popup, { sf: "cmd", cmd: "next" });
		d.send(d.opened[1], { sf: "cmd", cmd: "next" });
		assert.deepEqual(d.calls, ["next", "prev", 1, "next"]);
	});

	test(`notes reject unrelated senders and invalid state (${origin})`, () => {
		const n = notes(origin),
			good = { sf: "state", i: 1, step: 0, max: 0 };
		assert.equal(
			n.opener.sent[0].origin,
			messageOrigin(origin) === "null" ? "*" : origin,
		);
		n.send(peer(), good);
		n.send(n.opener, good, "https://evil.example");
		for (const invalid of [
			null,
			[],
			{ ...good, i: "1" },
			{ ...good, i: 2 },
			{ ...good, i: -1 },
			{ ...good, step: 1 },
			{ ...good, max: NaN },
			{ ...good, step: 0.5 },
		])
			n.send(n.opener, invalid);
		assert.match(n.elements.pos.textContent, /1 of 2/);
		n.send(n.opener, good);
		assert.match(n.elements.pos.textContent, /2 of 2/);
		n.key("ArrowLeft");
		assert.equal(n.opener.sent.at(-1).data.cmd, "prev");
		n.opener.closed = true;
		n.key("ArrowLeft");
		assert.match(n.elements.pos.textContent, /1 of 2/);
		assert.match(n.elements.link.textContent, /not linked/);
	});
}

test("standalone notes navigate locally", () => {
	const n = notes("null", null);
	n.key("ArrowRight");
	assert.match(n.elements.pos.textContent, /2 of 2/);
});

test("blocked popup cannot accept a greeting", () => {
	const d = deck("https://slides.example");
	vm.runInContext("window.open = () => null; openNotes()", d.context);
	d.send(null, { sf: "hello" });
	assert.deepEqual(d.calls, []);
});
