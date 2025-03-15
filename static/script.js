let mediaRecorder;
let audioChunks = [];
let isRecording = false;
let initial_value="Your transcribed text will appear here.";
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;

const recognition = new SpeechRecognition();
recognition.continuous = false; // Stops listening after speech is detected
recognition.interimResults = false; // Only return final result
recognition.lang = "en-US"; // Set language

// Get HTML elements
const startButton = document.getElementById("start-recording");
const stopButton = document.getElementById("stop-recording");
const transcription = document.getElementById("transcription");
const voiceTextInput = document.getElementById("voiceText");
const voiceForm = document.getElementById("voiceForm");
const resultSection = document.getElementById("result");
const factText = document.getElementById("fact-text");
const searchResult = document.getElementById("search-result");
let speechToText="";
transcription.innerText = "No voice input yet";
factText.innerText = "Loading interesting tax facts... 🤓";
// Fun Tax Law Facts
const taxFacts = [
    "The Income Tax Act of India was passed in 1961 and governs all direct taxes.",
    "GST (Goods and Services Tax) was introduced in India on July 1, 2017.",
    "Under Section 80C, you can claim up to ₹1.5 lakh as tax deductions for investments.",
    "Agricultural income in India is fully exempt from tax!",
    "Did you know? The highest income tax slab in India is 30% for earnings above ₹10 lakh.",
    "The first-ever income tax was introduced in India in 1860 by Sir James Wilson.",
    "The penalty for not filing your Income Tax Return (ITR) on time can be up to ₹10,000.",
    "House rent allowance (HRA) can help you save on taxes if you live in a rented house."
];
document.addEventListener("DOMContentLoaded", function () {
    setInterval(changeFact, 5000); // Restart fact-changing on page load
});
// Function to change facts every 5 seconds
function changeFact() {
    const randomFact = taxFacts[Math.floor(Math.random() * taxFacts.length)];
    factText.innerText = randomFact;
}

function showLoading(message) {
    if (searchResult) {
        searchResult.innerHTML = `<p>⏳ ${message}...</p>`;
    } else {
        console.error("searchResult element not found in HTML.");
    }}

// Change fact every 5 seconds
import OpenAI from "openai";
const client = new OpenAI();
const queryForm = document.querySelector("form[action='/process']");
queryForm.addEventListener("submit", async (event) => {
    
    event.preventDefault();
    const formData = new FormData(queryForm);
    const textInput = formData.get("text_input");
    let prompt = `Extract Indian tax law keywords from this query: '${textInput}'. Return as a comma-separated list.`
    const completion = await client.chat.completions.create({
        model: "gpt-4o",
        messages: [{
            role: "user",
            content: prompt,
        }],
    });
    // showLoading("Processing your text input");

    // try {
    //     const response = await fetch("/process", {
    //         method: "POST",
    //         body: formData
    //     });
    //     if (!response.ok) {
    //         throw new Error(`Server error: ${response.status}`);
    //     }
    //     const data = await response.json();
    //     if (data.result) {
    //         searchResult.innerText = data.result;
    //     } else {
    //         searchResult.innerText = "No results found.";
    //     }
    // } catch (error) {
    //     searchResult.innerText = "Error processing text input.";
    //     console.error("Text Input Error:", error);
    // }
    
   
    
    console.log(completion.choices[0].message.content);
});
//setInterval(changeFact, 5000);




// Start recording
startButton.addEventListener("click", async () => {
    try {
        // const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        // mediaRecorder = new MediaRecorder(stream);
        // audioChunks = [];
        // isRecording = true;

        // mediaRecorder.ondataavailable = event => audioChunks.push(event.data);
        // mediaRecorder.start();
        recognition.start();
        startButton.innerText = "🎤 Recording...";
        startButton.style.backgroundColor = "#e74c3c"; // Red
        stopButton.disabled = false;
        startButton.disabled = true;
    } catch (error) {
        alert("Error accessing microphone. Please check your permissions.");
    }
});

// Stop recording & send to backend
stopButton.addEventListener("click", () => {
    recognition.stop();

    // if (!isRecording) return;
    // mediaRecorder.stop();
    // isRecording = false;

    // stopButton.innerText = "⏳ Processing...";
    // stopButton.style.backgroundColor = "#cccccc"; // Grey
    // startButton.disabled = false;

    // mediaRecorder.onstop = async () => {
    //     if (searchResult) {
    //         showLoading("Processing your voice input");
    //     }
    //     const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });
    //     const formData = new FormData();
    //     console.log("audioBlob:", audioBlob);
    //     formData.append("audio", audioBlob, "recording.webm");

    //     try {
    //         const response = await fetch("/transcribe", {
    //             method: "POST",
    //             body: formData
    //         });
    //         if (!response.ok) {
    //             throw new Error(`Server error: ${response.status}`);
    //         }
    //         const data = await response.json();
    //         if (data.error) {
    //              throw new Error(data.error);
    //         }
    //         console.log("Transcription data:", data);

            // Reset button UI
            startButton.innerText = "🎤 Start Recording";
            startButton.style.backgroundColor = "#007bff";
          //  stopButton.disabled = true;
            stopButton.innerText = "⏹️ Stop & Submit";
            stopButton.style.backgroundColor = "#28a745";

        //     if (data.transcription) {
        //         transcription.innerText = data.transcription;
        //         voiceTextInput.value = data.transcription;

        //         // Show in search result section
        //         if (searchResult) {
        //             searchResult.innerText = `Searching for relevant tax laws related to: ${data.transcription}`;
        //         }
        //         voiceForm.submit();
        //     }else{
        //         transcription.innerText = "Transcription failed.";
        //     }
        // } catch (error) {
        //     transcription.innerText = "Error processing audio.";
        //     console.error("Transcription Error:", error);

        // }
    });
    recognition.onresult = (event) => {
        speechToText = event.results[0][0].transcript; // Get first result
        console.log("Transcribed Text: ", speechToText);
        console.log("hii");
        // Update UI
       
        // Show in search result section
        if (searchResult) {
            searchResult.innerText = `Searching for relevant tax laws related to: ${speechToText}`;
            transcription.innerText = speechToText;

        }
        voiceTextInput.value = speechToText;
        initial_value=speechToText;
        startButton.innerText = "🎤 Start Recording";
        startButton.style.backgroundColor = "#007bff";
        startButton.disabled = false;
        stopButton.disabled = true;
        fetch("/voice_process", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded"
            },
            body: `voiceText=${encodeURIComponent(speechToText)}`
        })
        .then(response => response.json()) // Expecting JSON response
        .then(data => {
            if (data.filtered_keywords) {
                console.log("Keywords:", data.filtered_keywords);
                let keywordbox = document.querySelector(".keyword-box");
                if(keywordbox){
                    console.log("hello");
                    keywordbox.innerHTML =  `<p><strong>Relevant Tax Keywords:</strong> ${data.filtered_keywords.join(", ")}</p>`;
            }}
            if(data.transcribed_text) console.log("arumai da");
            if (data.result){
                console.log("Result:", data.result);
                 searchResult.innerText = data.result;
            }


        })  
        // .then(data => {
        //     document.body.innerHTML = data; // Update page dynamically
        // })
        .catch(error => {
            console.error("Error processing voice input:", error);
        });
        // Auto-submit form
       
        

    };
    recognition.onerror = (event) => {
        console.error("Speech Recognition Error: ", event.error);
       // transcription.innerText = "Error recognizing speech. Please try again.";
        startButton.innerText = "🎤 Start Recording";
        startButton.style.backgroundColor = "#007bff";
        startButton.disabled = false;
        stopButton.disabled = true;
    };
    recognition.onend = () => {
        startButton.innerText = "🎤 Start Recording";
        startButton.style.backgroundColor = "#007bff";
        startButton.disabled = false;
        stopButton.disabled = true;
       // speechToText = " "
      // setInterval(changeFact, 5000);

    };

