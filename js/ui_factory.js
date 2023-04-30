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
   */
  window.UiFactory.createTable = (tableData) => {
    console.log(tableData)
    const {headers, data} = tableData;

    // Create the table element
    const table = document.createElement("table")
    table.classList.add("table")

    // Create table artifacts
    const tr = document.createElement("tr")
    const th = document.createElement("th")
    const td = document.createElement("td")
    const tbody = document.createElement("tbody")

    const thead = document.createElement("thead")

    // Build the header
    const tableHeadRow = tr.cloneNode()
    headers.map((label) => {
      const cell = th.cloneNode()
      cell.setAttribute("scope", "col")
      cell.innerHTML = label
      tableHeadRow.appendChild(cell)
    })
    thead.appendChild(tableHeadRow)

    //TODO Build the table body

    // Build the table
    table.appendChild(thead)

    return table
  }

})()