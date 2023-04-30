/**
  Factory methods for rendering UI elements
 */
"use strict";

(() => {
  console.log("loaded ui_factory")

  // Declaration in global namespace
  window.UiFactory = {};

  /**
    A factory that creates HTML table elements.
    @param {Object} tableData
    @param {Array} tableData.headers - Array of table headers, they need to be
      consistent with the keys of the data field.
    @param {Array} tableData.data - Array of table data consisting of objects.
    @param {Object} tableData.data[] - An object holding table data that has
      keys consistent with the headers field.
    @return {HTMLElement} A HTML element that can be added to the DOM.
   */
  window.UiFactory.createTable = (tableData) => {
    console.log(tableData)
    const {headers, data} = tableData;

    // Create the table element
    const table = document.createElement("table")
    table.classList.add("table")

    // Create table artefacts
    const tr = document.createElement("tr")
    const th = document.createElement("th")
    const td = document.createElement("td")

    // Build the header
    const thead = document.createElement("thead")
    const tableHeadRow = tr.cloneNode()
    headers.map((label) => {
      const cell = th.cloneNode()
      cell.setAttribute("scope", "col")
      cell.innerHTML = label
      tableHeadRow.appendChild(cell)
    })
    thead.appendChild(tableHeadRow)

    // Build the table body
    const tbody = document.createElement("tbody")
    data.map((row) => {
      const tableRow = tr.cloneNode()

      // Check that row data matches headers in number of elements
      if (Object.keys(row).length != headers.length) {
        console.error("Table Factory: Row data does not match headers")
        return
      }

      Object.values(row).map((content) => {
        const cell = td.cloneNode()
        cell.innerHTML = content
        tableRow.appendChild(cell)
      })

      tbody.appendChild(tableRow)
    })

    // Build the table
    table.appendChild(thead)
    table.appendChild(tbody)

    return table
  }

})()