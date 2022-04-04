function toggle_login_form() {
    document.getElementById("login-form").style.display = "none";
    document.getElementById("reset-pin-form").style.display = "inline";
}

function toggle_reset_pin_form() {
    document.getElementById("login-form").style.display = "inline";
    document.getElementById("reset-pin-form").style.display = "none";
}

