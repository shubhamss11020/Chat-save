/**
 * Welcome page: the person must tick the box and press Start saving before anything is captured.
 * The choice is stored with the date and the consent version, so it is clear what was agreed to.
 */
const CONSENT_VERSION = 1;  // keep in step with background.js
// Replace with the real address of the published privacy policy before submitting to the store.
const PRIVACY_POLICY_URL = "https://PASTE-PRIVACY-POLICY-URL-HERE";

const agree = document.getElementById("agree");
const start = document.getElementById("start");
const notNow = document.getElementById("notNow");
const done = document.getElementById("done");
const policyLink = document.getElementById("policyLink");

policyLink.href = PRIVACY_POLICY_URL;
agree.addEventListener("change", () => { start.disabled = !agree.checked; });

start.addEventListener("click", async () => {
  if (!agree.checked) return;
  await chrome.storage.local.set({
    chatsave_consent: { accepted: true, version: CONSENT_VERSION, at: new Date().toISOString() },
  });
  start.disabled = true;
  notNow.disabled = true;
  done.style.display = "block";
});

notNow.addEventListener("click", () => {
  window.close();
});
