/*
 *
 * login-register modal
 * Autor: Creative Tim
 * Web-autor: creative.tim
 * Web script: http://creative-tim.com
 *
 */
function showRegisterForm() {
  $(".loginBox").fadeOut("fast", function () {
    $(".registerBox").fadeIn("fast");
    $(".login-footer").fadeOut("fast", function () {
      $(".register-footer").fadeIn("fast");
    });
  });
  $(".error").removeClass("alert alert-danger").html("");
}
function showLoginForm() {
  $("#loginModal .registerBox").fadeOut("fast", function () {
    $(".loginBox").fadeIn("fast");
    $(".register-footer").fadeOut("fast", function () {
      $(".login-footer").fadeIn("fast");
    });
  });
  $(".error").removeClass("alert alert-danger").html("");
}

function openLoginModal() {
  showLoginForm();
  setTimeout(function () {
    $("#loginModal").modal("show");
  }, 230);
}
function openRegisterModal() {
  showRegisterForm();
  setTimeout(function () {
    $("#loginModal").modal("show");
  }, 230);
}

function loginAjax() {
  var email = document.getElementById("emailLog").value;
  var zip = document.getElementById("passwordLog").value;
  if (!email || !zip) {
    shakeModal();
    return;
  }
  $.ajax({
    type: "POST",
    url: "login",
    data: $("#loginForm").serialize(),
    success: function (data) {
      window.location.replace("/");
    },
    error: function (data) {
      console.log("uyee");
      shakeModal();
    },
  });
}

function registerAjax() {
  //   Remove this comments when moving to server
  //   $.post("/register", function (data) {
  //     console.log(data);
  //     if (data == 1) {
  //     } else {
  //       shakeModal();
  //     }
  //   });
  var form = document.getElementById("registerForm");
  var email = document.getElementById("emailRegister").value;
  var zip = document.getElementById("zipCodeRegister").value;
  var password = document.getElementById("passwordRegister").value;
  var confirmation = document.getElementById("password_confirmationRegister")
    .value;
  if (!email || !zip || !password || !confirmation) {
    shakeModal();
    return;
  }
  var n = password.localeCompare(confirmation);
  console.log(n);
  console.log(password);
  console.log(confirmation);
  if (n != 0) {
    shakeModal();
    console.log("wagwan2");
    return;
  }
  console.log("wagwan");
  $.ajax({
    type: "POST",
    url: "register",
    data: $("#registerForm").serialize(),
    success: function (data) {
      window.location.replace("/");
    },
    error: function (data) {
      shakeModal();
    },
  });

  // $(document).ready(function () {

  // $.post("/register", $("#registerForm").serialize())
  // ("registerForm").on("submit", function (event) {
  //   event.preventDefault();
  //   $.ajax({
  //     url: $(this).attr("action"),
  //     processData: false,
  //     contentType: false,
  //     type: "POST",
  //     data: $(this).serialize(),
  //     dataType: "json",
  //     success: function (data) {
  //       console.log("wagwan3");
  //       window.location.replace("/");
  //     },
  //     error: function (data) {
  //       console.log("wagwan3");
  //       window.location.replace("/");
  //     },
  //   });
  // });

  // });
  // $("#registerForm").submit(function(){
  //   $(this).ajaxSubmit();
  //   success: function (response) {
  //     console.log("wagwan3");
  //     window.location.replace("/");
  //   },
  //   failure: function (response) {
  //     console.log("wagwan3");
  //     window.location.replace("/");
  //   },
  // });
}
function shakeModal() {
  $("#loginModal .modal-dialog").addClass("shake");
  $(".error")
    .addClass("alert alert-danger")
    .html("Invalid email/password combination");
  $('input[type="password"]').val("");
  setTimeout(function () {
    $("#loginModal .modal-dialog").removeClass("shake");
  }, 1000);
}
