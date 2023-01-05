/**
    @Author: Esteban Cabrera.
    @Version: 1.0.0.
    @See: /templates/index.html
    
    Este script se realizo para manejar el elemento de UI de la pantalla del login (index.html).
    Tiene dos metodos que realizan un toggle entre los formularios de ingreso y de re-establecimiento del
    PIN del usuario.
 */

function toggle_login_form() {
    /*
        Este metodo realiza la accion de esconder el formulario de login y muestra el formulario del
        re-establecimiento del PIN de usuario haciendo cambios en las propiedades 'display' del estilo
        de los elementos 'login-form' y 'reset-pin-form' que se encuentran en /templates/index.html.
    */
    document.getElementById("login-form").style.display = "none";
    document.getElementById("reset-pin-form").style.display = "inline";
}

function toggle_reset_pin_form() {
    /*
        Este metodo realiza la accion de esconder el formulario del re-establecimiento del PIN de usuario
        y muestra el formulario del haciendo cambios en las propiedades 'display' del estilo
        de los elementos 'login-form' y 'reset-pin-form' que se encuentran en /templates/index.html.
    */
    document.getElementById("login-form").style.display = "inline";
    document.getElementById("reset-pin-form").style.display = "none";
}

