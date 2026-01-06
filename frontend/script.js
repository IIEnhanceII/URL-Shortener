const API_BASE = "http://localhost:5000";

//ui
let currentState = "home"; 
// "home" | "shorten" | "open"

const shortenSection = document.getElementById("shortenSection");
const openSection = document.getElementById("openSection");

const shortenArrow = document.getElementById("shortenArrow");
const openArrow = document.getElementById("openArrow");

// from HOME
shortenSection.addEventListener("click", () => {
    if (currentState === "home") {
        expandShorten();
    }
});

openSection.addEventListener("click", () => {
    if (currentState === "home") {
        expandOpen();
    }
});
shortenArrow.addEventListener("click", (e) => {
    e.stopPropagation();

    if (currentState === "home") {
        expandShorten();
    } else if (currentState === "shorten") {
        // Shorten is expanded → go to Open
        expandOpen();
    }
});
openArrow.addEventListener("click", (e) => {
    e.stopPropagation();

    if (currentState === "home") {
        expandOpen();
    } else if (currentState === "open") {
        // Open is expanded → go to Shorten
        expandShorten();
    }
});

// state shift
function expandShorten() {
    shortenSection.classList.add("expanded");
    shortenSection.classList.remove("collapsed");

    openSection.classList.add("collapsed");
    openSection.classList.remove("expanded");

    // Arrow directions
    shortenArrow.textContent = "←"; // go to Open
    openArrow.textContent = "←";    // hidden but consistent

    currentState = "shorten";
}

function expandOpen() {
    openSection.classList.add("expanded");
    openSection.classList.remove("collapsed");

    shortenSection.classList.add("collapsed");
    shortenSection.classList.remove("expanded");

    // Arrow directions
    openArrow.textContent = "→";    // go to Shorten
    shortenArrow.textContent = "→"; // hidden but consistent

    currentState = "open";
}

// backend
// POST /api/shorten
function shortenUrl() {
    const input = document.getElementById("urlInput");
    const result = document.getElementById("shortenResult");

    const longUrl = input.value.trim();

    if (!longUrl) {
        result.innerHTML = "<span style='color:red'>Please enter a URL</span>";
        result.style.display = "block";
        return;
    }

    fetch(`${API_BASE}/api/shorten`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ long_url: longUrl })
    })
    .then(res => res.json())
    .then(data => {
        if (data.error) {
            result.innerHTML = `<span style="color:red">${data.error}</span>`;
        } else {
            result.innerHTML = `
                Short URL:
                <a href="${data.short_url}" target="_blank">
                    ${data.short_url}
                </a>
            `;
        }
        result.style.display = "block";
    })
    .catch(() => {
        result.innerHTML = "<span style='color:red'>Server error</span>";
        result.style.display = "block";
    });
}

// GET /<short_code> (backend handles redirect)
function openUrl() {
    const input = document.getElementById("shortUrlInput");
    const result = document.getElementById("openResult");

    const shortUrl = input.value.trim();

    if (!shortUrl) {
        result.innerHTML = "<span style='color:red'>Please enter a short URL</span>";
        result.style.display = "block";
        return;
    }

    window.open(shortUrl, "_blank");
}
