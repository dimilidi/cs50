const questions = [
    {
        question: "What does HTML stand for?",
        choices: ["Http Transfer Modeling Language", "Hyper Text Markup Language", "Holistic Text Markup Language"],
        answer: "Hyper Text Markup Language"
    },
    {
        question: "Which ones are valid HTML document type definitions?",
        choices: ["<!doctype html-5>", "<!doctype html5>", "<!doctype html>"],
        answer: "<!doctype html>"
    },
    {
        question: "Which ones are valid HTML elements?",
        choices: ["<head>", "<header>", "<body>", "<row>", "<foot>", "<footer>"],
        answer: ["<header>", "<body>", "<footer>"]
    },
    {
        question: "Which ones are valid link definitions?",
        choices: [
            "<a src=\"http://www.google.de\">",
            "<a target=\"http://www.google.de\" ref=\"_blank\">",
            "<a href=\"http://www.google.de\" target=\"_blank\">",
            "<a href=\"email:john.doe@mail.com\">",
            "<a href=\"mailto:john.doe@mail.com\">"
        ],
        answer: ["<a href=\"http://www.google.de\" target=\"_blank\">", "<a href=\"mailto:john.doe@mail.com\">"]
    },
    {
        question: "Which ones are valid image definitions?",
        choices: [
            "<img src=\"http://lorempixel.com/350/250/cats/\" alt=\"Cat Adventures\">",
            "<img target=\"dog.jpeg\" width=\"200\" height=\"200\">",
            "<img href=\"hamster.gif\" alt=\"My funny hamster\" width=\"100%\">",
            "<img src=\"data:image/jpeg;base64,/9j/4RiD...\" width=\"150\" height=\"150\">",
            "<image src=\"horse.jpg\" width=\"250\" height=\"250\" alt=\"My little pony\">"
        ],
        answer: ["<img src=\"http://lorempixel.com/350/250/cats/\" alt=\"Cat Adventures\">", "<img src=\"data:image/jpeg;base64,/9j/4RiD...\" width=\"150\" height=\"150\">"]
    }
];

let currentQuestionIndex = 0;

function displayQuestion() {
    const questionElement = document.getElementById("question");
    const choicesElement = document.getElementById("choices");

    questionElement.textContent = questions[currentQuestionIndex].question;
    choicesElement.innerHTML = "";

    questions[currentQuestionIndex].choices.forEach(choice => {
        const button = document.createElement("button");
        button.textContent = choice;
        button.className = "btn btn-outline-primary";
        button.onclick = () => alert(
            Array.isArray(questions[currentQuestionIndex].answer)
                ? questions[currentQuestionIndex].answer.includes(choice)
                    ? "Correct!"
                    : "Wrong!"
                : choice === questions[currentQuestionIndex].answer
                    ? "Correct!"
                    : "Wrong!"
        );
        choicesElement.appendChild(button);
    });
}

document.getElementById("nextBtn").onclick = () => {
    currentQuestionIndex = (currentQuestionIndex + 1) % questions.length;
    displayQuestion();
};

displayQuestion();
