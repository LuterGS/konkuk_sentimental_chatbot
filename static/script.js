const chatList = document.querySelector(".chatting-list");
const chatInput = document.querySelector(".chatting-input");
const sendBtn = document.querySelector(".send-btn");
const modal = document.querySelector(".modal");
const closeBtn = document.querySelector("#close-btn");
const info = document.querySelector(".info");

chatInput.focus();

closeBtn.addEventListener("click", () => {
  modal.style.display = "none";
  chatInput.focus();
});

const checkKorean = (string) => {
  const korean = /[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/;
  return korean.test(string);
};

function checkValue(userinput) {
  if (!userinput) {
    info.textContent = "문장을 입력해주세요.";
    modal.style.display = "block";
    chatInput.blur();
    return false;
  }
  if (!checkKorean(userinput)) {
    info.textContent = "한국어를 입력해주세요.";
    modal.style.display = "block";
    chatInput.blur();
    return false;
  }
  return true;
}

function checkLength() {
  if (chatInput.value.length > 200) {
    info.textContent = "200자 이내만 입력해주세요.";
    modal.style.display = "block";
    chatInput.blur();
  }
}

function createUserLi(userInput) {
  const li = document.createElement("li");
  li.classList.add("sent");
  const dom = `<img src="/static/img/user.png" alt="">
      <p class="msg">${userInput}</p>`;
  li.innerHTML = dom;
  chatList.appendChild(li);
}

function createChatbotLi(chatbotOutput) {
  const li = document.createElement("li");
  li.classList.add("received");
  const dom = `<img src="/static/img/chatbot.png" alt="">
      <p class="msg">${chatbotOutput}</p></p>`;
  li.innerHTML = dom;
  chatList.appendChild(li);
}

async function processing() {
  const msg = chatInput.value;
  if (!checkValue(msg)) {
    return;
  }
  createUserLi(msg);

  const chatbotResponse = await fetch("/conversation", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ userInput: msg }),
  });
  const retrVal = await chatbotResponse.json();
  createChatbotLi(retrVal["response"]);

  chatInput.value = "";
  chatList.lastElementChild.scrollIntoView();
}

sendBtn.addEventListener("click", () => {
  processing();
});

function pressEnter() {
  if (this.event.keyCode === 13) {
    processing();
  }
}