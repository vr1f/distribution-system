/**
  Methods relating to user login
 */
(() => {
  // Resets form
  const clearForm = () => {
    document.getElementById("username").value = "";
    document.getElementById("password").value = "";
    document.getElementById("privilege").value = 0;
  }

  // Check if all fields are filled by user
  const isValid = (username, password, privilege) => {
    return (username != "" && password != "" && privilege != 0);
  }

  // TO DO: Check if require privilege option or to use a default (user)
  const registerUser = async () => {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    // Admin => Value = 1  User => Value = 2 (defined in db_builder.py)
    const privilege = document.getElementById("privilege").value;
    if (isValid(username, password, privilege)) {
      // If all fields are entered
      const result = await fetch("/add_new_user", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: username,
          password: password,
          privilege: privilege,
        }),
      })
      .then((response) => {
        if (response.status != 201) {
          throw new Error("Unable to register new user!");
        }
        alert("User registered!");
        return response.json();
      })
      .catch((error) => {
        alert(error.message);
      })
    } else {
      alert("Please fill all of the required fields.")
    }
    clearForm();
  }

  const bindButtonActions = () => {
    document.getElementById("submit").addEventListener("click", registerUser)
  }

  /**
     Run on load
 */
  window.addEventListener("load", () => {
    bindButtonActions();
  })
})()