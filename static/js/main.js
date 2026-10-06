/**
 * College Student Management System - Main Interactive JavaScript
 */

document.addEventListener("DOMContentLoaded", function () {
  initChatWidget();
  initTableSearch();
  initDemoCredentials();
});

// ==================== FLOATING AI CHATBOT ====================
function initChatWidget() {
  const toggleBtn = document.getElementById("chatToggleBtn");
  const chatWindow = document.getElementById("chatWindow");
  const closeBtn = document.getElementById("chatCloseBtn");
  const sendBtn = document.getElementById("chatSendBtn");
  const chatInput = document.getElementById("chatInput");
  const messagesContainer = document.getElementById("chatMessages");
  const pills = document.querySelectorAll(".chat-pill");

  if (!toggleBtn || !chatWindow) return;

  toggleBtn.addEventListener("click", () => {
    chatWindow.classList.toggle("open");
    if (chatWindow.classList.contains("open")) {
      chatInput.focus();
    }
  });

  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      chatWindow.classList.remove("open");
    });
  }

  // Handle pill click
  pills.forEach((pill) => {
    pill.addEventListener("click", () => {
      const query = pill.getAttribute("data-query") || pill.innerText;
      chatInput.value = query;
      sendChatMessage();
    });
  });

  if (sendBtn) {
    sendBtn.addEventListener("click", sendChatMessage);
  }

  if (chatInput) {
    chatInput.addEventListener("keypress", (e) => {
      if (e.key === "Enter") {
        e.preventDefault();
        sendChatMessage();
      }
    });
  }

  function sendChatMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    // Append user message
    appendMessage(text, "user");
    chatInput.value = "";

    // Show typing bubble
    const typingId = showTypingIndicator();

    fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text }),
    })
      .then((res) => res.json())
      .then((data) => {
        removeTypingIndicator(typingId);
        appendMessage(data.reply, "bot", data.sources);
      })
      .catch((err) => {
        removeTypingIndicator(typingId);
        appendMessage(
          "I apologize, but I encountered a momentary connection hiccup. Please ask me again or check your network.",
          "bot"
        );
      });
  }

  function appendMessage(text, sender, sources = []) {
    const msgDiv = document.createElement("div");
    msgDiv.className = `chat-msg ${sender}`;

    // Format basic markdown (bold, lists, emojis)
    let formattedText = escapeHtml(text)
      .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
      .replace(/\*(.*?)\*/g, "<em>$1</em>")
      .replace(/\n• /g, "<br>• ")
      .replace(/\n- /g, "<br>• ")
      .replace(/\n\n/g, "<br><br>")
      .replace(/\n/g, "<br>");

    msgDiv.innerHTML = formattedText;

    if (sources && sources.length > 0) {
      const srcDiv = document.createElement("div");
      srcDiv.style.fontSize = "0.7rem";
      srcDiv.style.color = "#64748b";
      srcDiv.style.marginTop = "6px";
      srcDiv.style.borderTop = "1px dashed #cbd5e1";
      srcDiv.style.paddingTop = "4px";
      srcDiv.innerHTML = `📚 Verified Source: ${sources.join(", ")}`;
      msgDiv.appendChild(srcDiv);
    }

    messagesContainer.appendChild(msgDiv);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
  }

  function showTypingIndicator() {
    const id = "typing-" + Date.now();
    const ind = document.createElement("div");
    ind.id = id;
    ind.className = "typing-indicator";
    ind.innerHTML = `
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
      <div class="typing-dot"></div>
    `;
    messagesContainer.appendChild(ind);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
    return id;
  }

  function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  function escapeHtml(string) {
    return String(string)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }
}

// ==================== TABLE FILTER & SEARCH ====================
function initTableSearch() {
  const searchInput = document.getElementById("tableSearchInput");
  const targetTable = document.querySelector(".data-table tbody");

  if (!searchInput || !targetTable) return;

  searchInput.addEventListener("input", function () {
    const filter = searchInput.value.toLowerCase();
    const rows = targetTable.getElementsByTagName("tr");

    for (let i = 0; i < rows.length; i++) {
      const text = rows[i].textContent.toLowerCase();
      rows[i].style.display = text.indexOf(filter) > -1 ? "" : "none";
    }
  });
}

// ==================== DEMO CREDENTIALS QUICK-FILLER ====================
function initDemoCredentials() {
  const demoBtns = document.querySelectorAll(".btn-demo-creds");
  if (!demoBtns.length) return;

  const usernameInput = document.getElementById("username");
  const passwordInput = document.getElementById("password");
  const roleSelect = document.getElementById("role");

  demoBtns.forEach((btn) => {
    btn.addEventListener("click", () => {
      const u = btn.getAttribute("data-user");
      const p = btn.getAttribute("data-pass");
      const r = btn.getAttribute("data-role");

      if (usernameInput) usernameInput.value = u;
      if (passwordInput) passwordInput.value = p;
      if (roleSelect && r) roleSelect.value = r;

      // Visual feedback
      btn.style.transform = "scale(0.96)";
      setTimeout(() => {
        btn.style.transform = "scale(1)";
      }, 150);
    });
  });
}

// Modal open/close helpers
window.openModal = function (modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "flex";
  }
};

window.closeModal = function (modalId) {
  const modal = document.getElementById(modalId);
  if (modal) {
    modal.style.display = "none";
  }
};
