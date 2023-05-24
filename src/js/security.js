/**
  Methods relating to security settings
 */
(() => {

  // Resets form
  const clearForm = () => {
    document.getElementById("lockout-period").value = "";
    document.getElementById("login-attempts").value = "";
  }

  // Update placeholder value after update
  const updateForm = (lockoutPeriod, loginAttempts) => {
    document.getElementById("lockout-period").placeholder = lockoutPeriod;
    document.getElementById("login-attempts").placeholder = loginAttempts;
  }

  // Check if settings inputted is valid
  const isValid = (lockoutPeriod, loginAttempts) => {
    return ((lockoutPeriod == "" || lockoutPeriod >= 0) && (loginAttempts == "" || loginAttempts >= 0)) 
  }

  // Sends new login settings to API endpoint
  const updateSettings = async () => {
    var lockoutPeriod = document.getElementById("lockout-period").value;
    var loginAttempts = document.getElementById("login-attempts").value;
    if (isValid(lockoutPeriod, loginAttempts)) {
      // Check if input is positive
      if (lockoutPeriod == "") {
        // If left empty OR accidental string input, use previous existing value
        lockoutPeriod = document.getElementById("lockout-period").getAttribute("placeholder");
      }
      if (loginAttempts == "") {
        // If left empty OR accidental gibberish string input, use previous existing value
        loginAttempts = document.getElementById("login-attempts").getAttribute("placeholder");
      }

      const result = await fetch("/update_admin_settings", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          lockout_period: lockoutPeriod,
          login_attempts: loginAttempts
        }),
      })
      .then((response) => {
        if (response.status != 200) {
          throw new Error("Unable to save updated settings!");
        }
        updateForm(lockoutPeriod,loginAttempts);
        clearForm();
        alert("Settings updated!");
        return response.json();
      })
      .catch((error) => {
        alert(error.message);
      })
    } else {
      // Inputted values are negative
      alert("Invalid values, please try again!")
      clearForm();
    }
  }

  const bindButtonActions = () => {
    document.getElementById("save").addEventListener("click", updateSettings)
  }

  /**
     Run on load
 */
  window.addEventListener("load", () => {
    bindButtonActions();
  })
})()