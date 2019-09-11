const addListBtn = document.querySelector(".add-list-btn");
const row = document.querySelector(".row1");

const ELEMENT_DIV = "div";
const ELEMENT_INPUT = "input";
const ELEMENT_BTN = "button";

const CLASS_BUBBLE = "bubble";
const CLASS_BUBBLE_TITLE = "bubble-title";
const CLASS_DROPS = "drops";
const CLASS_DIPLAY_NONE = "display-none";
const CLASS_DROP_BTN = "drop-btn";
const CLASS_ADD_CARD = "add-card";
const CLASS_DEL_LIST = "del-list";
const CLASS_BUBBLE_CONTENT = "bubble-content";

const ACTION_ADDLIST = "addList";

const ATTR_DROPPABLE = "droppable";
const ATTR_TYPE = "type";

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
      console.log(data);
      return data;
    }
  });
  console.log(result);
  return result.responseText;
}

function drawNewBubble() {
  const bubble = document.createElement(ELEMENT_DIV);
  bubble.classList.add(CLASS_BUBBLE);

  const bubbleTitle = document.createElement(ELEMENT_DIV);
  bubbleTitle.classList.add(CLASS_BUBBLE_TITLE);
  bubbleTitle.setAttribute(ATTR_DROPPABLE, "true");

  const bubbleTitleInput = document.createElement(ELEMENT_INPUT);
  bubbleTitleInput.setAttribute(ATTR_TYPE, "text");
  bubbleTitleInput.value = "something";

  const dropBtn = document.createElement(ELEMENT_BTN);
  dropBtn.classList.add(CLASS_DROP_BTN);
  dropBtn.innerText = "=";

  const drops = document.createElement(ELEMENT_DIV);
  drops.classList.add(CLASS_DROPS);
  drops.classList.add(CLASS_DIPLAY_NONE);

  const addCardBtn = document.createElement(ELEMENT_BTN);
  addCardBtn.classList.add(CLASS_ADD_CARD);
  addCardBtn.innerText = "Add Card";

  const delListBtn = document.createElement(ELEMENT_BTN);
  delListBtn.classList.add(CLASS_DEL_LIST);
  delListBtn.innerText = " Del List";

  const bubbleContent = document.createElement(ELEMENT_DIV);
  bubbleContent.classList.add(CLASS_BUBBLE_CONTENT);

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
  console.log(bubbleId);
  drawNewBubble();
}

function init() {
  addListBtn.addEventListener("click", addListBtnClicked);
}

init();
