/**
 * Popup for Chat-Save. Shows plain-language status and offers two actions.
 */

document.addEventListener("DOMContentLoaded", () => {
  const statusPill = document.getElementById("statusPill");
  const statusText = document.getElementById("statusText");
  const managedBadge = document.getElementById("managedBadge");
  const valUser = document.getElementById("valUser");
  const valServer = document.getElementById("valServer");
  const valQueue = document.getElementById("valQueue");
  const valReceipt = document.getElementById("valReceipt");
  const valLastSync = document.getElementById("valLastSync");
  const valDeadLetter = document.getElementById("valDeadLetter");
  const rowDeadLetter = document.getElementById("rowDeadLetter");
  const btnSyncNow = document.getElementById("btnSyncNow");
  const btnRetryDLQ = document.getElementById("btnRetryDLQ");
  const linkOptions = document.getElementById("linkOptions");

  /** level: "ok" | "warn" | "danger" */
  function setStatus(text, level) {
    statusText.textContent = text;
    statusPill.className = `status ${level === "ok" ? "" : level}`.trim();
  }

  function loadStatus() {
    chrome.runtime.sendMessage({ type: "GET_STATUS" }, (res) => {
      if (chrome.runtime.lastError || !res) {
        setStatus("Not connected", "danger");
        return;
      }

      const { config, pendingCount, deadLetterCount, lastReceipt, lastSyncTime } = res;

      valUser.textContent = config.identity?.user || "Not connected yet";
      valServer.textContent = config.serverUrl || "Not set";
      if (config.isManaged) managedBadge.style.display = "inline-block";

      if (deadLetterCount > 0) {
        rowDeadLetter.style.display = "flex";
        valDeadLetter.textContent = `${deadLetterCount} conversation(s)`;
        btnRetryDLQ.style.display = "flex";
        setStatus("Needs attention", "danger");
      } else {
        rowDeadLetter.style.display = "none";
        btnRetryDLQ.style.display = "none";
        if (pendingCount > 0) {
          setStatus("Saving...", "warn");
        } else {
          setStatus("Up to date", "ok");
        }
      }

      if (pendingCount > 0) {
        valQueue.textContent = `${pendingCount} conversation(s)`;
        valQueue.className = "val warn";
      } else {
        valQueue.textContent = "None";
        valQueue.className = "val";
      }

      if (lastReceipt) {
        const n = lastReceipt.saved_messages || 0;
        valReceipt.textContent = `${n} message${n === 1 ? "" : "s"} saved`;
      }

      if (lastSyncTime) {
        const d = new Date(lastSyncTime);
        valLastSync.textContent = d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
      }
    });
  }

  btnRetryDLQ.addEventListener("click", () => {
    btnRetryDLQ.disabled = true;
    btnRetryDLQ.textContent = "Trying again...";
    chrome.runtime.sendMessage({ type: "RETRY_DEAD_LETTER" }, () => {
      if (chrome.runtime.lastError) { /* consumed */ }
      setTimeout(() => {
        loadStatus();
        btnRetryDLQ.disabled = false;
        btnRetryDLQ.textContent = "Try again for failed saves";
      }, 800);
    });
  });

  btnSyncNow.addEventListener("click", () => {
    btnSyncNow.disabled = true;
    btnSyncNow.textContent = "Saving...";
    chrome.runtime.sendMessage({ type: "SYNC_NOW" }, () => {
      if (chrome.runtime.lastError) { /* consumed */ }
      setTimeout(() => {
        loadStatus();
        btnSyncNow.disabled = false;
        btnSyncNow.textContent = "Save now";
      }, 1000);
    });
  });

  linkOptions.addEventListener("click", () => {
    if (chrome.runtime.openOptionsPage) {
      chrome.runtime.openOptionsPage();
    } else {
      window.open(chrome.runtime.getURL("options.html"));
    }
  });

  loadStatus();
});
