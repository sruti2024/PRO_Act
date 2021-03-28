const emailField = document.querySelector("#email");
const usernameField = document.querySelector("#username");
const password1Field = document.querySelector("#password1");
const password2Field = document.querySelector("#password2");
const emailFeedBackArea = document.querySelector(".emailFeedBackArea");
const usernameFeedBackArea = document.querySelector(".usernameFeedBackArea");
const passwordFeedBackArea = document.querySelector(".passwordFeedBackArea");
const sendOtpBtn = document.querySelector("#sendOtpBtn");
const otpFeedBackArea = document.querySelector(".OTPStatusFeedBackArea");
const verifyOTPFeedback = document.querySelector(".OTPFeedBackArea");
const verifyOtpBtn = document.querySelector("#verifyOtpBtn");

emailField.addEventListener("keyup", (e) => {
  const emailVal = e.target.value;

  emailField.classList.remove("is-invalid");
  emailFeedBackArea.style.display = "none";

  if (emailVal.length > 0) {
    fetch("/validate-email/", {
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

usernameField.addEventListener("keyup", (e) => {
  const usernameVal = e.target.value;

  usernameField.classList.remove("is-invalid");
  usernameFeedBackArea.style.display = "none";

  if (usernameVal.length > 0) {
    fetch("/validate-username/", {
      body: JSON.stringify({ username: usernameVal }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.username_error) {
          sendOtpBtn.disabled = true;
          usernameField.classList.add("is-invalid");
          usernameFeedBackArea.style.display = "block";
          usernameFeedBackArea.innerHTML = `<p>${data.username_error}</p>`;
        } else if (data.username_length_error) {
            sendOtpBtn.disabled = true;
            usernameField.classList.add("is-invalid");
            usernameFeedBackArea.style.display = "block";
            usernameFeedBackArea.innerHTML = `<p>${data.username_length_error}</p>`;
        }
        else {
          sendOtpBtn.removeAttribute("disabled");
        }
      });
  }
});

password1Field.addEventListener("keyup", (e) => {
  const passwordVal = e.target.value;

  password1Field.classList.remove("is-invalid");
  passwordFeedBackArea.style.display = "none";

  if (passwordVal.length > 0) {
    fetch("/validate-password/", {
      body: JSON.stringify({
        password1: passwordVal,
      }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.password_error) {
          sendOtpBtn.disabled = true;
          password1Field.classList.add("is-invalid");
          passwordFeedBackArea.style.display = "block";
          passwordFeedBackArea.innerHTML = `<p>${data.password_error}</p>`;
        } else {
          sendOtpBtn.removeAttribute("disabled");
        }
      });
  }
});

password2Field.addEventListener("keyup", (e) => {
  const passwordVal = e.target.value;
  const password1Val = document.getElementById("password1").value;

  password2Field.classList.remove("is-invalid");
  passwordFeedBackArea.style.display = "none";

  if (passwordVal.length > 0) {
    fetch("/match-passwords/", {
      body: JSON.stringify({
        password1: password1Val,
        password2: passwordVal,
      }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        if (data.password_mismatch) {
          sendOtpBtn.disabled = true;
          password2Field.classList.add("is-invalid");
          passwordFeedBackArea.style.display = "block";
          passwordFeedBackArea.innerHTML = `<p>${data.password_mismatch}</p>`;
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
  let fname = $("#fname").val();
  $.ajax({
    url: "/send-otp/",
    type: "GET",
    data: {
      email: email,
      fname: fname,
    },
    success: function (data) {
      console.log(data);
      sendOtpBtn.innerHTML = "Get OTP";
      if (data.otp_error) {
        otpFeedBackArea.style.display = "block";
        otpFeedBackArea.innerHTML = `<p class='alert alert-danger'>${data.otp_error}</p>`;
      } else {
        otpFeedBackArea.style.display = "block";
        otpFeedBackArea.innerHTML = `<p class='alert alert-success'>${data.otp_sent}</p>`;
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
        verifyOtpBtn.innerHTML =
          '<div class="spinner-border text-light" role="status"><span class="sr-only">Loading...</span></div>';
        document.getElementById("signupForm").submit();
      }
    },
  });
}
