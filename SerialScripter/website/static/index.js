function deleteKey(keyId) {
    // fetch the end point created in views.py
    fetch("/delete-key", {
        method: "POST",
        body: JSON.stringify({ keyId: keyId }),
        // creates a json object that we can access as a dict in python containing the keyId that we need
    }).then((_res) => {
        // refreshes the page
        window.location.href = "/key-management";
    });
}

function deleteHost(hostname) {
    // fetch the end point created in views.py
    console.log(hostname)
    fetch("/delete/"+hostname, {
        method: "POST",
        // creates a json object that we can access as a dict in python containing the keyId that we need
    }).then((_res) => {
        // refreshes the page
        window.location.href = "/";
    });
}

function checkAllBoxesLinux(source) {
    var checkboxes = document.querySelectorAll('input[class="boxesLinux"]');

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i] != source)
            checkboxes[i].checked = source.checked;
    }
}

function checkAllBoxesWindows(source) {
    var checkboxes = document.querySelectorAll('input[class="boxesWindows"]');

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i] != source)
            checkboxes[i].checked = source.checked;
    }
}

function checkAllScriptsLinux(source) {
    var checkboxes = document.querySelectorAll('input[class="scriptsLinux"]');

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i] != source)
            checkboxes[i].checked = source.checked;
    }
}

function checkAllScriptsWindows(source) {
    var checkboxes = document.querySelectorAll('input[class="scriptsWindows"]');

    for (var i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i] != source)
            checkboxes[i].checked = source.checked;
    }
}
