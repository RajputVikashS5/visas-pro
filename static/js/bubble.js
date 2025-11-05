// AI Second Brain Summary Bubble
document.addEventListener('mouseup', () => {
    const selection = window.getSelection();
    const text = selection.toString().trim();
    if (text.length > 10) {
        fetch('/ask', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({query: `Summarize this text: ${text}`})
        }).then(r => r.json())
          .then(data => {
              document.getElementById('bubble-text').textContent = data.response;
              document.getElementById('summary-bubble').classList.remove('hidden');
          });
        selection.removeAllRanges();
    }
});

// Hide bubble after 10s
setTimeout(() => {
    document.getElementById('summary-bubble').classList.add('hidden');
}, 10000);