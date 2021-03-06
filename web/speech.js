var recognizing = false

if (window.hasOwnProperty('webkitSpeechRecognition')) {

    var recognition = new webkitSpeechRecognition();

    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = "cmn-Hant-TW";

    recognition.onstart = function() {
        recognizing = true;
        document.getElementById("ximage").src="icons/loading.gif";
    };

    recognition.onend = function() {
        recognizing = false;
        document.getElementById("ximage").src="icons/mic-icon.png";
    };

    recognition.onresult = function(event) {
        document.getElementById('xinput').value = event.results[0][0].transcript;
        recognition.stop();
        document.getElementById('xform').submit();
    };

    recognition.onerror = function(event) {
        console.log(event.error);
        recognition.stop();
    };

}

function loadImage() {
    if (!window.hasOwnProperty('webkitSpeechRecognition')) {
        document.getElementById("ximage").src="";
    }
}

function startDictation() {

    if (window.hasOwnProperty('webkitSpeechRecognition')) {

        if (recognizing == true) {
            recognizing = false;
            document.getElementById("ximage").src="icons/mic-icon.png";
            recognition.stop();
        }

        else {
            recognition.start();
        }

    }
}

