"use strict";

const IMAGE_PATH = "WebpImage/";
const MUSIC_PATH = "Music/";

const ASSETS = {
  images: {
    opening: `${IMAGE_PATH}OP.webp`,
    dupontTrain: `${IMAGE_PATH}Dupont_Train.webp`,
    introClosed: `${IMAGE_PATH}Intro_ClosingCrossingGate.webp`,
    introSouth: `${IMAGE_PATH}Intro_To_South.webp`,
    introOpen: `${IMAGE_PATH}Intro_OpeningCrossingGate.webp`,
    north: `${IMAGE_PATH}To_North.webp`,
    south: `${IMAGE_PATH}To_South.webp`,
    east: `${IMAGE_PATH}To_East.webp`,
    west: `${IMAGE_PATH}To_West.webp`,
  },
  music: {
    opening: `${MUSIC_PATH}Train-Invitation to Cyberspace.wav`,
    main: `${MUSIC_PATH}Opening-Invitation to Cyberspace.wav`,
    ending: `${MUSIC_PATH}DJ_Dupont.mp3`,
  },
};

const DEFAULT_MUSIC_VOLUME = 0.62;
const QUIET_MUSIC_VOLUME = DEFAULT_MUSIC_VOLUME * 0.8;
const ENDING_EXIT_URL = "https://x.com/te_hen1919810";

// 数字当ては最大3回。途中で4ヒットなら、その場で最高グレードを確定します。
const MAX_GUESS_ATTEMPTS = 3;
const GUESS_FORMAT_ERROR = "4桁の数字で答えなきゃ。";

// デバッグ用チート表示です。公開前は false にするか、この行をコメントアウトしてください。
const DEBUG_SHOW_SECRET_NUMBER = false;

const DIRECTIONS = [
  {
    id: "north",
    label: "北",
    image: ASSETS.images.north,
    name: "アメカジさん",
    lines: [
      "まゆみちゃん。あんたの自転車の鍵の番号なんだっけ？",
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
      "素敵な音楽だったね。",
      "あなたも上に乗って。",
    ],
  },
  {
    id: "south",
    label: "南",
    image: ASSETS.images.south,
    name: "美容師",
    lines: [
      "オレのケー番の下４桁当ててみて。",
      "xxxxだよ。",
      "申し訳ございませんでした。２か月後に来てください。",
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
      "やるじゃねぇか！！",
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
    text: "（カットだけで８千円もする美容室だったのに、狂ってる・・・逃げなきゃ！）",
  },
];

const ENDING_STEPS = [
  { speaker: "てほん", text: "これローソンで使える500円クーポン券だけど、使わないでね。https://apli.lawson.jp/ldcp/login/?campaignId=sjabtpu9zk&encDataCode=5ED8D094000919A57DC2327ECC46A1582E903B110C28E1D34F6045874169A48D" },
  { speaker: "てほん", text: "こんなげーむにまじになっちゃってどうするの 完" },
];

const CARD_DEFINITIONS = [
  ["G0-01", "薄闇の/鍵音", 0, 9, 2, 2, 1],
  ["G0-02", "駅の/裏出口", 0, 1, 9, 2, 2],
  ["G0-03", "湿った/切符", 0, 2, 1, 9, 2],
  ["G0-04", "消灯した/路地", 0, 2, 2, 1, 9],
  ["G0-05", "深夜の/改札", 0, 6, 3, 3, 2],
  ["G0-06", "古傷の/写真", 0, 2, 6, 3, 3],
  ["G0-07", "忘れられた/雨傘", 0, 3, 2, 6, 3],
  ["G0-08", "黒電話の/呼出", 0, 3, 3, 2, 6],
  ["G0-09", "段差の/影", 0, 4, 4, 3, 3],
  ["G0-10", "作業灯の/火花", 0, 5, 3, 3, 3],
  ["G0-11", "赤信号の/無音", 0, 3, 5, 3, 3],
  ["G0-12", "終電の/遅延", 0, 3, 3, 5, 3],
  ["G0-13", "袖口の/血痕", 0, 3, 3, 3, 5],
  ["G0-14", "鍵束の/鈍色", 0, 5, 2, 5, 2],
  ["G0-15", "非常口の/青灯", 0, 2, 5, 2, 5],
  ["G0-16", "地下道の/靴音", 0, 7, 2, 3, 2],
  ["G0-17", "死者を/呼ぶ音", 0, 2, 7, 2, 3],
  ["G0-18", "窓際の/冷気", 0, 3, 2, 7, 2],
  ["G0-19", "封印/手紙", 0, 2, 3, 2, 7],
  ["G0-20", "サンダー/力学", 0, 4, 4, 3, 3],
  ["G1-01", "少しの/警告", 1, 8, 3, 3, 3],
  ["G1-02", "廃線の/灯り", 1, 3, 8, 3, 3],
  ["G1-03", "追跡の/足音", 1, 3, 3, 8, 3],
  ["G1-04", "地獄への/誘い", 1, 3, 3, 3, 8],
  ["G1-05", "最後の/白線", 1, 6, 4, 4, 3],
  ["G1-06", "裏口/合図", 1, 3, 6, 4, 4],
  ["G1-07", "焦げた/工具", 1, 4, 3, 6, 4],
  ["G1-08", "静寂な/雑音", 1, 4, 4, 3, 6],
  ["G1-09", "あの人の/影", 1, 5, 5, 4, 3],
  ["G1-10", "一斉の/叫び", 1, 3, 5, 5, 4],
  ["G1-11", "デビル/サイト", 1, 4, 3, 5, 5],
  ["G1-12", "残響/記憶", 1, 5, 4, 3, 5],
  ["G1-13", "コインの/裏面", 1, 7, 2, 5, 3],
  ["G1-14", "細工された/針金", 1, 3, 7, 2, 5],
  ["G1-15", "開かずの/改札", 1, 5, 3, 7, 2],
  ["G1-16", "あの/予定", 1, 2, 5, 3, 7],
  ["G1-17", "仮眠/夢見", 1, 4, 4, 4, 4],
  ["G1-18", "未読の/手紙", 1, 7, 3, 3, 3],
  ["G1-19", "街灯/点滅", 1, 3, 7, 3, 3],
  ["G1-20", "イリーガル/デビル", 1, 3, 3, 7, 3],
  ["G2-01", "監視/カメラ", 2, 9, 5, 4, 4],
  ["G2-02", "深層/ログ", 2, 4, 9, 5, 4],
  ["G2-03", "切断/回線", 2, 4, 4, 9, 5],
  ["G2-04", "青白い/画面", 2, 5, 4, 4, 9],
  ["G2-05", "指紋/照合", 2, 7, 6, 5, 4],
  ["G2-06", "警笛/遠く", 2, 4, 7, 6, 5],
  ["G2-07", "非常/突破", 2, 5, 4, 7, 6],
  ["G2-08", "現場の/血", 2, 6, 5, 4, 7],
  ["G2-09", "隠し/階段", 2, 8, 3, 8, 3],
  ["G2-10", "照明/落下", 2, 3, 8, 3, 8],
  ["G2-11", "合鍵/コピー", 2, 6, 6, 5, 5],
  ["G2-12", "微熱/診断", 2, 10, 4, 4, 4],
  ["G2-13", "無人駅/時計", 2, 6, 5, 5, 5],
  ["G2-14", "路線図/赤丸", 2, 8, 5, 4, 4],
  ["G2-15", "硝子の/亀裂", 2, 4, 8, 5, 4],
  ["G2-16", "電光/掲示", 2, 4, 4, 8, 5],
  ["G2-17", "黒服/フィッシュ", 2, 5, 4, 4, 8],
  ["G2-18", "留守電/逆再生", 2, 7, 7, 4, 3],
  ["G2-19", "禁止された/領域", 2, 3, 7, 7, 4],
  ["G2-20", "記録/消去", 2, 4, 3, 7, 7],
  ["G3-01", "逃走/経路", 3, 10, 7, 6, 5],
  ["G3-02", "偽装/書類", 3, 5, 10, 7, 6],
  ["G3-03", "鈍い/金属音", 3, 6, 5, 10, 7],
  ["G3-04", "逆光の/人影", 3, 7, 6, 5, 10],
  ["G3-05", "施錠/解除", 3, 9, 7, 6, 5],
  ["G3-06", "白煙/の残像", 3, 5, 9, 7, 6],
  ["G3-07", "制御室/の赤灯", 3, 6, 5, 9, 7],
  ["G3-08", "空席の/列車", 3, 7, 6, 5, 9],
  ["G3-09", "心霊/現像", 3, 8, 8, 6, 5],
  ["G3-10", "送信/失敗", 3, 5, 8, 8, 6],
  ["G3-11", "振動/ローム", 3, 6, 5, 8, 8],
  ["G3-12", "証拠/の欠片", 3, 8, 6, 5, 8],
  ["G3-13", "応答の/無い人", 3, 10, 4, 9, 4],
  ["G3-14", "沈む/ホーム", 3, 4, 10, 4, 9],
  ["G3-15", "逃げ道/消失", 3, 9, 4, 10, 4],
  ["G3-16", "鍵穴/ブローカー", 3, 4, 9, 4, 10],
  ["G3-17", "死の/報告", 3, 7, 7, 7, 6],
  ["G3-18", "歪んだ/鏡", 3, 6, 7, 7, 7],
  ["G3-19", "黒幕/の足跡", 3, 8, 7, 6, 6],
  ["G3-20", "訪れない/終点", 3, 6, 8, 7, 6],
  ["G4-01", "電脳/マシン", 4, 9, 8, 7, 5],
  ["G4-02", "虚空の/愛", 4, 5, 9, 8, 7],
  ["G4-03", "断罪の/時間", 4, 7, 5, 9, 8],
  ["G4-04", "危険/領域", 4, 8, 7, 5, 9],
  ["G4-05", "極夜/零度", 4, 9, 9, 6, 5],
  ["G4-06", "残酷な/出来事", 4, 5, 9, 9, 6],
  ["G4-07", "制圧/コード", 4, 6, 5, 9, 9],
  ["G4-08", "冷徹な/追跡者", 4, 9, 6, 5, 9],
  ["G4-09", "無音/急行", 4, 8, 8, 7, 6],
  ["G4-10", "閉鎖/区画", 4, 6, 8, 8, 7],
  ["G4-11", "真相の/直前", 4, 7, 6, 8, 8],
  ["G4-12", "漆黒な/階層", 4, 8, 7, 6, 8],
  ["G4-13", "未知の/領域", 4, 9, 7, 9, 4],
  ["G4-14", "閃光/ダイナマイト", 4, 4, 9, 7, 9],
  ["G4-15", "限界/突破", 4, 9, 4, 9, 7],
  ["G4-16", "狂った/回路", 4, 7, 9, 4, 9],
  ["G4-17", "災厄を/呼ぶ番号", 4, 7, 7, 7, 7],
  ["G4-18", "最後の/時", 4, 9, 8, 6, 5],
  ["G4-19", "完全/包囲", 4, 5, 9, 8, 6],
  ["G4-20", "醒める/夢", 4, 6, 5, 9, 8],
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
  // 画面内テンキーで入力中の数字です。スマホのキーボードには依存しません。
  guessDraft: "",
  guessHistory: [],
  matchedDigits: 0,
  blowDigits: 0,
  grade: 0,
  guessCompleteReason: "",
  pendingHands: null,
  pendingFirstPlayer: "blue",
  battle: null,
  outcome: null,
  endingIndex: 0,
  feedback: "",
};

app.addEventListener("click", onClick);
render();

function onClick(event) {
  const target = event.target.closest("[data-action], [data-card-index], [data-cell-index], [data-guess-digit]");
  if (!target) return;

  if (target.dataset.cardIndex !== undefined) {
    selectPlayerCard(Number(target.dataset.cardIndex));
    return;
  }

  if (target.dataset.cellIndex !== undefined) {
    placePlayerCard(Number(target.dataset.cellIndex));
    return;
  }

  if (target.dataset.guessDigit !== undefined) {
    appendGuessDigit(target.dataset.guessDigit);
    return;
  }

  const action = target.dataset.action;
  unlockAudio();

  if (action === "enter-opening") enterOpening();
  if (action === "start-intro") startIntro();
  if (action === "external-link") window.location.href = "https://tenki.jp/";
  if (action === "intro-next") advanceIntro();
  if (action === "go-direction") goDirection(Number(target.dataset.directionIndex));
  if (action === "nav-left") rotateDirection(-1);
  if (action === "nav-right") rotateDirection(1);
  if (action === "talk") startNumberGuess();
  if (action === "guess-clear") clearGuessDraft();
  if (action === "guess-delete") deleteGuessDigit();
  if (action === "submit-guess-keypad") submitGuess(game.guessDraft);
  if (action === "start-battle") startBattle();
  if (action === "finish-win") finishWin();
  if (action === "reset-opening") resetToOpening();
  if (action === "ending-next") advanceEnding();
  if (action === "ending-exit") window.location.href = ENDING_EXIT_URL;
  if (action === "toggle-mute") toggleMute();
}

function appendGuessDigit(digit) {
  // テンキーの数字ボタンを押した時だけ、4桁まで入力中の数字に追加します。
  if (game.screen !== "guess" || !/^\d$/.test(digit) || game.guessDraft.length >= 4) return;
  game.guessDraft += digit;
  clearGuessFormatError();
  renderGuess();
}

function deleteGuessDigit() {
  // 1文字戻すボタン用です。空の時は何も起きません。
  if (game.screen !== "guess" || !game.guessDraft) return;
  game.guessDraft = game.guessDraft.slice(0, -1);
  clearGuessFormatError();
  renderGuess();
}

function clearGuessDraft() {
  // Cボタン用です。入力中の数字だけを消し、対戦状況や履歴は残します。
  if (game.screen !== "guess" || !game.guessDraft) return;
  game.guessDraft = "";
  clearGuessFormatError();
  renderGuess();
}

function clearGuessFormatError() {
  // 桁数不足の注意だけ消します。直前のヒット＆ブロー台詞は履歴と合わせて残します。
  if (game.feedback === GUESS_FORMAT_ERROR) game.feedback = "";
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
          <button class="command-button" data-action="start-intro">「髪を切らせてくれてありがとうございます。」</button>
          <button class="command-button" data-action="external-link">天気を確認する</button>
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
  const nextAttempt = Math.min(game.guessHistory.length + 1, MAX_GUESS_ATTEMPTS);
  const dialogueText = game.feedback || character.lines[0];
  const debugSecretChip = DEBUG_SHOW_SECRET_NUMBER ? `<div class="status-chip debug-chip">DEBUG 正解：${game.secret}</div>` : "";
  app.innerHTML = sceneHtml({
    image: character.image,
    content: `
      ${topbarHtml(`<div class="status-chip">${character.label}：${character.name}</div><div class="status-chip">挑戦：${nextAttempt}/${MAX_GUESS_ATTEMPTS}</div>${debugSecretChip}`)}
      <div class="bottom">
        ${dialogueHtml(character.name, dialogueText)}
        <div class="guess-panel">
          ${guessDisplayHtml()}
          ${guessKeypadHtml()}
        </div>
        ${guessHistoryHtml()}
      </div>
    `,
  });
}

function renderGuessResult() {
  const character = game.currentCharacter;
  const answerLine = character.lines[1].replace("xxxx", game.secret).replace("XXXX", game.secret);
  const resultLine = game.guessCompleteReason === "perfect" ? perfectGuessResultLine(character) : answerLine;
  const resultMessage = `最終回答：${game.guess} / 正解：${game.secret} / ${game.matchedDigits}ヒット、${game.blowDigits}ブロー / カードグレード：${game.grade}`;
  app.innerHTML = sceneHtml({
    image: character.image,
    content: `
      ${topbarHtml(`<div class="status-chip">${game.matchedDigits}ヒット</div><div class="status-chip">${game.blowDigits}ブロー</div><div class="status-chip">グレード${game.grade}</div>`)}
      <div class="bottom">
        ${dialogueHtml(character.name, resultLine)}
        ${guessHistoryHtml()}
        <div class="battle-message">${escapeHtml(resultMessage)}</div>
        <button class="primary-button" data-action="start-battle">カードバトルへ</button>
      </div>
    `,
  });
}

function renderBattle() {
  const battle = game.battle;
  const score = displayScoreBattle(battle);
  const turnText = battle.turn === "blue" ? "あなたの番" : `${game.currentCharacter.name}の番`;
  app.innerHTML = sceneHtml({
    image: game.currentCharacter.image,
    content: `
      ${topbarHtml(`<button class="surrender-button" data-action="reset-opening">諦める</button><div class="status-chip">${turnText}</div><div class="status-chip">先攻：${ownerLabel(battle.firstPlayer)}</div>`)}
      <div class="bottom battle-shell">
        <div class="battle-message">${battle.messageHtml || escapeHtml(battle.message)}</div>
        <div class="score-row">
          <div class="score-box">青 ${score.blue}</div>
          <div class="score-box">${turnText}</div>
          <div class="score-box">赤 ${score.red}</div>
        </div>
        <div class="hand-panel">
          <div class="hand-title">${game.currentCharacter.name}の手札</div>
          <div class="hand-list">${handHtml(battle.redHand, "red", false)}</div>
        </div>
        <div class="battle-board">${boardHtml(battle)}</div>
        <div class="hand-panel">
          <div class="hand-title">あなたの手札</div>
          <div class="hand-list">${handHtml(battle.blueHand, "blue", battle.turn === "blue")}</div>
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
    image: ASSETS.images.dupontTrain,
    content: `
      ${topbarHtml(`<div class="status-chip">完</div>`)}
      <div class="bottom">
        ${dialogueHtml(step.speaker, step.text)}
        ${
          game.endingIndex < ENDING_STEPS.length - 1
            ? `<button class="primary-button" data-action="ending-next">次へ</button>`
            : `<button class="primary-button" data-action="ending-exit">完</button>`
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

function goDirection(index) {
  if (!Number.isInteger(index) || index < 0 || index >= DIRECTIONS.length) return;
  game.directionIndex = index;
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
  game.guess = "";
  game.guessDraft = "";
  game.guessHistory = [];
  game.matchedDigits = 0;
  game.blowDigits = 0;
  game.grade = 0;
  game.guessCompleteReason = "";
  game.pendingHands = null;
  game.feedback = "";
  game.screen = "guess";
  render();
}

function submitGuess(value) {
  if (!/^\d{4}$/.test(value)) {
    game.feedback = GUESS_FORMAT_ERROR;
    renderGuess();
    return;
  }

  const result = scoreHitAndBlow(game.secret, value);
  const attempt = game.guessHistory.length + 1;
  game.guess = value;
  game.guessDraft = "";
  game.matchedDigits = result.hits;
  game.blowDigits = result.blows;
  game.guessHistory.push({ attempt, value, hits: result.hits, blows: result.blows });

  if (result.hits === 4) {
    game.feedback = perfectGuessResultLine(game.currentCharacter);
    completeNumberGuess("perfect");
    return;
  }

  if (game.guessHistory.length >= MAX_GUESS_ATTEMPTS) {
    completeNumberGuess("attempts");
    return;
  }

  game.feedback = hitAndBlowLine(game.currentCharacter, result, MAX_GUESS_ATTEMPTS - game.guessHistory.length);
  renderGuess();
}

function completeNumberGuess(reason) {
  // カードの強さは最後に出たヒット数で決まります。途中4ヒットなら必ずグレード4です。
  game.grade = game.matchedDigits;
  game.guessCompleteReason = reason;
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
    messageHtml: "",
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
  game.guess = "";
  game.guessDraft = "";
  game.guessHistory = [];
  game.matchedDigits = 0;
  game.blowDigits = 0;
  game.grade = 0;
  game.guessCompleteReason = "";
  game.pendingHands = null;
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
  battle.message = "";
  battle.messageHtml = `${cardNameMessageHtml(battle.blueHand[index], "blue")}を選んだ。置く場所を選んで。`;
  render();
}

function placePlayerCard(position) {
  const battle = game.battle;
  if (!battle || battle.turn !== "blue") return;
  if (battle.selectedHandIndex === null) {
    battle.message = "先に手札を選んで。";
    battle.messageHtml = "";
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
  battle.message = "";
  battle.messageHtml = `${ownerLabel(move.owner)}が${cardNameMessageHtml(card, move.owner)}を置いた。${captured ? `${captured}枚ひっくり返した。` : "ひっくり返せなかった。"}`;
}

function finishBattle() {
  const battle = game.battle;
  const score = scoreBattle(battle);
  const playerWon = score.blue >= score.red;
  const result = playerWon ? "win" : "lose";
  let note = playerWon ? `勝ち。青${score.blue} - 赤${score.red}` : `負け。青${score.blue} - 赤${score.red}`;
  if (score.blue === score.red) note = `引き分け。青${score.blue} - 赤${score.red}。同点なので逃げ切り成功。`;
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

function displayScoreBattle(battle) {
  // 試合中の参考値は、青赤どちらも「盤面の所有枚数 + 残り手札」で表示します。
  const score = { blue: 0, red: 0 };
  for (const cell of battle.board) {
    if (cell) score[cell.owner] += 1;
  }
  score.blue += battle.blueHand.length;
  score.red += battle.redHand.length;
  return score;
}

function winnerOf(battle) {
  const score = scoreBattle(battle);
  // このゲームでは同点ならプレイヤー側（青）の勝ちとして扱います。
  if (score.blue >= score.red) return "blue";
  return "red";
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
    messageHtml: battle.messageHtml,
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
  return scoreHitAndBlow(secret, guess).hits;
}

function scoreHitAndBlow(secret, guess) {
  // ヒットは「数字も位置も一致」、ブローは「数字だけ一致」。同じ数字の重複も数え過ぎないようにします。
  let hits = 0;
  const secretRest = {};
  const guessRest = {};

  for (let index = 0; index < 4; index += 1) {
    if (secret[index] === guess[index]) {
      hits += 1;
    } else {
      secretRest[secret[index]] = (secretRest[secret[index]] || 0) + 1;
      guessRest[guess[index]] = (guessRest[guess[index]] || 0) + 1;
    }
  }

  let blows = 0;
  for (const digit of Object.keys(guessRest)) {
    blows += Math.min(guessRest[digit], secretRest[digit] || 0);
  }

  return { hits, blows };
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
    bgm.volume = game.muted ? 0 : musicVolume(src);
  }
  bgm.play().catch(() => {});
}

function toggleMute() {
  game.muted = !game.muted;
  bgm.volume = game.muted ? 0 : musicVolume(bgm.dataset.src);
  render();
}

function musicVolume(src) {
  // 通常BGM2曲だけ、以前の8割程度の音量に下げます。エンディング曲は元の音量です。
  if (src === ASSETS.music.opening || src === ASSETS.music.main) return QUIET_MUSIC_VOLUME;
  return DEFAULT_MUSIC_VOLUME;
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

function guessDisplayHtml() {
  // 入力中の4桁を、スマホキーボードではなく画面内の枠として見せます。
  const slots = Array.from({ length: 4 }, (_, index) => {
    const digit = game.guessDraft[index] || "";
    const filledClass = digit ? " is-filled" : "";
    return `<span class="guess-digit-slot${filledClass}">${escapeHtml(digit)}</span>`;
  }).join("");

  return `<div class="guess-display" aria-label="入力中の4桁">${slots}</div>`;
}

function guessKeypadHtml() {
  // 電卓風テンキーです。4桁そろうまで「答える」は押せないようにします。
  const digitButtons = ["1", "2", "3", "4", "5", "6", "7", "8", "9"]
    .map((digit) => `<button class="keypad-button" type="button" data-guess-digit="${digit}" aria-label="${digit}を入力">${digit}</button>`)
    .join("");
  const submitDisabled = game.guessDraft.length === 4 ? "" : " disabled";

  return `
    <div class="guess-keypad">
      ${digitButtons}
      <button class="keypad-button keypad-utility" type="button" data-action="guess-clear" aria-label="入力を消す">C</button>
      <button class="keypad-button" type="button" data-guess-digit="0" aria-label="0を入力">0</button>
      <button class="keypad-button keypad-utility" type="button" data-action="guess-delete" aria-label="1文字戻す">←</button>
      <button class="keypad-button keypad-submit" type="button" data-action="submit-guess-keypad"${submitDisabled}>答える</button>
    </div>
  `;
}

function guessHistoryHtml() {
  if (!game.guessHistory.length) return "";
  return `
    <div class="guess-history">
      ${game.guessHistory
        .map(
          (record) => `
            <div class="guess-history-row">
              <span>${record.attempt}回目</span>
              <span>${escapeHtml(record.value)}</span>
              <span>${record.hits}ヒット / ${record.blows}ブロー</span>
            </div>
          `,
        )
        .join("")}
    </div>
  `;
}

function hitAndBlowLine(character, result, remainingAttempts) {
  // 3回目までは答えを明かさず、ヒット数とブロー数だけでプレイヤーを誘導します。
  const scoreText = `${result.hits}ヒット、${result.blows}ブロー`;
  if (character.id === "south") {
    return `${scoreText}だぜ。切り口は悪くないな。あと${remainingAttempts}回。`;
  }
  if (character.id === "west") {
    return `${scoreText}だ。意識はまだあるな、あと${remainingAttempts}回。`;
  }
  if (character.id === "east") {
    return `${scoreText}。音が少し近づいた。あと${remainingAttempts}回。`;
  }
  return `${scoreText}。鍵穴が少し動いたよ。あと${remainingAttempts}回。`;
}

function perfectGuessResultLine(character) {
  // 奇跡の4ヒット時は数字当てを即終了し、最高グレードの手札でカードバトルに進みます。
  if (character.id === "south") {
    return "4ヒット。うわ、そこまでピタッと当てる？最高グレードで勝負だぜ。";
  }
  if (character.id === "west") {
    return "4ヒットだ。計器より正確じゃないか。最高グレードでいくぞ。";
  }
  if (character.id === "east") {
    return "4ヒット。今の音、ぜんぶ綺麗に重なった。最高グレードだよ。";
  }
  return "4ヒット。鍵番号、完全に思い出したんだね。最高グレードだよ。";
}

function progressHtml() {
  return `
    <div class="progress-list">
      ${DIRECTIONS.map(
        (direction, index) =>
          `<button class="progress-item${game.defeated.has(direction.id) ? " done" : ""}${game.directionIndex === index ? " current" : ""}" data-action="go-direction" data-direction-index="${index}">${escapeHtml(direction.label)}</button>`,
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
    <span class="card-name">${cardNameHtml(card.name)}</span>
  `;
}

function cardNameHtml(name) {
  // カード中央の名前は「/」区切りを行として扱い、最大3行・各行4文字までに抑えます。
  return String(name)
    .split("/")
    .slice(0, 3)
    .map((line) => `<span>${escapeHtml(line.slice(0, 4))}</span>`)
    .join("");
}

function cardNameMessageHtml(card, owner) {
  const className = owner === "blue" ? "blue" : "red";
  return `<strong class="battle-card-name ${className}">&quot;${escapeHtml(cardReadableName(card))}&quot;</strong>`;
}

function cardReadableName(card) {
  // メッセージ欄では「真相の/直前」のような行分け名を、自然な1行の通り名にします。
  const lines = String(card.name).split("/").filter(Boolean);
  return lines.reduce((name, line) => {
    if (!name) return line;
    if (name.endsWith("の") || line.startsWith("の")) return `${name}${line}`;
    return `${name}の${line}`;
  }, "");
}

function escapeHtml(value) {
  return String(value)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}
