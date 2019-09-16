const addListBtn = document.querySelector(".add-list-btn");
const row = document.querySelector(".row1");

const ELEMENT_DIV = "div";
const ELEMENT_INPUT = "input";
const ELEMENT_BTN = "button";
const ELEMENT_TEXT_AREA = "textarea";
const ELEMENT_P = "p";
const ELEMENT_SMALL = "small";

const CLASS_BUBBLE = "bubble";
const CLASS_BUBBLE_TITLE = "bubble-title";
const CLASS_DROPS = "drops";
const CLASS_DISPLAY_NONE = "display-none";
const CLASS_DROP_BTN = "drop-btn";
const CLASS_ADD_CARD = "add-card";
const CLASS_DEL_LIST = "del-list";
const CLASS_BUBBLE_CONTENT = "bubble-content";
const CLASS_CARD = "card";
const CLASS_CARD_TEXT = "card-text";
const CLASS_CARD_SUBMIT = "card-submit";
const CLASS_MODAL_FRAME = "modal-frame";
const CLASS_MODAL = "modal";
const CLASS_DIVIDER = "divider";
const CLASS_EXIT_BUTTON = "exit-button";
const CLASS_DESC_TEXT = "desc-text";
const CLASS_DEL_CARD = "del-card";

const DEFAULT_CARD_TEXT = "something to do";

const ACTION_ADDLIST = "addList";

const ATTR_DROPPABLE = "droppable";
const ATTR_TYPE = "type";
const ATTR_LIST_ID = "listId";
const ATTR_CARD_ID = "card-id";

function delCardBtnClicked(event) {
  cardId = this.getAttribute(ATTR_CARD_ID);
  console.log(cardId);
  $.ajax({
    url: "/troloTest",
    type: "DELETE",
    data: {
      action: "cardDelete",
      cardId
    },
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
    }
  });
  card = row.querySelector(`.card[card-id='${cardId}']`);
  card.parentNode.removeChild(card);
  row.removeChild(row.lastChild);
}

function exitButtonClicked(exitButton, cardId) {
  exitButton.addEventListener("click", function() {
    card = row.querySelector(`.card[card-id='${cardId}'] .card-text`);
    card.innerText = this.parentNode.querySelector(".card-text").innerText;
    row.removeChild(row.lastChild);
  });
}
function textareaHeightHandle() {
  this.style.height = "";
  this.style.height = this.scrollHeight + "px";
}

function textareaBlured(textarea, className) {
  textarea.addEventListener("blur", function() {
    let action;
    const data = this.value;
    if (className == CLASS_CARD_TEXT) {
      action = "cardTitleUpdate";
    } else if (className == CLASS_DESC_TEXT) {
      action = "cardDescUpdate";
    }
    $.ajax({
      url: "/troloTest",
      type: "PUT",
      data: {
        action,
        data,
        cardId: this.getAttribute(ATTR_CARD_ID)
      },
      beforeSend: function(xhr) {
        xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
      }
    });

    const p = document.createElement(ELEMENT_P);
    p.classList.add(CLASS_CARD_TEXT);
    p.innerText = this.value;
    p.setAttribute(ATTR_CARD_ID, this.getAttribute(ATTR_CARD_ID));
    pToTextarea(p, className);
    this.parentNode.replaceChild(p, this);
  });
}

function pToTextarea(p, className) {
  p.addEventListener("click", function() {
    const text = this.innerText;
    const textarea = document.createElement(ELEMENT_TEXT_AREA);
    textarea.addEventListener("input", textareaHeightHandle);
    textareaBlured(textarea, className);
    textarea.value = text;
    textarea.classList.add(className);
    textarea.setAttribute(ATTR_CARD_ID, this.getAttribute(ATTR_CARD_ID));
    this.parentNode.replaceChild(textarea, this);
  });
}

function drawNewModal(titleText, descriptionText, listTitle, cardId) {
  const modalFrame = document.createElement(ELEMENT_DIV);
  modalFrame.classList.add(CLASS_MODAL_FRAME);

  const modal = document.createElement(ELEMENT_DIV);
  modal.classList.add(CLASS_MODAL);

  const title = document.createElement(ELEMENT_P);
  title.textContent = "Card Title";

  const cardTitle = document.createElement(ELEMENT_P);
  cardTitle.textContent = titleText;
  cardTitle.classList.add(CLASS_CARD_TEXT);
  cardTitle.setAttribute(ATTR_CARD_ID, cardId);
  pToTextarea(cardTitle, CLASS_CARD_TEXT);

  const small = document.createElement(ELEMENT_SMALL);
  small.textContent = "in list " + listTitle;

  const divider = document.createElement(ELEMENT_DIV);
  divider.classList.add(CLASS_DIVIDER);

  const desc = document.createElement(ELEMENT_P);
  desc.textContent = "Description";

  const desText = document.createElement(ELEMENT_P);
  desText.classList.add(CLASS_DESC_TEXT);
  desText.textContent = descriptionText;
  desText.setAttribute(ATTR_CARD_ID, cardId);
  pToTextarea(desText, CLASS_DESC_TEXT);

  const exitButton = document.createElement(ELEMENT_BTN);
  exitButton.textContent = "X";
  exitButton.classList.add(CLASS_EXIT_BUTTON);
  exitButtonClicked(exitButton, cardId);

  const delCardBtn = document.createElement(ELEMENT_BTN);
  delCardBtn.textContent = "Delete Card";
  delCardBtn.classList.add(CLASS_DEL_CARD);
  delCardBtn.setAttribute(ATTR_CARD_ID, cardId);
  delCardBtn.addEventListener("click", delCardBtnClicked);

  modal.appendChild(exitButton);
  modal.appendChild(title);
  modal.appendChild(cardTitle);
  modal.appendChild(small);
  modal.appendChild(divider);
  modal.appendChild(desc);
  modal.appendChild(desText);
  modal.appendChild(delCardBtn);

  modalFrame.appendChild(modal);
  row.appendChild(modalFrame);
}

function cardClicked(event) {
  cardId = this.getAttribute(ATTR_CARD_ID);
  console.log(cardId);
  $.ajax({
    url: "/troloTest",
    type: "GET",
    data: {
      action: "getCard",
      cardId,
      csrfmiddlewaretoken: CSRF_TOKEN
    }
  }).done(function(card) {
    card = JSON.parse(card);
    drawNewModal(card.cardTitle, card.cardDescription, card.listTitle, cardId);
  });
}

function delListBtnClicked(event) {
  list = document.getElementById(this.getAttribute(ATTR_LIST_ID));
  $.ajax({
    url: "/troloTest",
    type: "DELETE",
    data: {
      action: "listDelete",
      listId: this.getAttribute(ATTR_LIST_ID)
    },
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
    }
  });
  row.removeChild(list);
}

function listTitleBlured(event) {
  if (this.value === undefined) {
    console.log("Dude");
  }
  $.ajax({
    url: "/troloTest",
    type: "PUT",
    async: false,
    data: {
      action: "listTitleUpdate",
      listId: this.getAttribute(ATTR_LIST_ID),
      listTitle: this.value
    },
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
    }
  });
}

function cardTextBlured(event) {
  const card = this.parentNode;
  const p = document.createElement(ELEMENT_P);
  p.innerText = this.value;
  p.classList.add(CLASS_CARD_TEXT);
  card.innerHTML = "";
  card.appendChild(p);
  $.ajax({
    url: "/troloTest",
    type: "PUT",
    async: false,
    data: {
      action: "cardTitleUpdate",
      cardId: card.getAttribute(ATTR_CARD_ID),
      data: p.innerText
    },
    beforeSend: function(xhr) {
      xhr.setRequestHeader("X-CSRFToken", CSRF_TOKEN);
    }
  });
}

function addCardClicked(event) {
  const listId = this.getAttribute(ATTR_LIST_ID);
  const result = $.ajax({
    url: "/troloTest",
    type: "post",
    async: false,
    data: {
      action: "addCard",
      listId,
      csrfmiddlewaretoken: CSRF_TOKEN
    },
    success: function(data) {
      return data;
    }
  });
  this.parentNode.classList.add(CLASS_DISPLAY_NONE);
  drawNewCard(listId, result.responseText);
}

function dropBtnClicked(event) {
  this.parentNode.querySelector(".drops").classList.toggle(CLASS_DISPLAY_NONE);
}

// ############## REFACORING NEED ################
function sendPostReq(action) {
  const result = $.ajax({
    url: "/troloTest",
    type: "post",
    async: false,
    data: {
      action,
      csrfmiddlewaretoken: CSRF_TOKEN
    },
    success: function(data) {
      return data;
    }
  });
  return result.responseText;
}
// ###############################################
function drawNewCard(listId, cardId) {
  const bubbleContent = row.querySelector(
    `.bubble-content[listId='${listId}']`
  );

  const card = document.createElement(ELEMENT_DIV);
  card.classList.add(CLASS_CARD);
  card.setAttribute(ATTR_CARD_ID, cardId);
  card.addEventListener("click", cardClicked);

  const cardText = document.createElement(ELEMENT_TEXT_AREA);
  cardText.classList.add(CLASS_CARD_TEXT);
  cardText.textContent = DEFAULT_CARD_TEXT;
  cardText.addEventListener("blur", cardTextBlured);

  const cardSubmit = document.createElement(ELEMENT_BTN);
  cardSubmit.classList.add(CLASS_CARD_SUBMIT);
  cardSubmit.textContent = "save";

  card.appendChild(cardText);
  card.appendChild(cardSubmit);

  bubbleContent.appendChild(card);
  cardText.focus();
}

function drawNewBubble(bubbleId) {
  const bubble = document.createElement(ELEMENT_DIV);
  bubble.classList.add(CLASS_BUBBLE);
  bubble.setAttribute("id", bubbleId);

  const bubbleTitle = document.createElement(ELEMENT_DIV);
  bubbleTitle.classList.add(CLASS_BUBBLE_TITLE);
  bubbleTitle.setAttribute(ATTR_DROPPABLE, "true");

  const bubbleTitleInput = document.createElement(ELEMENT_INPUT);
  bubbleTitleInput.setAttribute(ATTR_TYPE, "text");
  bubbleTitleInput.value = "something";
  bubbleTitleInput.addEventListener("blur", listTitleBlured);

  const dropBtn = document.createElement(ELEMENT_BTN);
  dropBtn.classList.add(CLASS_DROP_BTN);
  dropBtn.addEventListener("click", dropBtnClicked);
  dropBtn.innerText = "=";

  const drops = document.createElement(ELEMENT_DIV);
  drops.classList.add(CLASS_DROPS);
  drops.classList.add(CLASS_DISPLAY_NONE);

  const addCardBtn = document.createElement(ELEMENT_BTN);
  addCardBtn.classList.add(CLASS_ADD_CARD);
  addCardBtn.addEventListener("click", addCardClicked);
  addCardBtn.innerText = "Add Card";
  addCardBtn.setAttribute("listId", bubbleId);

  const delListBtn = document.createElement(ELEMENT_BTN);
  delListBtn.classList.add(CLASS_DEL_LIST);
  delListBtn.innerText = "Del List";
  delListBtn.setAttribute("listId", bubbleId);
  delListBtn.addEventListener("click", delListBtnClicked);

  const bubbleContent = document.createElement(ELEMENT_DIV);
  bubbleContent.classList.add(CLASS_BUBBLE_CONTENT);
  bubbleContent.setAttribute("listId", bubbleId);

  drops.appendChild(addCardBtn);
  drops.appendChild(delListBtn);

  bubbleTitle.appendChild(bubbleTitleInput);
  bubbleTitle.appendChild(dropBtn);
  bubbleTitle.appendChild(drops);

  bubble.appendChild(bubbleTitle);
  bubble.appendChild(bubbleContent);

  row.appendChild(bubble);
}

function addListBtnClicked() {
  bubbleId = sendPostReq(ACTION_ADDLIST);
  drawNewBubble(bubbleId);
}

function drawBubbles() {
  const dropBtns = row.querySelectorAll("." + CLASS_DROP_BTN);
  const addCardBtns = row.querySelectorAll("." + CLASS_ADD_CARD);
  const listTitles = row.querySelectorAll(".bubble-title input");
  const delListBtns = row.querySelectorAll("." + CLASS_DEL_LIST);
  const cards = row.querySelectorAll("." + CLASS_CARD);
  dropBtns.forEach(element => {
    element.addEventListener("click", dropBtnClicked);
  });
  addCardBtns.forEach(element => {
    element.addEventListener("click", addCardClicked);
  });
  listTitles.forEach(element => {
    element.addEventListener("blur", listTitleBlured);
  });
  delListBtns.forEach(element => {
    element.addEventListener("click", delListBtnClicked);
  });
  cards.forEach(element => {
    element.addEventListener("click", cardClicked);
  });
}

function init() {
  addListBtn.addEventListener("click", addListBtnClicked);
  drawBubbles();
}

init();
