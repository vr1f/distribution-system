

/**
  Methods relating to search function
 */
(() => {

  const search = async () => {
    const firstName = document.getElementById("firstname").value;
    const lastName = document.getElementById("lastname").value;
    // Recipient => Value = 1  Donor => Value = 2
    const type = document.getElementById("type").value;
    // TO DO: POST REQUEST
    // TO DO: VALID FORM CHECK
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