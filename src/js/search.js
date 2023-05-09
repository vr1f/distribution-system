

/**
  Methods relating to search function
 */
(() => {


  // Check if first name is given
  const isValid = (firstName, type) => {
    return (firstName != "" && type != 0);
  }

  const search = async () => {
    const firstName = document.getElementById("firstname").value;
    const lastName = document.getElementById("lastname").value;
    // Recipient => Value = 1  Donor => Value = 2
    const type = document.getElementById("type").value;
    if (isValid(firstName, type)) {
      // If all fields are entered
      const result = await fetch("/search", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          firstname: firstName,
          lastname: lastName,
          type: type,
        }),
      })
      .then((response) => {
        if (response.status != 200) {
          throw new Error("Bad Request");
        }
        return response.json();
      })
      .then((json) => {
        // TO DO: Unpack and create table with UiFactory
      })
      .catch((error) => {
        alert(error.message);
      })
    } else {
      alert("Please fill the first name and type!")
    }
  }

  const bindButtonActions = () => {
    document
      .getElementById("submit")
      .addEventListener("click", () => {
        const testData = {
          headers: ["First Name", "Last Name", "Age", "Address"], data: [
            { a: "James", b: "T", c: 23, d: "14 Elizabeth Street" },
            { a: "Tom", b: "Z", c: 35, d: "9 Pelham Street" },
          ]
        }
        const tableNode = UiFactory && UiFactory.createTable(testData)
        const el = document.getElementById("factoryTarget")
        el.innerHTML = ""
        el.appendChild(tableNode)
      })
  }

  /**
     Run on load
  */
  window.addEventListener("load", () => {
    bindButtonActions();
  })
})()