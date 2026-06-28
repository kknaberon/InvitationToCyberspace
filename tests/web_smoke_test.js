"use strict";

const path = require("path");

let renderedHtml = "";

global.document = {
  getElementById(id) {
    if (id !== "app") throw new Error(`Unexpected element id: ${id}`);
    return {
      addEventListener() {},
      querySelector() {
        return null;
      },
      set innerHTML(value) {
        renderedHtml = value;
      },
      get innerHTML() {
        return renderedHtml;
      },
    };
  },
};

global.window = {
  setTimeout() {
    return 0;
  },
};

global.Audio = class {
  constructor() {
    this.dataset = {};
    this.volume = 0;
    this.loop = false;
    this.src = "";
  }

  play() {
    return Promise.resolve();
  }
};

require(path.join(__dirname, "..", "game.js"));

if (!renderedHtml.includes("スタート")) {
  throw new Error("Start button was not rendered.");
}

if (!renderedHtml.includes("音が流れます")) {
  throw new Error("Audio warning was not rendered.");
}

console.log("web smoke test passed");
