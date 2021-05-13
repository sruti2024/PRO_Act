const emailField = document.querySelector("#email");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const sendOtpBtn = document.querySelector("#sendOtpBtn");
const otpFeedBackArea = document.querySelector(".otpFeedBackArea");
const verifyOTPFeedback = document.querySelector(".OTPFeedBackArea");
const verifyOtpBtn = document.querySelector("#verifyOtpBtn");

emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;

  emailField.classList.remove("is-invalid");
  emailFeedBackArea.style.display = "none";

  if (emailVal.length > 0) {
    fetch("/find-email/", {
      body: JSON.stringify({ email: emailVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.email_error) {
          sendOtpBtn.disabled = true;
          emailField.classList.add("is-invalid");
          emailFeedBackArea.style.display = "block";
          emailFeedBackArea.innerHTML = `<p>${data.email_error}</p>`;
        } else {
          sendOtpBtn.removeAttribute("disabled");
        }
      });
  }
});

function sendOTP() {
  sendOtpBtn.innerHTML =
    '<div class="spinner-border text-light" role="status"><span class="sr-only">Loading...</span></div>';
  let email = $("#email").val();
  $.ajax({
    url: "/send-otp/",
    type: "GET",
    data: {
      email: email,
    },
    success: function (data) {
      sendOtpBtn.innerHTML = "Get OTP";
      if (data.otp_error) {
        otpFeedBackArea.style.display = "block";
        otpFeedBackArea.innerHTML = `<p class='alert alert-danger text-center'>${data.otp_error}</p>`;
      } else {
        otpFeedBackArea.style.display = "block";
        otpFeedBackArea.innerHTML = `<p class='alert alert-success text-center'>${data.otp_sent}</p>`;
        $("#sendOtpBtn").hide();
        $("#afterOTP").slideDown(1000);
      }
    },
  });
}

function verifyOTP() {
  let otp = $("#otp").val();
  let email = $("#email").val();
  $.ajax({
    url: "/check-otp/",
    type: "GET",
    data: {
      email: email,
      otp: otp,
    },
    success: function (data) {
      if (data.otp_mismatch) {
        verifyOTPFeedback.style.display = "block";
        verifyOTPFeedback.innerHTML = `<p>${data.otp_mismatch}</p>`;
      } else {
        verifyOtpBtn.removeAttribute("disabled");
        otpFeedBackArea.style.display = "none";
        $("#afterOTP").hide();
        $("#newPassword").fadeIn(1000);
      }
    },
  });
}

const passwordField = document.querySelector("#password");
const passwordFeedBackArea = document.querySelector(".passwordFeedBackArea");
const changePasswordBtn = document.querySelector("#changePasswordBtn");

passwordField.addEventListener("keyup", (e) => {
  const passwordVal = e.target.value;

  passwordField.classList.remove("is-invalid");
  passwordFeedBackArea.style.display = "none";

  if (passwordVal.length > 0) {
    fetch("/validate-password/", {
      body: JSON.stringify({
        password: passwordVal,
      }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.password_error) {
          changePasswordBtn.disabled = true;
          passwordField.classList.add("is-invalid");
          passwordFeedBackArea.style.display = "block";
          passwordFeedBackArea.innerHTML = `<p>${data.password_error}</p>`;
        } else {
          changePasswordBtn.removeAttribute("disabled");
        }
      });
  }
});
