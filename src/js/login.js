/**
  Methods relating to user login
 */
(() => {
    const login = async() => {
      const url = "http://localhost:8000/check_login"
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;
      const result = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: username,
          password: password
        }),
      })
      .then((response) => {
        if (response.status != 200) {
          throw new Error ("Unauthorized Request");
        }
        alert("Login Success!");
        return response.json();
      })
      .then((json) => {
        const token = json.token;
        setCookie(token);
        window.location = "http://localhost:8000/home";
        return json;
      })
      .catch((error) => {
        alert(error.message);
      })
    }

    const setCookie = (token) => {
      const minutes = 60000;
      const currTime = new Date().getTime();
      const expiryTime = currTime + (30 * minutes);
      const expiryUTC = new Date(expiryTime).toUTCString();
      document.cookie = `token=${token}; expires=${expiryUTC}`;
    }

    const bindButtonActions = () => {
      document.getElementById("submit").addEventListener("click", login)
    }
    
    /**
        Run on load
    */
    window.onload = () => {
      bindButtonActions();
    }
  })()