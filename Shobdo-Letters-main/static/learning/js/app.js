const buttons = document.querySelectorAll(".js-speak");

function speak(text, lang) {
    if (!("speechSynthesis" in window)) {
        window.alert("Audio playback is not supported in this browser.");
        return;
    }

    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = lang || "en-US";
    utterance.rate = 0.85;
    utterance.pitch = 1.05;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(utterance);
}

buttons.forEach((button) => {
    button.addEventListener("click", () => {
        speak(button.dataset.text, button.dataset.lang);
    });
});
