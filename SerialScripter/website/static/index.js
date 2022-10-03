function deleteKey(keyId) {
    fetch("/delete-key", {
        method: "POST",
        body: JSON.stringify({ keyId: keyId }),
    }).then((_res) => {
        window.location.href = "/key-management";
    });
}