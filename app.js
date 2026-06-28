console.log("Jarvis Loaded");
//weather
const WEATHER_API_KEY = "483d2cdfae46be11fb49873e7acd931b";

function weather(city) {

    fetch(
        `https://api.openweathermap.org/data/2.5/weather?q=${city}&appid=${WEATHER_API_KEY}`
    )
    .then(response => response.json())
    .then(data => {

        document.getElementById("location").textContent =
            `Location: ${data.name}`;

        document.getElementById("country").textContent =
            `Country: ${data.sys.country}`;

        document.getElementById("weatherT").textContent =
            `Weather: ${data.weather[0].main}`;

        document.getElementById("weatherD").textContent =
            data.weather[0].description;

        document.getElementById("weatherIcon").src =
            `https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png`;

        document.getElementById("oTemp").textContent =
            `Temperature: ${(data.main.temp - 273.15).toFixed(1)}°C`;

        document.getElementById("feelLikeTemp").textContent =
            `Feels Like: ${(data.main.feels_like - 273.15).toFixed(1)}°C`;

        document.getElementById("minT").textContent =
            `Min Temp: ${(data.main.temp_min - 273.15).toFixed(1)}°C`;

        document.getElementById("maxT").textContent =
            `Max Temp: ${(data.main.temp_max - 273.15).toFixed(1)}°C`;
    })
    .catch(error => {
        console.log(error);
    });
}

const startBtn = document.getElementById("start_jarvis_btn");
const stopBtn = document.getElementById("stop_jarvis_btn");

const time = document.getElementById("time");
const battery = document.getElementById("battery");
const internet = document.getElementById("internet");

const setup = document.querySelector(".jarvis_setup");
const submitBtn = document.getElementById("sub_btn");

const smallJarvisBtn = document.getElementById("small_jarvis");
const machine = document.querySelector(".machine");

let isListening = false;


function updateRecognitionUI() {
    if (isListening) {
        startBtn.style.display = "none";
        stopBtn.style.display = "flex";
    } else {
        startBtn.style.display = "flex";
        stopBtn.style.display = "none";
    }
}

updateRecognitionUI();

const savedUser = JSON.parse(
    localStorage.getItem("jarvis_setup")
);

if (savedUser && savedUser.location) {
    weather(savedUser.location);
}

function updateClock() {
    const now = new Date();

    const hrs = String(now.getHours()).padStart(2, "0");
    const mins = String(now.getMinutes()).padStart(2, "0");
    const secs = String(now.getSeconds()).padStart(2, "0");

    time.textContent = `${hrs}:${mins}:${secs}`;
}

updateClock();
setInterval(updateClock, 1000);


function updateInternet() {
    internet.textContent =
        navigator.onLine ? "Online" : "Offline";
}

updateInternet();

window.addEventListener("online", updateInternet);
window.addEventListener("offline", updateInternet);


if (navigator.getBattery) {

    navigator.getBattery().then((batteryManager) => {

        function updateBattery() {

            const level =
                Math.floor(
                    batteryManager.level * 100
                );

            battery.textContent =
                batteryManager.charging
                    ? `${level}% Charging`
                    : `${level}%`;
        }

        updateBattery();

        batteryManager.addEventListener(
            "levelchange",
            updateBattery
        );

        batteryManager.addEventListener(
            "chargingchange",
            updateBattery
        );
    });

} else {
    battery.textContent = "Battery API Unsupported";
}



if (localStorage.getItem("jarvis_setup")) {

    setup.style.display = "none";

} else {

    setup.style.display = "flex";

}

submitBtn.addEventListener("click", saveUserInfo);

function saveUserInfo() {

    const inputs =
        setup.querySelectorAll("input");

    const user = {
        name: inputs[0].value.trim(),
        bio: inputs[1].value.trim(),
        location: inputs[2].value.trim(),
        instagram: inputs[3].value.trim(),
        twitter: inputs[4].value.trim(),
        github: inputs[5].value.trim()
    };

    for (const key in user) {
        if (user[key] === "") {
            alert("Please fill all fields");
            return;
        }
    }

   localStorage.setItem(
    "jarvis_setup",
    JSON.stringify(user)
);

weather(user.location);

setup.style.display = "none";

    setup.style.display = "none";

    speak(
        `Welcome ${user.name}`
    );

    alert("Setup Complete");
}


const SpeechRecognition =
    window.SpeechRecognition ||
    window.webkitSpeechRecognition;

if (SpeechRecognition) {

    const recognition =
        new SpeechRecognition();

   recognition.continuous = true;
recognition.interimResults = false;
recognition.maxAlternatives = 1;
recognition.lang = "en-US";

   recognition.onstart = () => {
    console.log("Listening...");
    isListening = true;
    updateRecognitionUI();
};

   recognition.onend = () => {

    if (isListening) {
        recognition.start();
        return;
    }

    updateRecognitionUI();
};

    recognition.onerror = (event) => {

    console.log("Speech Error:", event.error);

    if (event.error === "no-speech") {
        console.log("No speech detected, restarting...");
        return;
    }
};

    recognition.onresult = (event) => {

        const transcript =
            event.results[
                event.resultIndex
            ][0]
                .transcript
                .toLowerCase();

        console.log(transcript);

        if (
            transcript.includes(
                "hello jarvis"
            )
        ) {
            speak("Hello");
        }

        if (
            transcript.includes(
                "open google"
            )
        ) {
            speak(
                "Opening Google"
            );

            window.open(
                "https://google.com",
                "_blank"
            );
        }

        if (
            transcript.includes(
                "open youtube"
            )
        ) {
            speak(
                "Opening YouTube"
            );

            window.open(
                "https://youtube.com",
                "_blank"
            );
        }

        if (
            transcript.includes(
                "open github"
            )
        ) {
            speak(
                "Opening GitHub"
            );

            window.open(
                "https://github.com",
                "_blank"
            );
        }

        if (
            transcript.includes(
                "search for"
            )
        ) {

            const query =
                transcript
                    .replace(
                        "search for",
                        ""
                    )
                    .trim()
                    .replaceAll(
                        " ",
                        "+"
                    );

            window.open(
                `https://www.google.com/search?q=${query}`,
                "_blank"
            );
        }

          if (
            transcript.includes(
                "open games"
            )
        ) {
            speak(
                "Opening GitHub"
            );

            window.open(
                "https://crazygames.com",
                "_blank"
            );
        }
          if (
            transcript.includes(
                "open instagram"
            )
        ) {
            speak(
                "Opening Instagram"
            );

            window.open(
                "https://instagram.com",
                "_blank"
            );
        }
          if (
            transcript.includes(
                "open gmail"
            )
        ) {
            speak(
                "Opening Gmail"
            );

            window.open(
                "https://gmail.com",
                "_blank"
            );
        }
        if (
            transcript.includes(
                "stop recognition"
            ) ||
            transcript.includes(
                "shut down"
            )
        ) {

            speak(
                "Stopping recognition"
            );

            recognition.stop();
        }
    };

   startBtn.addEventListener("click", () => {

    isListening = true;

    try{
        recognition.start();
    }
    catch(err){
        console.log(err);
    }
});

   stopBtn.addEventListener("click", () => {
    isListening = false;
    recognition.stop();
});

} else {

    alert(
        "Speech recognition is not supported in this browser."
    );
}

function speak(text) {

    const utterance = new SpeechSynthesisUtterance(text);

    const setVoiceAndSpeak = () => {

        const voices = speechSynthesis.getVoices();

        const maleVoice =
            voices.find(
                v => v.name === "Google UK English Male"
            ) ||
            voices.find(
                v => v.name === "Microsoft George - English (United Kingdom)"
            );

        if (maleVoice) {
            utterance.voice = maleVoice;
        }

        utterance.rate = 0.9;
        utterance.pitch = 0.75;
        utterance.volume = 1;

        speechSynthesis.speak(utterance);
    };

    if (speechSynthesis.getVoices().length === 0) {
        speechSynthesis.onvoiceschanged = setVoiceAndSpeak;
    } else {
        setVoiceAndSpeak();
    }
}


if (
    smallJarvisBtn &&
    machine
) {

    smallJarvisBtn.addEventListener(
        "click",
        () => {

            if (
                machine.style.transform ===
                "scale(0.5)"
            ) {

                machine.style.transform =
                    "scale(1)";

                machine.style.transformOrigin =
                    "center center";

                smallJarvisBtn.querySelector(
                    "p"
                ).textContent =
                    "Make Me Small";

            } else {

                machine.style.transform =
                    "scale(0.5)";

                machine.style.transformOrigin =
                    "bottom right";

                smallJarvisBtn.querySelector(
                    "p"
                ).textContent =
                    "Normal Size";
            }
        }
    );
}