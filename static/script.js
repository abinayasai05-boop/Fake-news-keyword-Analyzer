async function analyzeNews() {

    const text = document.getElementById("newsText").value.trim();

    if (!text) {
        alert("Please enter a news headline or article.");
        return;
    }

    try {

        const response = await fetch("/analyze", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                text: text
            })
        });

        const data = await response.json();

        if (!response.ok) {
            alert(data.error);
            return;
        }

        displayResults(data);

    } catch (error) {

        console.error(error);

        alert(
            "Unable to connect to the analyzer. " +
            "Make sure Flask is running."
        );
    }
}


function displayResults(data) {

    document.getElementById("results")
        .classList.remove("hidden");


    const icon = document.getElementById("resultIcon");

    if (data.level === "danger") {
        icon.textContent = "🔴";
    }
    else if (data.level === "warning") {
        icon.textContent = "🟡";
    }
    else {
        icon.textContent = "🟢";
    }


    document.getElementById("resultTitle")
        .textContent = data.result;


    document.getElementById("resultDescription")
        .textContent =
        `Fake score: ${data.fake_score} | ` +
        `Reliable score: ${data.reliable_score}`;


    document.getElementById("riskPercentage")
        .textContent = data.risk_percentage + "%";


    document.getElementById("riskBar")
        .style.width = data.risk_percentage + "%";


    document.getElementById("wordCount")
        .textContent = data.word_count;

    document.getElementById("sentenceCount")
        .textContent = data.sentence_count;

    document.getElementById("exclamationCount")
        .textContent = data.exclamation_count;

    document.getElementById("questionCount")
        .textContent = data.question_count;


    createKeywords(
        "fakeKeywords",
        data.fake_keywords,
        "fake"
    );


    createKeywords(
        "reliableKeywords",
        data.reliable_keywords,
        "reliable"
    );


    const reasons = document.getElementById("reasons");

    reasons.innerHTML = "";

    data.reasons.forEach(reason => {

        const li = document.createElement("li");

        li.textContent = reason;

        reasons.appendChild(li);
    });


    document.getElementById("results")
        .scrollIntoView({
            behavior: "smooth"
        });
}


function createKeywords(elementId, keywords, className) {

    const container = document.getElementById(elementId);

    container.innerHTML = "";

    if (keywords.length === 0) {

        container.innerHTML =
            "<span class='keyword'>None detected</span>";

        return;
    }

    keywords.forEach(keyword => {

        const span = document.createElement("span");

        span.className = `keyword ${className}`;

        span.textContent = keyword;

        container.appendChild(span);
    });
}


function clearText() {

    document.getElementById("newsText").value = "";

    document.getElementById("results")
        .classList.add("hidden");
}