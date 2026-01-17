const form = document.getElementById("emailForm");
const resultDiv = document.getElementById("result-container");
const classificationSpan = document.getElementById("classification");
const responseBox = document.getElementById("suggestedResponse");
const loader = document.querySelector(".loader");
const submitBtn = document.getElementById("submitBtn");
const bulb = document.querySelector(".bulb");
const fileInput = document.getElementById("fileInput");
const fileName = document.getElementById("fileName");
const fileInfo = document.getElementById("fileInfo");
const removeFileBtn = document.getElementById("removeFile");
const errorBubble = document.getElementById("errorBubble");
const bubbleText = errorBubble.querySelector(".bubble-text");

let bulbTimeout;

fileInput.addEventListener("change", () => {
  fileName.textContent = fileInput.files.length
    ? fileInput.files[0].name
    : "Nenhum arquivo selecionado";
});

fileInput.addEventListener("change", () => {
  if (fileInput.files.length > 0) {
    fileName.textContent = fileInput.files[0].name;
    fileInfo.classList.remove("hidden");
  }
});

removeFileBtn.addEventListener("click", () => {
  fileInput.value = "";
  fileInfo.classList.add("hidden");
  fileName.textContent = "";
});

function showError(message) {
  bubbleText.textContent = message;
  errorBubble.classList.add("active");
  bubbleText.classList.add("active");
}

function hideError() {
  bubbleText.classList.remove("active");
  errorBubble.classList.remove("active");
  bubbleText.textContent = "";
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const rawText = document.getElementById("emailText").innerText;
  const text = rawText.trim();

  const fileInput = document.getElementById("fileInput").files[0];

  if (!text && !fileInput) {
    showError("Informe um texto ou envie um arquivo.");
    return;
  }

  if (text && fileInput) {
    showError("Escolhe apenas uma opção.");
    return;
  }

  const formData = new FormData();
  if (text) formData.append("text", text);
  if (fileInput) formData.append("file", fileInput);

  hideError();
  bulb.classList.add("hidden");
  loader.classList.add("loading");
  submitBtn.disabled = true;
  submitBtn.textContent = "Processando...";
  resultDiv.classList.add("hidden");

  bulbTimeout = setTimeout(() => {
    bulb.classList.remove("hidden");
  }, 3100);

  try {
    const response = await fetch("/process-email", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error("Erro ao processar email");
    }

    const data = await response.json();

    classificationSpan.textContent = data.classification;
    responseBox.textContent = data.suggested_response;

    resultDiv.classList.remove("hidden");
  } catch (error) {
    showError("Erro ao comunicar com o backend.");
    console.error(error);
  } finally {
    clearTimeout(bulbTimeout);
    bulb.classList.add("hidden");
    loader.classList.remove("loading");
    submitBtn.disabled = false;
    submitBtn.textContent = "Processar Email";
  }
});
