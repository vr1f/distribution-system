

/**
  Methods relating to search function
 */
(() => {

  // Display results that have matching first names to user input
  function search() {
    const input = document.getElementById('search').value.toLowerCase();
    const table = document.getElementById("table");
    const tr = table.getElementsByTagName("tr");

    // Check each row and display matching results
    for (i = 0; i < tr.length; i++) {
      var td = tr[i].getElementsByTagName("td")[0];
      if (td) {
        const text = td.textContent.toLowerCase();
        if (text.includes(input)) {
          tr[i].style.display = "";
        } else {
          tr[i].style.display = "none";
        }
      }
    }
  }

  const bindButtonActions = () => {
    document.getElementById("search").addEventListener("input", search);
  }

  /**
     Run on load
  */
  window.addEventListener("load", () => {
    bindButtonActions();
  })
})()