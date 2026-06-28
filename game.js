"use strict";

const IMAGE_PATH = "WebpImage/";
const MUSIC_PATH = "Music/";

const ASSETS = {
  images: {
    opening: `${IMAGE_PATH}OP.webp`,
    introClosed: `${IMAGE_PATH}Intro_ClosingCrossingGate.webp`,
    introSouth: `${IMAGE_PATH}Intro_To_South.webp`,
    introOpen: `${IMAGE_PATH}Intro_OpeningCrossingGate.webp`,
    north: `${IMAGE_PATH}To_North.webp`,
    south: `${IMAGE_PATH}To_South.webp`,
    east: `${IMAGE_PATH}To_East.webp`,
    west: `${IMAGE_PATH}To_West.webp`,
  },
  music: {
    opening: `${MUSIC_PATH}Opening-Invitation to Cyberspace.wav`,
    main: `${MUSIC_PATH}Train-Invitation to Cyberspace.wav`,
    ending: `${MUSIC_PATH}DJ_Dupont.mp3`,
  },
};

const DIRECTIONS = [
  {
    id: "north",
    label: "北",
    image: ASSETS.images.north,
    name: "アメカジさん",
    lines: [
      "まゆみちゃん。自転車の鍵の番号なんだっけ？",
      "xxxxじゃなかった？",
      "自転車の鍵開けておいたよ！",
      "自転車借りていくね。",
    ],
  },
  {
    id: "east",
    label: "東",
    image: ASSETS.images.east,
    name: "野生動物",
    lines: [
      "１、３、５、７・・・綺麗な音。あなたの音は？",
      "xxxxの方が綺麗だよ。",
      "ふふふ。",
      "あなたも上に乗って。",
    ],
  },
  {
    id: "south",
    label: "南",
    image: ASSETS.images.south,
    name: "美容師",
    lines: [
      "オレ美容師だけど、0000から9999の間でオレの好きな数字当ててみて。",
      "xxxxだよ。",
      "２か月後に来てください。",
      "逃がさねぇ！！",
    ],
  },
  {
    id: "west",
    label: "西",
    image: ASSETS.images.west,
    name: "鉄道車両整備士たち",
    lines: [
      "おい！大丈夫か？西暦何年か答えてみろ！",
      "XXXX年だよ！",
      "大丈夫か？",
      "顔色が悪いぞ。",
    ],
  },
];

const INTRO_STEPS = [
  { image: ASSETS.images.introClosed, speaker: "私", text: "！？" },
  { image: ASSETS.images.introSouth, speaker: "美容師", text: "一昨日はありがとうございました。" },
  { image: ASSETS.images.introSouth, speaker: "私", text: "ひっ！！" },
  { image: ASSETS.images.introSouth, speaker: "私", text: "（お店出てからずっと後ろにいる・・・）" },
  {
    image: ASSETS.images.introOpen,
    speaker: "私",
    text: "（カットだけで８千円もする美容室なのに、狂ってる・・・逃げなきゃ！）",
  },
];

const ENDING_STEPS = [
  { speaker: "てほん", text: "これローソンで使える500円クーポン券の番号○○○だけど。" },
  { speaker: "てほん", text: "こんなげーむにまじになっちゃってどうするの 完" },
];

const CARD_DEFINITIONS = [
  ["G0-01", "Grade 0 Card 01", 0, 9, 1, 1, 1],
  ["G0-02", "Grade 0 Card 02", 0, 1, 9, 1, 1],
  ["G0-03", "Grade 0 Card 03", 0, 1, 1, 9, 1],
  ["G0-04", "Grade 0 Card 04", 0, 1, 1, 1, 9],
  ["G0-05", "Grade 0 Card 05", 0, 6, 2, 2, 2],
  ["G0-06", "Grade 0 Card 06", 0, 2, 6, 2, 2],
  ["G0-07", "Grade 0 Card 07", 0, 2, 2, 6, 2],
  ["G0-08", "Grade 0 Card 08", 0, 2, 2, 2, 6],
  ["G0-09", "Grade 0 Card 09", 0, 3, 3, 3, 3],
  ["G0-10", "Grade 0 Card 10", 0, 4, 3, 2, 3],
  ["G0-11", "Grade 0 Card 11", 0, 3, 4, 3, 2],
  ["G0-12", "Grade 0 Card 12", 0, 2, 3, 4, 3],
  ["G0-13", "Grade 0 Card 13", 0, 3, 2, 3, 4],
  ["G0-14", "Grade 0 Card 14", 0, 5, 1, 5, 1],
  ["G0-15", "Grade 0 Card 15", 0, 1, 5, 1, 5],
  ["G0-16", "Grade 0 Card 16", 0, 7, 1, 2, 2],
  ["G0-17", "Grade 0 Card 17", 0, 2, 7, 1, 2],
  ["G0-18", "Grade 0 Card 18", 0, 2, 2, 7, 1],
  ["G0-19", "Grade 0 Card 19", 0, 1, 2, 2, 7],
  ["G0-20", "Grade 0 Card 20", 0, 4, 4, 2, 2],
  ["G1-01", "Grade 1 Card 01", 1, 8, 3, 3, 3],
  ["G1-02", "Grade 1 Card 02", 1, 3, 8, 3, 3],
  ["G1-03", "Grade 1 Card 03", 1, 3, 3, 8, 3],
  ["G1-04", "Grade 1 Card 04", 1, 3, 3, 3, 8],
  ["G1-05", "Grade 1 Card 05", 1, 6, 4, 4, 3],
  ["G1-06", "Grade 1 Card 06", 1, 3, 6, 4, 4],
  ["G1-07", "Grade 1 Card 07", 1, 4, 3, 6, 4],
  ["G1-08", "Grade 1 Card 08", 1, 4, 4, 3, 6],
  ["G1-09", "Grade 1 Card 09", 1, 5, 5, 4, 3],
  ["G1-10", "Grade 1 Card 10", 1, 3, 5, 5, 4],
  ["G1-11", "Grade 1 Card 11", 1, 4, 3, 5, 5],
  ["G1-12", "Grade 1 Card 12", 1, 5, 4, 3, 5],
  ["G1-13", "Grade 1 Card 13", 1, 7, 2, 5, 3],
  ["G1-14", "Grade 1 Card 14", 1, 3, 7, 2, 5],
  ["G1-15", "Grade 1 Card 15", 1, 5, 3, 7, 2],
  ["G1-16", "Grade 1 Card 16", 1, 2, 5, 3, 7],
  ["G1-17", "Grade 1 Card 17", 1, 4, 4, 4, 4],
  ["G1-18", "Grade 1 Card 18", 1, 7, 3, 3, 3],
  ["G1-19", "Grade 1 Card 19", 1, 3, 7, 3, 3],
  ["G1-20", "Grade 1 Card 20", 1, 3, 3, 7, 3],
  ["G2-01", "Grade 2 Card 01", 2, 9, 5, 4, 4],
  ["G2-02", "Grade 2 Card 02", 2, 4, 9, 5, 4],
  ["G2-03", "Grade 2 Card 03", 2, 4, 4, 9, 5],
  ["G2-04", "Grade 2 Card 04", 2, 5, 4, 4, 9],
  ["G2-05", "Grade 2 Card 05", 2, 7, 6, 5, 4],
  ["G2-06", "Grade 2 Card 06", 2, 4, 7, 6, 5],
  ["G2-07", "Grade 2 Card 07", 2, 5, 4, 7, 6],
  ["G2-08", "Grade 2 Card 08", 2, 6, 5, 4, 7],
  ["G2-09", "Grade 2 Card 09", 2, 8, 3, 8, 3],
  ["G2-10", "Grade 2 Card 10", 2, 3, 8, 3, 8],
  ["G2-11", "Grade 2 Card 11", 2, 6, 6, 5, 5],
  ["G2-12", "Grade 2 Card 12", 2, 10, 4, 4, 4],
  ["G2-13", "Grade 2 Card 13", 2, 6, 5, 5, 5],
  ["G2-14", "Grade 2 Card 14", 2, 8, 5, 4, 4],
  ["G2-15", "Grade 2 Card 15", 2, 4, 8, 5, 4],
  ["G2-16", "Grade 2 Card 16", 2, 4, 4, 8, 5],
  ["G2-17", "Grade 2 Card 17", 2, 5, 4, 4, 8],
  ["G2-18", "Grade 2 Card 18", 2, 7, 7, 4, 3],
  ["G2-19", "Grade 2 Card 19", 2, 3, 7, 7, 4],
  ["G2-20", "Grade 2 Card 20", 2, 4, 3, 7, 7],
  ["G3-01", "Grade 3 Card 01", 3, 10, 7, 6, 5],
  ["G3-02", "Grade 3 Card 02", 3, 5, 10, 7, 6],
  ["G3-03", "Grade 3 Card 03", 3, 6, 5, 10, 7],
  ["G3-04", "Grade 3 Card 04", 3, 7, 6, 5, 10],
  ["G3-05", "Grade 3 Card 05", 3, 9, 7, 6, 5],
  ["G3-06", "Grade 3 Card 06", 3, 5, 9, 7, 6],
  ["G3-07", "Grade 3 Card 07", 3, 6, 5, 9, 7],
  ["G3-08", "Grade 3 Card 08", 3, 7, 6, 5, 9],
  ["G3-09", "Grade 3 Card 09", 3, 8, 8, 6, 5],
  ["G3-10", "Grade 3 Card 10", 3, 5, 8, 8, 6],
  ["G3-11", "Grade 3 Card 11", 3, 6, 5, 8, 8],
  ["G3-12", "Grade 3 Card 12", 3, 8, 6, 5, 8],
  ["G3-13", "Grade 3 Card 13", 3, 10, 4, 9, 4],
  ["G3-14", "Grade 3 Card 14", 3, 4, 10, 4, 9],
  ["G3-15", "Grade 3 Card 15", 3, 9, 4, 10, 4],
  ["G3-16", "Grade 3 Card 16", 3, 4, 9, 4, 10],
  ["G3-17", "Grade 3 Card 17", 3, 7, 7, 7, 6],
  ["G3-18", "Grade 3 Card 18", 3, 6, 7, 7, 7],
  ["G3-19", "Grade 3 Card 19", 3, 8, 7, 6, 6],
  ["G3-20", "Grade 3 Card 20", 3, 6, 8, 7, 6],
  ["G4-01", "Grade 4 Card 01", 4, 10, 9, 8, 6],
  ["G4-02", "Grade 4 Card 02", 4, 6, 10, 9, 8],
  ["G4-03", "Grade 4 Card 03", 4, 8, 6, 10, 9],
  ["G4-04", "Grade 4 Card 04", 4, 9, 8, 6, 10],
  ["G4-05", "Grade 4 Card 05", 4, 10, 10, 7, 6],
  ["G4-06", "Grade 4 Card 06", 4, 6, 10, 10, 7],
  ["G4-07", "Grade 4 Card 07", 4, 7, 6, 10, 10],
  ["G4-08", "Grade 4 Card 08", 4, 10, 7, 6, 10],
  ["G4-09", "Grade 4 Card 09", 4, 9, 9, 8, 7],
  ["G4-10", "Grade 4 Card 10", 4, 7, 9, 9, 8],
  ["G4-11", "Grade 4 Card 11", 4, 8, 7, 9, 9],
  ["G4-12", "Grade 4 Card 12", 4, 9, 8, 7, 9],
  ["G4-13", "Grade 4 Card 13", 4, 10, 8, 10, 5],
  ["G4-14", "Grade 4 Card 14", 4, 5, 10, 8, 10],
  ["G4-15", "Grade 4 Card 15", 4, 10, 5, 10, 8],
  ["G4-16", "Grade 4 Card 16", 4, 8, 10, 5, 10],
  ["G4-17", "Grade 4 Card 17", 4, 8, 8, 8, 8],
  ["G4-18", "Grade 4 Card 18", 4, 10, 9, 7, 6],
  ["G4-19", "Grade 4 Card 19", 4, 6, 10, 9, 7],
  ["G4-20", "Grade 4 Card 20", 4, 7, 6, 10, 9],
];

const MODEL_WEIGHTS = {
  bias: 0.0,
  turn_index: 0.0,
  is_blue: 0.0,
  is_red: 0.0,
  is_first_player: 0.0,
  is_second_player: 0.0,
  self_hand_count: 0.0,
  opponent_hand_count: 0.0,
  self_board_count: 0.0,
  opponent_board_count: 0.0,
  card_grade: -0.9499999999999991,
  card_top: 0.8799999999999792,
  card_right: 0.7799999999999955,
  card_bottom: 0.7399999999999791,
  card_left: 0.8199999999999792,
  card_average: 0.8049999999999782,
  position: 0.02499999999999887,
  row: 0.10000000000000003,
  col: -0.19999999999999954,
  is_center: 0.6000000000000001,
  is_corner: 0.0,
  is_edge: -0.6000000000000001,
  adjacent_self: -0.10000000000000046,
  adjacent_opponent: 0.10000000000000923,
  adjacent_empty: 0.15000000000004754,
  ownership_gain: 3.1600000000000024,
  score_diff_after: 3.160000000000002,
  wins_immediately: 0.0,
  loses_immediately: 0.0,
};

const CARDS = CARD_DEFINITIONS.map(([id, name, grade, top, right, bottom, left]) => ({
  id,
  name,
  grade,
  top,
  right,
  bottom,
  left,
}));

const app = document.getElementById("app");
const bgm = new Audio();
let cardInstanceId = 0;

const game = {
  screen: "start",
  muted: false,
  introIndex: 0,
  directionIndex: 0,
  defeated: new Set(),
  currentCharacter: null,
  secret: "",
  guess: "",
  matchedDigits: 0,
  grade: 0,
  pendingHands: null,
  pendingFirstPlayer: "blue",
  battle: null,
  outcome: null,
  endingIndex: 0,
  feedback: "",
};

app.addEventListener("click", onClick);
app.addEventListener("submit", onSubmit);
render();

function onClick(event) {
  const target = event.target.closest("[data-action], [data-card-index], [data-cell-index]");
  if (!target) return;

  if (target.dataset.cardIndex !== undefined) {
    selectPlayerCard(Number(target.dataset.cardIndex));
    return;
  }

  if (target.dataset.cellIndex !== undefined) {
    placePlayerCard(Number(target.dataset.cellIndex));
    return;
  }

  const action = target.dataset.action;
  unlockAudio();

  if (action === "enter-opening") enterOpening();
  if (action === "start-intro") startIntro();
  if (action === "external-link") window.location.href = "https://andleather.official.ec/categories/2110113";
  if (action === "intro-next") advanceIntro();
  if (action === "nav-left") rotateDirection(-1);
  if (action === "nav-right") rotateDirection(1);
  if (action === "talk") startNumberGuess();
  if (action === "start-battle") startBattle();
  if (action === "finish-win") finishWin();
  if (action === "reset-opening") resetToOpening();
  if (action === "ending-next") advanceEnding();
  if (action === "toggle-mute") toggleMute();
}

function onSubmit(event) {
  if (event.target.id !== "guess-form") return;
  event.preventDefault();
  const value = String(new FormData(event.target).get("guess") || "").trim();
  submitGuess(value);
}

function render() {
  if (game.screen === "start") renderStart();
  if (game.screen === "opening") renderOpening();
  if (game.screen === "intro") renderIntro();
  if (game.screen === "main") renderMain();
  if (game.screen === "guess") renderGuess();
  if (game.screen === "guess-result") renderGuessResult();
  if (game.screen === "battle") renderBattle();
  if (game.screen === "post-battle") renderPostBattle();
  if (game.screen === "ending") renderEnding();
}

function renderStart() {
  app.innerHTML = sceneHtml({
    plain: true,
    className: " scene--start",
    content: `
      <div class="start-content">
        <div class="start-note">音が流れます</div>
        <button class="primary-button start-button" data-action="enter-opening">スタート</button>
      </div>
    `,
  });
}

function renderOpening() {
  setMusic(ASSETS.music.opening, true);
  app.innerHTML = sceneHtml({
    image: ASSETS.images.opening,
    content: `
      ${topbarHtml("")}
      <div class="bottom">
        <div class="commands">
          <button class="command-button" data-action="start-intro">髪を切ってくれてありがとうございます。</button>
          <button class="command-button" data-action="external-link">レザークラフトを始めてみる</button>
        </div>
      </div>
    `,
  });
}

function renderIntro() {
  setMusic(ASSETS.music.main, true);
  const step = INTRO_STEPS[game.introIndex];
  app.innerHTML = sceneHtml({
    image: step.image,
    content: `
      ${topbarHtml("")}
      <div class="bottom">
        ${dialogueHtml(step.speaker, step.text)}
        <button class="primary-button" data-action="intro-next">次へ</button>
      </div>
    `,
  });
}

function renderMain() {
  setMusic(ASSETS.music.main, true);
  const direction = currentDirection();
  const defeated = game.defeated.has(direction.id);
  const text = defeated
    ? `${direction.name}：${direction.lines[2]}`
    : `私：（${direction.label}に${direction.name}がいる・・・）`;

  app.innerHTML = sceneHtml({
    image: direction.image,
    content: `
      ${topbarHtml(`<div class="status-chip">向き：${direction.label}</div>`)}
      <div class="player-marker" aria-hidden="true"></div>
      <div class="bottom">
        ${dialogueHtml(defeated ? direction.name : "私", text.replace(`${direction.name}：`, ""))}
        <div class="nav-controls">
          <button class="nav-button" data-action="nav-left" aria-label="左へ向く">←</button>
          <button class="nav-button" data-action="talk" aria-label="話しかける">↑</button>
          <button class="nav-button" data-action="nav-right" aria-label="右へ向く">→</button>
        </div>
        ${progressHtml()}
      </div>
    `,
  });
}

function renderGuess() {
  const character = game.currentCharacter;
  app.innerHTML = sceneHtml({
    image: character.image,
    content: `
      ${topbarHtml(`<div class="status-chip">${character.label}：${character.name}</div>`)}
      <div class="bottom">
        ${dialogueHtml(character.name, character.lines[0])}
        <form id="guess-form" class="guess-form">
          <input class="guess-input" name="guess" inputmode="numeric" pattern="[0-9]{4}" maxlength="4" autocomplete="off" placeholder="0000" />
          <button class="command-button" type="submit">答える</button>
        </form>
        ${game.feedback ? `<div class="battle-message">${escapeHtml(game.feedback)}</div>` : ""}
      </div>
    `,
  });
  const input = app.querySelector(".guess-input");
  if (input) input.focus({ preventScroll: true });
}

function renderGuessResult() {
  const character = game.currentCharacter;
  const answerLine = character.lines[1].replace("xxxx", game.secret).replace("XXXX", game.secret);
  app.innerHTML = sceneHtml({
    image: character.image,
    content: `
      ${topbarHtml(`<div class="status-chip">一致：${game.matchedDigits}桁</div><div class="status-chip">グレード${game.grade}</div>`)}
      <div class="bottom">
        ${dialogueHtml(character.name, answerLine)}
        <div class="battle-message">あなたの入力：${escapeHtml(game.guess)} / 正解：${game.secret} / カードグレード：${game.grade}</div>
        <button class="primary-button" data-action="start-battle">カードバトルへ</button>
      </div>
    `,
  });
}

function renderBattle() {
  const battle = game.battle;
  const score = scoreBattle(battle);
  const turnText = battle.turn === "blue" ? "あなたの番" : `${game.currentCharacter.name}の番`;
  app.innerHTML = sceneHtml({
    image: game.currentCharacter.image,
    content: `
      ${topbarHtml(`<div class="status-chip">${turnText}</div><div class="status-chip">先攻：${ownerLabel(battle.firstPlayer)}</div>`)}
      <div class="bottom battle-shell">
        <div class="battle-message">${escapeHtml(battle.message)}</div>
        <div class="score-row">
          <div class="score-box">青 ${score.blue}</div>
          <div class="score-box">${turnText}</div>
          <div class="score-box">赤 ${score.red}</div>
        </div>
        <div class="hand-panel">
          <div class="hand-title">あなたの手札</div>
          <div class="hand-list">${handHtml(battle.blueHand, "blue", battle.turn === "blue")}</div>
        </div>
        <div class="battle-board">${boardHtml(battle)}</div>
        <div class="hand-panel">
          <div class="hand-title">${game.currentCharacter.name}の手札</div>
          <div class="hand-list">${handHtml(battle.redHand, "red", false)}</div>
        </div>
      </div>
    `,
  });
  scheduleCpuMove();
}

function renderPostBattle() {
  const outcome = game.outcome;
  const character = game.currentCharacter;
  const won = outcome.result === "win";
  const sceneClass = won ? "" : " penalty";
  const scoreLine = `最終スコア 青${outcome.score.blue} - 赤${outcome.score.red}`;
  app.innerHTML = sceneHtml({
    image: character.image,
    className: sceneClass,
    content: `
      ${topbarHtml(`<div class="status-chip">${scoreLine}</div>`)}
      <div class="bottom">
        ${dialogueHtml(character.name, won ? character.lines[2] : character.lines[3])}
        <div class="battle-message">${escapeHtml(outcome.note)}</div>
        <button class="primary-button" data-action="${won ? "finish-win" : "reset-opening"}">${won ? "次へ" : "オープニングへ戻る"}</button>
      </div>
    `,
  });
}

function renderEnding() {
  setMusic(ASSETS.music.ending, true);
  const step = ENDING_STEPS[game.endingIndex];
  app.innerHTML = sceneHtml({
    plain: true,
    content: `
      ${topbarHtml(`<div class="status-chip">完</div>`)}
      <div class="bottom">
        ${dialogueHtml(step.speaker, step.text)}
        ${
          game.endingIndex < ENDING_STEPS.length - 1
            ? `<button class="primary-button" data-action="ending-next">次へ</button>`
            : `<button class="primary-button" disabled>完</button>`
        }
      </div>
    `,
  });
}

function enterOpening() {
  game.screen = "opening";
  render();
}

function startIntro() {
  game.introIndex = 0;
  game.screen = "intro";
  render();
}

function advanceIntro() {
  game.introIndex += 1;
  if (game.introIndex >= INTRO_STEPS.length) {
    game.screen = "main";
    game.directionIndex = 0;
  }
  render();
}

function rotateDirection(delta) {
  game.directionIndex = (game.directionIndex + delta + DIRECTIONS.length) % DIRECTIONS.length;
  render();
}

function startNumberGuess() {
  const direction = currentDirection();
  if (game.defeated.has(direction.id)) {
    game.feedback = "もう勝った相手だ。次の方角を探そう。";
    renderMain();
    return;
  }
  game.currentCharacter = direction;
  game.secret = randomFourDigits();
  game.feedback = "";
  game.screen = "guess";
  render();
}

function submitGuess(value) {
  if (!/^\d{4}$/.test(value)) {
    game.feedback = "4桁の数字で答えなきゃ。";
    renderGuess();
    return;
  }
  game.guess = value;
  game.matchedDigits = scoreGuess(game.secret, value);
  game.grade = game.matchedDigits;
  game.pendingHands = {
    blue: instantiateHand(drawPlayerHand(game.grade), "blue"),
    red: instantiateHand(drawCpuHand(), "red"),
  };
  game.pendingFirstPlayer = Math.random() < 0.5 ? "blue" : "red";
  game.screen = "guess-result";
  render();
}

function startBattle() {
  const first = game.pendingFirstPlayer;
  game.battle = {
    board: Array(9).fill(null),
    blueHand: game.pendingHands.blue,
    redHand: game.pendingHands.red,
    turn: first,
    firstPlayer: first,
    selectedHandIndex: null,
    awaitingCpu: false,
    message: first === "blue" ? "あなたが先攻。" : `${game.currentCharacter.name}が先攻。`,
  };
  game.screen = "battle";
  render();
}

function finishWin() {
  game.defeated.add(game.currentCharacter.id);
  game.battle = null;
  game.outcome = null;
  if (game.defeated.size >= DIRECTIONS.length) {
    game.screen = "ending";
    game.endingIndex = 0;
  } else {
    game.screen = "main";
  }
  render();
}

function resetToOpening() {
  game.screen = "opening";
  game.introIndex = 0;
  game.directionIndex = 0;
  game.defeated = new Set();
  game.currentCharacter = null;
  game.battle = null;
  game.outcome = null;
  game.feedback = "";
  render();
}

function advanceEnding() {
  game.endingIndex = Math.min(game.endingIndex + 1, ENDING_STEPS.length - 1);
  render();
}

function selectPlayerCard(index) {
  const battle = game.battle;
  if (!battle || battle.turn !== "blue") return;
  battle.selectedHandIndex = index;
  battle.message = `${battle.blueHand[index].name}を選んだ。置く場所を選んで。`;
  render();
}

function placePlayerCard(position) {
  const battle = game.battle;
  if (!battle || battle.turn !== "blue") return;
  if (battle.selectedHandIndex === null) {
    battle.message = "先に手札を選んで。";
    render();
    return;
  }
  if (battle.board[position]) return;
  applyMove(battle, { owner: "blue", handIndex: battle.selectedHandIndex, position });
  render();
}

function scheduleCpuMove() {
  const battle = game.battle;
  if (!battle || battle.turn !== "red" || battle.awaitingCpu || isBattleOver(battle)) return;
  battle.awaitingCpu = true;
  window.setTimeout(() => {
    if (game.screen !== "battle" || !game.battle || game.battle.turn !== "red") return;
    const move = chooseCpuMove(game.battle);
    game.battle.awaitingCpu = false;
    applyMove(game.battle, move);
    render();
  }, 520);
}

function applyMove(battle, move) {
  const hand = handForOwner(battle, move.owner);
  const card = hand.splice(move.handIndex, 1)[0];
  battle.board[move.position] = { card, owner: move.owner };
  const captured = captureNeighbors(battle.board, move.position, card, move.owner);
  battle.selectedHandIndex = null;

  if (isBattleOver(battle)) {
    finishBattle();
    return;
  }

  battle.turn = opponent(move.owner);
  battle.message = `${ownerLabel(move.owner)}が${card.name}を置いた。${captured ? `${captured}枚ひっくり返した。` : "ひっくり返せなかった。"}`;
}

function finishBattle() {
  const battle = game.battle;
  const score = scoreBattle(battle);
  let result = "lose";
  let note = `負け。青${score.blue} - 赤${score.red}`;
  if (score.blue > score.red) {
    result = "win";
    note = `勝ち。青${score.blue} - 赤${score.red}`;
  } else if (score.blue === score.red) {
    note = `引き分け。青${score.blue} - 赤${score.red}。逃げ切れなかった。`;
  }
  game.outcome = { result, score, note };
  game.screen = "post-battle";
}

function captureNeighbors(board, position, card, owner) {
  let captured = 0;
  for (const neighbor of neighbors(position)) {
    const placed = board[neighbor.position];
    if (!placed || placed.owner === owner) continue;
    if (card[neighbor.ownSide] > placed.card[neighbor.neighborSide]) {
      placed.owner = owner;
      captured += 1;
    }
  }
  return captured;
}

function chooseCpuMove(battle) {
  const moves = legalMoves(battle);
  let bestMove = moves[0];
  let bestScore = -Infinity;
  for (const move of moves) {
    const score = combinedAiScore(battle, move);
    if (score > bestScore) {
      bestScore = score;
      bestMove = move;
    }
  }
  return bestMove;
}

function combinedAiScore(battle, move) {
  return modelScore(battle, move) + tacticalScore(battle, move, 0.25) * 0.8;
}

function modelScore(battle, move) {
  const features = extractMoveFeatures(battle, move);
  return Object.entries(features).reduce((sum, [name, value]) => sum + (MODEL_WEIGHTS[name] || 0) * value, 0);
}

function tacticalScore(battle, move, replyPenaltyWeight) {
  const owner = move.owner;
  const beforeOwned = ownedBoardCount(battle, owner);
  const next = simulateMove(battle, move);
  const afterOwned = ownedBoardCount(next, owner);
  const gain = afterOwned - beforeOwned;
  const score = scoreBattle(next);
  const scoreDiff = score[owner] - score[opponent(owner)];
  const card = handForOwner(battle, owner)[move.handIndex];
  let value = gain * 4.0 + scoreDiff * 1.5 + positionBonus(move.position) + cardAverage(card) / 10.0;

  if (replyPenaltyWeight && !isBattleOver(next)) {
    const replies = legalMoves(next);
    const opponentBest = Math.max(...replies.map((reply) => tacticalScoreWithoutReply(next, reply)));
    value -= opponentBest * replyPenaltyWeight;
  }

  if (isBattleOver(next)) {
    const winner = winnerOf(next);
    if (winner === owner) value += 100;
    if (winner === opponent(owner)) value -= 100;
  }
  return value;
}

function tacticalScoreWithoutReply(battle, move) {
  const owner = move.owner;
  const beforeOwned = ownedBoardCount(battle, owner);
  const next = simulateMove(battle, move);
  const afterOwned = ownedBoardCount(next, owner);
  const gain = afterOwned - beforeOwned;
  const score = scoreBattle(next);
  const scoreDiff = score[owner] - score[opponent(owner)];
  const card = handForOwner(battle, owner)[move.handIndex];
  let value = gain * 4.0 + scoreDiff * 1.5 + positionBonus(move.position) + cardAverage(card) / 10.0;
  if (isBattleOver(next)) {
    const winner = winnerOf(next);
    if (winner === owner) value += 100;
    if (winner === opponent(owner)) value -= 100;
  }
  return value;
}

function extractMoveFeatures(battle, move) {
  const owner = move.owner;
  const card = handForOwner(battle, owner)[move.handIndex];
  const next = simulateMove(battle, move);
  const score = scoreBattle(next);
  const beforeOwned = ownedBoardCount(battle, owner);
  const afterOwned = ownedBoardCount(next, owner);
  const row = Math.floor(move.position / 3);
  const col = move.position % 3;
  const adjacent = adjacentOwnerCounts(battle, move.position, owner);

  return {
    bias: 1.0,
    turn_index: moveCount(battle) / 8.0,
    is_blue: owner === "blue" ? 1.0 : 0.0,
    is_red: owner === "red" ? 1.0 : 0.0,
    is_first_player: owner === battle.firstPlayer ? 1.0 : 0.0,
    is_second_player: owner === secondPlayer(battle) ? 1.0 : 0.0,
    self_hand_count: handForOwner(battle, owner).length / 5.0,
    opponent_hand_count: handForOwner(battle, opponent(owner)).length / 5.0,
    self_board_count: ownedBoardCount(battle, owner) / 9.0,
    opponent_board_count: ownedBoardCount(battle, opponent(owner)) / 9.0,
    card_grade: card.grade / 4.0,
    card_top: card.top / 10.0,
    card_right: card.right / 10.0,
    card_bottom: card.bottom / 10.0,
    card_left: card.left / 10.0,
    card_average: cardAverage(card) / 10.0,
    position: move.position / 8.0,
    row: row / 2.0,
    col: col / 2.0,
    is_center: move.position === 4 ? 1.0 : 0.0,
    is_corner: [0, 2, 6, 8].includes(move.position) ? 1.0 : 0.0,
    is_edge: [1, 3, 5, 7].includes(move.position) ? 1.0 : 0.0,
    adjacent_self: adjacent.self / 4.0,
    adjacent_opponent: adjacent.opponent / 4.0,
    adjacent_empty: adjacent.empty / 4.0,
    ownership_gain: (afterOwned - beforeOwned) / 5.0,
    score_diff_after: (score[owner] - score[opponent(owner)]) / 10.0,
    wins_immediately: isBattleOver(next) && winnerOf(next) === owner ? 1.0 : 0.0,
    loses_immediately: isBattleOver(next) && winnerOf(next) === opponent(owner) ? 1.0 : 0.0,
  };
}

function simulateMove(battle, move) {
  const clone = cloneBattle(battle);
  const hand = handForOwner(clone, move.owner);
  const card = hand.splice(move.handIndex, 1)[0];
  clone.board[move.position] = { card, owner: move.owner };
  captureNeighbors(clone.board, move.position, card, move.owner);
  if (!isBattleOver(clone)) clone.turn = opponent(move.owner);
  return clone;
}

function legalMoves(battle) {
  if (isBattleOver(battle)) return [];
  const hand = handForOwner(battle, battle.turn);
  const moves = [];
  for (let handIndex = 0; handIndex < hand.length; handIndex += 1) {
    for (let position = 0; position < battle.board.length; position += 1) {
      if (!battle.board[position]) moves.push({ owner: battle.turn, handIndex, position });
    }
  }
  return moves;
}

function scoreBattle(battle) {
  const score = { blue: 0, red: 0 };
  for (const cell of battle.board) {
    if (cell) score[cell.owner] += 1;
  }
  const second = secondPlayer(battle);
  score[second] += handForOwner(battle, second).length;
  return score;
}

function winnerOf(battle) {
  const score = scoreBattle(battle);
  if (score.blue > score.red) return "blue";
  if (score.red > score.blue) return "red";
  return null;
}

function isBattleOver(battle) {
  return moveCount(battle) === 9;
}

function moveCount(battle) {
  return battle.board.filter(Boolean).length;
}

function secondPlayer(battle) {
  return opponent(battle.firstPlayer);
}

function handForOwner(battle, owner) {
  return owner === "blue" ? battle.blueHand : battle.redHand;
}

function ownedBoardCount(battle, owner) {
  return battle.board.filter((cell) => cell && cell.owner === owner).length;
}

function adjacentOwnerCounts(battle, position, owner) {
  const counts = { self: 0, opponent: 0, empty: 0 };
  for (const neighborPosition of neighborPositions(position)) {
    const cell = battle.board[neighborPosition];
    if (!cell) counts.empty += 1;
    else if (cell.owner === owner) counts.self += 1;
    else counts.opponent += 1;
  }
  return counts;
}

function cloneBattle(battle) {
  return {
    board: battle.board.map((cell) => (cell ? { card: cell.card, owner: cell.owner } : null)),
    blueHand: [...battle.blueHand],
    redHand: [...battle.redHand],
    turn: battle.turn,
    firstPlayer: battle.firstPlayer,
    selectedHandIndex: battle.selectedHandIndex,
    awaitingCpu: false,
    message: battle.message,
  };
}

function neighbors(position) {
  const result = [];
  const row = Math.floor(position / 3);
  const col = position % 3;
  if (row > 0) result.push({ position: position - 3, ownSide: "top", neighborSide: "bottom" });
  if (col < 2) result.push({ position: position + 1, ownSide: "right", neighborSide: "left" });
  if (row < 2) result.push({ position: position + 3, ownSide: "bottom", neighborSide: "top" });
  if (col > 0) result.push({ position: position - 1, ownSide: "left", neighborSide: "right" });
  return result;
}

function neighborPositions(position) {
  return neighbors(position).map((neighbor) => neighbor.position);
}

function drawPlayerHand(grade) {
  const pool = CARDS.filter((card) => card.grade === grade);
  return Array.from({ length: 5 }, () => pool[Math.floor(Math.random() * pool.length)]);
}

function drawCpuHand() {
  const shuffled = [...CARDS].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, 5);
}

function instantiateHand(cards, owner) {
  return cards.map((card) => ({ ...card, uid: `${owner}-${cardInstanceId++}` }));
}

function scoreGuess(secret, guess) {
  let score = 0;
  for (let index = 0; index < 4; index += 1) {
    if (secret[index] === guess[index]) score += 1;
  }
  return score;
}

function randomFourDigits() {
  return String(Math.floor(Math.random() * 10000)).padStart(4, "0");
}

function currentDirection() {
  return DIRECTIONS[game.directionIndex];
}

function opponent(owner) {
  return owner === "blue" ? "red" : "blue";
}

function ownerLabel(owner) {
  return owner === "blue" ? "青" : "赤";
}

function cardAverage(card) {
  return (card.top + card.right + card.bottom + card.left) / 4;
}

function positionBonus(position) {
  if (position === 4) return 0.6;
  if ([0, 2, 6, 8].includes(position)) return 0.35;
  return 0.15;
}

function unlockAudio() {
  bgm.play().catch(() => {});
}

function setMusic(src, loop) {
  if (bgm.dataset.src !== src) {
    bgm.dataset.src = src;
    bgm.src = src;
    bgm.loop = loop;
    bgm.volume = game.muted ? 0 : 0.62;
  }
  bgm.play().catch(() => {});
}

function toggleMute() {
  game.muted = !game.muted;
  bgm.volume = game.muted ? 0 : 0.62;
  render();
}

function sceneHtml({ image = "", plain = false, className = "", content }) {
  const style = image ? `style="--bg: url('${image.replace(/'/g, "%27")}')"` : "";
  return `<main class="scene${plain ? " scene--plain" : ""}${className}" ${style}>${content}</main>`;
}

function topbarHtml(extra) {
  return `
    <div class="topbar">
      <div class="status-strip">${extra || ""}</div>
      <button class="icon-button" data-action="toggle-mute" aria-label="音量切替">${game.muted ? "×" : "♪"}</button>
    </div>
  `;
}

function dialogueHtml(speaker, text) {
  return `
    <div class="dialogue">
      <div class="speaker">${escapeHtml(speaker)}：</div>
      <div class="dialogue-text">${escapeHtml(text)}</div>
    </div>
  `;
}

function progressHtml() {
  return `
    <div class="progress-list">
      ${DIRECTIONS.map(
        (direction) =>
          `<div class="progress-item${game.defeated.has(direction.id) ? " done" : ""}">${escapeHtml(direction.label)}</div>`,
      ).join("")}
    </div>
  `;
}

function boardHtml(battle) {
  return battle.board
    .map((cell, index) => {
      if (cell) return `<button class="cell" disabled>${cardHtml(cell.card, cell.owner)}</button>`;
      const canPlace = battle.turn === "blue" && battle.selectedHandIndex !== null;
      return `<button class="cell" ${canPlace ? `data-cell-index="${index}"` : "disabled"}></button>`;
    })
    .join("");
}

function handHtml(hand, owner, selectable) {
  if (!hand.length) {
    return Array.from({ length: 5 }, () => `<div class="empty-card"></div>`).join("");
  }
  const cards = hand
    .map((card, index) => {
      const selected = owner === "blue" && game.battle?.selectedHandIndex === index;
      if (selectable) {
        return `<button class="card-button ${owner}${selected ? " selected" : ""}" data-card-index="${index}">${cardInnerHtml(card)}</button>`;
      }
      return `<div class="card-face ${owner}">${cardInnerHtml(card)}</div>`;
    })
    .join("");
  const blanks = Array.from({ length: Math.max(0, 5 - hand.length) }, () => `<div class="empty-card"></div>`).join("");
  return cards + blanks;
}

function cardHtml(card, owner) {
  return `<div class="card-face ${owner}">${cardInnerHtml(card)}</div>`;
}

function cardInnerHtml(card) {
  return `
    <span class="card-value top">${card.top}</span>
    <span class="card-value right">${card.right}</span>
    <span class="card-value bottom">${card.bottom}</span>
    <span class="card-value left">${card.left}</span>
    <span class="card-name">${escapeHtml(card.name)}</span>
  `;
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
