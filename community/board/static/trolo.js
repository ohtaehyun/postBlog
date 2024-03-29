const row = document.querySelector(".row1");
const addListBtn = document.querySelector(".add-list-btn");
const body = document.querySelector("body");
const wrapper = document.querySelector(".wrapper");

const CLASS_BUBBLE = "bubble";
const CLASS_DISPLAY_NONE = "display-none";
const CLASS_CARD = "card";
const CLASS_MODAL_FRAME = "modal-frame";
const CLASS_CARD_TEXT = "card-text";
const CLASS_MODAL = "modal";
const CLASS_EXIT_BUTTON = "exit-button";
const CLASS_CARD_SUBMIT = "card-submit";
const CLASS_DESC_TEXT = "desc-text";
const CLASS_DIVIDER = "divider";
const CLASS_DEL_lIST = "del-list";
const CLASS_DEL_CARD = "del-card";

const DEFAULT_LIST_NAME = "SOMETHING";
const DEFAULT_CARD_TEXT = "SOMETHING TO DO";
const DEFAULT_DESC_TEXT = "DESCRIPTION HERE";

let trolloList = [];
let moveWrapper = false;
let wrapperX;
function cardDragOver(event) {
  event.preventDefault();
  moveWrapper = false;
}

function cardDropped(event) {
  event.preventDefault();
  const draggedBubbleIdx = event.dataTransfer.getData("bubbleIdx");
  const draggedSelfIdx = event.dataTransfer.getData("selfIdx");
  const cardText = trolloList[draggedBubbleIdx].cardList[draggedSelfIdx];
  const descText = trolloList[draggedBubbleIdx].descList[draggedSelfIdx];

  trolloList[draggedBubbleIdx].cardList.splice(draggedSelfIdx, 1);
  trolloList[draggedBubbleIdx].descList.splice(draggedSelfIdx, 1);

  if (Array.from(this.classList).indexOf("bubble-title") != -1) {
    const bubbleIdx = Array.from(row.children).indexOf(this.parentNode);
    trolloList[bubbleIdx].cardList.splice(0, 0, cardText);
    trolloList[bubbleIdx].descList.splice(0, 0, descText);
  } else {
    const bubbleIdx = Array.from(row.children).indexOf(
      this.parentNode.parentNode
    );
    const selfIdx = Array.from(this.parentNode.children).indexOf(this);
    if (bubbleIdx == draggedBubbleIdx) {
      trolloList[bubbleIdx].cardList.splice(selfIdx, 0, cardText);
      trolloList[bubbleIdx].descList.splice(selfIdx, 0, descText);
    } else {
      trolloList[bubbleIdx].cardList.splice(selfIdx + 1, 0, cardText);
      trolloList[bubbleIdx].descList.splice(selfIdx + 1, 0, descText);
    }
  }
  localStorage.setItem("trolloList", JSON.stringify(trolloList));
  drawBubbles();
  moveWrapper = false;
}

function cardDragStart(event) {
  const bubbleIdx = Array.from(row.children).indexOf(
    this.parentNode.parentNode
  );
  const selfIdx = Array.from(this.parentNode.children).indexOf(this);
  event.dataTransfer.dropEffect = "move";
  event.dataTransfer.setData("bubbleIdx", bubbleIdx);
  event.dataTransfer.setData("selfIdx", selfIdx);
  moveWrapper = false;
}

function delCardHandler(delCardBtn, bubbleIdx, selfIdx) {
  delCardBtn.addEventListener("click", function() {
    trolloList[bubbleIdx].cardList.splice(selfIdx, 1);
    trolloList[bubbleIdx].descList.splice(selfIdx, 1);
    localStorage.setItem("trolloList", JSON.stringify(trolloList));
    body.removeChild(body.lastChild);
    drawBubbles();
  });
}

function deleteButtonClicked(delButton, bubbleIdx) {
  delButton.addEventListener("click", function() {
    trolloList.splice(bubbleIdx, 1);
    localStorage.setItem("trolloList", JSON.stringify(trolloList));
    drawBubbles();
  });
}

function exitButtonClicked() {
  localStorage.setItem("trolloList", JSON.stringify(trolloList));
  drawBubbles();
  body.removeChild(body.lastChild);
}

function pToCardText(p, bubbleIdx, selfIdx, className) {
  p.addEventListener("click", function() {
    const textarea = document.createElement("textarea");
    textarea.classList.add(className);
    textarea.value = this.textContent;
    textarea.addEventListener("input", textareaHeightHandle);
    cardTextBlur(textarea, bubbleIdx, selfIdx, className);
    this.parentNode.replaceChild(textarea, p);
    textarea.focus();
  });
}

function cardTextBlur(textarea, bubbleIdx, selfIdx, className) {
  textarea.addEventListener("blur", function() {
    p = document.createElement("p");
    p.classList.add(className);
    p.textContent = this.value;
    if (className === CLASS_CARD_TEXT) {
      trolloList[bubbleIdx].cardList[selfIdx] = this.value;
      pToCardText(p, bubbleIdx, selfIdx, CLASS_CARD_TEXT);
    } else {
      trolloList[bubbleIdx].descList[selfIdx] = this.value;
      pToCardText(p, bubbleIdx, selfIdx, CLASS_DESC_TEXT);
    }
    this.parentNode.replaceChild(p, this);
  });
}

function textareaHeightHandle() {
  this.style.height = "";
  this.style.height = this.scrollHeight + "px";
}

function cardClicked(event) {
  const bubbleIdx = Array.from(row.children).indexOf(
    this.parentNode.parentNode
  );

  const selfIdx = Array.from(this.parentNode.children).indexOf(this);

  const modalFrame = document.createElement("div");
  modalFrame.classList.add(CLASS_MODAL_FRAME);

  const modal = document.createElement("div");
  modal.classList.add(CLASS_MODAL);

  const title = document.createElement("p");
  title.textContent = "Card Title";

  const cardText = document.createElement("p");
  cardText.textContent = this.querySelector(".card-text").textContent;
  cardText.addEventListener("input", textareaHeightHandle);
  cardText.classList.add(CLASS_CARD_TEXT);
  pToCardText(cardText, bubbleIdx, selfIdx, CLASS_CARD_TEXT);

  const small = document.createElement("small");
  small.textContent = "in list " + trolloList[bubbleIdx].name;

  const divider = document.createElement("div");
  divider.classList.add(CLASS_DIVIDER);

  const desc = document.createElement("p");
  desc.textContent = "Description";

  const desText = document.createElement("p");
  desText.classList.add(CLASS_DESC_TEXT);
  desText.textContent = trolloList[bubbleIdx].descList[selfIdx];
  desText.addEventListener("input", textareaHeightHandle);
  pToCardText(desText, bubbleIdx, selfIdx, CLASS_DESC_TEXT);

  const exitButton = document.createElement("button");
  exitButton.textContent = "X";
  exitButton.classList.add(CLASS_EXIT_BUTTON);
  exitButton.addEventListener("click", exitButtonClicked);

  const delCardBtn = document.createElement("button");
  delCardBtn.textContent = "Delete Card";
  delCardBtn.classList.add(CLASS_DEL_CARD);
  delCardHandler(delCardBtn, bubbleIdx, selfIdx);

  modal.appendChild(exitButton);
  modal.appendChild(title);
  modal.appendChild(cardText);
  modal.appendChild(small);
  modal.appendChild(divider);
  modal.appendChild(desc);
  modal.appendChild(desText);
  modal.appendChild(delCardBtn);

  modalFrame.appendChild(modal);
  body.appendChild(modalFrame);
}

function bubbleTitleBlur(event) {
  const bubbleIdx = Array.from(row.children).indexOf(
    this.parentNode.parentNode
  );
  trolloList[bubbleIdx].name = this.value;
  localStorage.setItem("trolloList", JSON.stringify(trolloList));
}

function dropBtnClick(event) {
  this.parentNode.querySelector(".drops").classList.toggle(CLASS_DISPLAY_NONE);
}

function dropBtnBlur(event) {
  this.classList.add(CLASS_DISPLAY_NONE);
}

function cardSubmitClicked(event) {
  const bubbleIdx = Array.from(row.children).indexOf(
    this.parentNode.parentNode.parentNode
  );

  const selfIdx = Array.from(this.parentNode.parentNode.children).indexOf(
    this.parentNode
  );

  trolloList[bubbleIdx].cardList[selfIdx] = this.parentNode.querySelector(
    ".card-text"
  ).value;

  localStorage.setItem("trolloList", JSON.stringify(trolloList));
  this.parentNode.addEventListener("click", cardClicked);
  this.parentNode.innerHTML = `<p class="card-text">${
    this.parentNode.querySelector(".card-text").value
  }</p>`;
}

//  @@@@@@@@@@@@@@ REFACTORING NEED @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
function addCardClick(event) {
  const bubbleIdx = Array.from(row.children).indexOf(
    this.parentNode.parentNode.parentNode
  );

  this.parentNode.classList.add(CLASS_DISPLAY_NONE);
  const card = document.createElement("div");
  card.classList.add(CLASS_CARD);
  card.setAttribute("draggable", "true");
  card.addEventListener("dragstart", cardDragStart);
  card.addEventListener("dragover", cardDragOver);
  card.addEventListener("drop", cardDropped);

  const cardText = document.createElement("textarea");
  cardText.classList.add(CLASS_CARD_TEXT);
  cardText.textContent = DEFAULT_CARD_TEXT;
  cardText.addEventListener("input", textareaHeightHandle);
  cardText.addEventListener("blur", cardSubmitClicked);
  cardText.addEventListener("mousemove", preventMoveWrapper);

  const cardSubmit = document.createElement("button");
  cardSubmit.classList.add(CLASS_CARD_SUBMIT);
  cardSubmit.addEventListener("click", cardSubmitClicked);
  cardSubmit.textContent = "save";

  card.appendChild(cardText);
  card.appendChild(cardSubmit);

  this.parentNode.parentNode.parentNode
    .querySelector(".bubble-content")
    .appendChild(card);
  cardText.focus();
  trolloList[bubbleIdx].cardList.push(DEFAULT_CARD_TEXT);
  trolloList[bubbleIdx].descList.push(DEFAULT_DESC_TEXT);
  localStorage.setItem("trolloList", JSON.stringify(trolloList));
}
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

function addListBtnClick(event) {
  const obj = {
    name: DEFAULT_LIST_NAME,
    cardList: [],
    descList: []
  };
  trolloList.push(obj);
  localStorage.setItem("trolloList", JSON.stringify(trolloList));
  drawBubbles();
  row.lastChild.querySelector(".bubble-title input").focus();
}

// @@@@@@@@@@@@@@@@@@ REFACTORING NEED BELOW THIS COMMENT @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

function drawBubbles() {
  row.innerHTML = "";
  trolloList = JSON.parse(localStorage.getItem("trolloList"));
  trolloList.forEach(element => {
    const bubble = document.createElement("div");
    bubble.classList.add(CLASS_BUBBLE);
    bubble.innerHTML = ` <div class="bubble-title" droppable="true">
    <input type="text" name="" id="" value=${element.name} />
    <button class="drop-btn">=</button>
    <div class="drops display-none">
      <button class="add-card" href="">Add Card</button>
      <button class="del-list" href="">Del List</button>
    </div>
  </div><div class="bubble-content"></div>`;
    row.appendChild(bubble);
    bubbleIdx = Array.from(row.children).indexOf(bubble);
    bubble.querySelector(".drop-btn").addEventListener("click", dropBtnClick);
    bubble.querySelector(".bubble-title").addEventListener("drop", cardDropped);
    bubble
      .querySelector(".bubble-title")
      .addEventListener("mousemove", preventMoveWrapper);
    bubble
      .querySelector(".bubble-title")
      .addEventListener("dragover", cardDragOver);
    bubble.querySelector(".drops").addEventListener("mouseleave", dropBtnBlur);
    bubble.querySelector(".add-card").addEventListener("click", addCardClick);
    bubble.querySelector("input").addEventListener("blur", bubbleTitleBlur);
    deleteButtonClicked(bubble.querySelector(".del-list"), bubbleIdx);
    element.cardList.forEach(element2 => {
      card = document.createElement("div");
      card.setAttribute("draggable", "true");
      card.setAttribute("droppable", "true");
      card.classList.add(CLASS_CARD);
      card.innerHTML = `<p class="card-text" name="" id="" >${element2}</p>`;
      card.addEventListener("dragstart", cardDragStart);
      card.addEventListener("dragover", cardDragOver);
      card.addEventListener("drop", cardDropped);
      card.addEventListener("dragend", preventMoveWrapper);
      card.addEventListener("mousemove", preventMoveWrapper);
      card.addEventListener("mouseenter", preventMoveWrapper);

      bubble.querySelector(".bubble-content").appendChild(card);
      card.addEventListener("click", cardClicked);
    });
  });
}
// @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
function preventMoveWrapper(event) {
  moveWrapper = false;
}
function wrapperMouseDown(event) {
  moveWrapper = true;
  wrapperX = event.clientX;
}
function wrapperMouseMove(event) {
  if (moveWrapper === true) {
    aa = wrapperX - event.clientX;
    wrapperX = event.clientX;
    wrapper.scrollLeft = wrapper.scrollLeft + aa;
  }
}
function wrapperMouseUp(event) {
  moveWrapper = false;
}
function wrapperMouseLeave() {
  moveWrapper = false;
}
function init() {
  addListBtn.addEventListener("click", addListBtnClick);

  wrapper.addEventListener("mousedown", wrapperMouseDown);
  wrapper.addEventListener("mousemove", wrapperMouseMove);
  wrapper.addEventListener("mouseup", wrapperMouseUp);
  wrapper.addEventListener("mouseleave", wrapperMouseLeave);
  if (localStorage.getItem("trolloList")) {
    drawBubbles();
  }
}

init();
