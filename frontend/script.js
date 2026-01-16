const form = document.getElementById("emailForm");
const resultDiv = document.getElementById("result-container");
const classificationSpan = document.getElementById("classification");
const responseBox = document.getElementById("suggestedResponse");

form.addEventListener("submit", async (e) => {
    e.preventDefault();


    const text = document.getElementById("emailText").value;
    const fileInput = document.getElementById("fileInput").files[0];

    if (!text && !fileInput) {
        alert("Informe um texto ou faça upload de um arquivo.");
        return;
    }

    if (text && fileInput) {
        alert("Por favor, forneça apenas UMA opção.");
        return;
    }

    const formData = new FormData();
    if (text) formData.append("text", text);
    if (fileInput) formData.append("file", fileInput);

    try {
        const response = await fetch("http://localhost:8000/process-email", {
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
     alert("Erro ao comunicar com o backend.");
        console.error(error);
    }
    });