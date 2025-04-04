// static/main.js
async function callBackendEncrypt() {
    const message = document.getElementById("message").value;
    const key = document.getElementById("key").value;
    const resultDiv = document.getElementById("result");
  
    if (![16, 24, 32].includes(key.length)) {
      resultDiv.textContent = "Key must be 16, 24, or 32 characters long.";
      return;
    }
  
    const response = await fetch('/encrypt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message, key })
    });
  
    const data = await response.json();
    resultDiv.textContent = data.encrypted || data.error;
  }
  
  async function callBackendDecrypt() {
    const encrypted = document.getElementById("encrypted").value;
    const key = document.getElementById("key2").value;
    const resultDiv = document.getElementById("decryptedResult");
  
    if (![16, 24, 32].includes(key.length)) {
      resultDiv.textContent = "Key must be 16, 24, or 32 characters long.";
      return;
    }
  
    const response = await fetch('/decrypt', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ encrypted, key })
    });
  
    const data = await response.json();
    resultDiv.textContent = data.decrypted || data.error;
  }
  