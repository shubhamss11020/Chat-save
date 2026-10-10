/**
 * Popup Script for Chat-Save Extension
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
  const btnSyncNow = document.getElementById("btnSyncNow");
  const linkOptions = document.getElementById("linkOptions");

  function loadStatus() {
    chrome.runtime.sendMessage({ type: "GET_STATUS" }, (res) => {
      if (chrome.runtime.lastError || !res) {
        statusText.textContent = "Offline";
        statusPill.style.color = "#ef4444";
        statusPill.style.borderColor = "rgba(239, 68, 68, 0.3)";
        statusPill.style.background = "rgba(239, 68, 68, 0.15)";
        return;
      }

      const { config, pendingCount, lastReceipt, lastSyncTime } = res;

      valUser.textContent = config.userId || "user";
      valServer.textContent = config.serverUrl || "Not configured";

      if (config.isManaged) {
        managedBadge.style.display = "inline-block";
      }

      if (pendingCount > 0) {
        valQueue.textContent = `${pendingCount} item(s) pending`;
        valQueue.style.color = "#f59e0b";
        statusText.textContent = "Offline (Queued)";
        statusPill.style.color = "#f59e0b";
        statusPill.style.borderColor = "rgba(245, 158, 11, 0.3)";
        statusPill.style.background = "rgba(245, 158, 11, 0.15)";
      } else {
        valQueue.textContent = "0 pending (clean)";
        valQueue.style.color = "#10b981";
        statusText.textContent = "Active";
        statusPill.style.color = "#10b981";
        statusPill.style.borderColor = "rgba(16, 185, 129, 0.3)";
        statusPill.style.background = "rgba(16, 185, 129, 0.15)";
      }

      if (lastReceipt) {
        valReceipt.textContent = `${lastReceipt.receipt_id} (${lastReceipt.saved_messages} msgs)`;
      }

      if (lastSyncTime) {
        const d = new Date(lastSyncTime);
        valLastSync.textContent = d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit", second: "2-digit" });
      }
    });
  }

  btnSyncNow.addEventListener("click", () => {
    btnSyncNow.disabled = true;
    btnSyncNow.innerHTML = "<span>⟳</span><span>Syncing...</span>";
    chrome.runtime.sendMessage({ type: "SYNC_NOW" }, () => {
      setTimeout(() => {
        loadStatus();
        btnSyncNow.disabled = false;
        btnSyncNow.innerHTML = "<span>⟳</span><span>Sync Outbox Now</span>";
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
