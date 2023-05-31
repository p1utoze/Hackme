function checker()
{
    let a = document.getElementById("check_in");
    let b = document.getElementById("check_out");
    if (a.checked || b.checked)
        return true
    return false
}

function verifyPassword() {
    event.preventDefault()
    let passwordInput = document.getElementById("input").value;
    const passphrase = "{{ password }}";  // Replace with your actual passphrase
    console.log(passphrase);
    console.log(passwordInput);
    console.log(typeof passwordInput === passphrase)
    if (passwordInput === passphrase) {
        // Password matches, submit the form
        document.forms[0].submit();

    } else {
        // Password doesn't match, display an error message or take appropriate action
        alert("Incorrect password");
    }
}