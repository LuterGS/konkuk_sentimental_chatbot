const checkKorean = (string) => {
  const korean = /[ㄱ-ㅎ|ㅏ-ㅣ|가-힣]/;
  return korean.test(string);
};

const inputText = document.getElementById("user-input-text");
const inputBtn = document.getElementById("user-input-btn");
const ulTag = document.querySelector("ul");

const outputText = document.getElementById("chatbot-output");

inputBtn.addEventListener("click", async () => {
  const userInputValue = inputText.value;
  if (!userInputValue) {
    alert("문장을 입력해주세요.");
    return;
  }

  if (!checkKorean(userInputValue)) {
    alert("한국어를 입력해주세요.");
    return;
  }

  const chatbotResponse = await fetch("/conversation", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ userInput: userInputValue }),
  });
  const retrVal = await chatbotResponse.json();

  outputText.innerText = retrVal["response"];
});
