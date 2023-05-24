/**
  Methods relating to recipient functionality
 */
"use strict";

(() => {

  console.log("loaded inventory")

  /** The state for this page */
  const state = {}

  /** Templates for various elements */
  state.template = {}
  state.template.addInventoryFormElements = [
    {
      label: "Name", placeholder: "Name",
      name:"item_name", required: true
    },
    {
      label: "Brand", placeholder: "Enter Brand (optional)",
      name: "item_brand"
    },
    {
      type: "select", name:"category_id", required: true,
      options: [], label: "Category"
    },
    {
      label: "Quantity", placeholder: "Enter Quantity",
      name: "item_quantity", type: "number", required: true
    },
    {
      label: "Size", placeholder: "Enter 1, 2, 3 or XL, XXL (optional)",
      name: "size",
    },
    {
      label: "Expiry Date", placeholder: "Enter expiry date (optional)",
      name: "expiry_date", type: "date"
    },
    {
      label: "Main Ingredients", placeholder: "Enter main ingredients (optional)",
      name: "ingredients"
    },
    {
      label: "Allergens", placeholder: "Enter any allergens (optional)",
      name: "allergen_info"
    },
    {
      label: "From Donor", placeholder: "Please select a donor who donated this item",
      name: "from_donor", type: "select", options: []
    },
  ];

  state.template.addAidCategoryFormElements = [
    {
      label: "Category Name", placeholder: "Enter aid category name",
      name:"category_name", required: true
    },
    {
      type: "select", name:"status", required: true, label: "Status",
      options: [
        {name: "Status Low", value: "low"},
        {name: "Status Medium", value: "medium"},
        {name: "Status High", value: "high"},
      ]
    }
  ]

  /**
    Representing info an inventory item, this should match `inventory.py`
    @todo Match this with inventory.py once it is complete
   */
  class Inventory {
    constructor(params) {
      const {
        item_id = undefined,
        item_name,
        item_quantity,
        item_brand = "",
        expiry_date = "",
        ingredients = "",
        allergen_info = "",
        size = "",
        category_id,
        from_donor,
      } = params
      this.item_id = item_id;
      this.item_name = item_name;
      this.item_brand = item_brand;
      this.category = state.inventory.categories.reduce((value, category) => {
        // Dynamically map category_id to category_name
        if (category_id == category.category_id) {
          value = category.category_name;
        }
        return value;
      }, "")
      this.item_quantity = item_quantity;
      this.size = size;
      this.expiry_date = expiry_date;
      this.ingredients = ingredients;
      this.allergen_info = allergen_info;
      this.from_donor = state.inventory.donors.reduce((value, donor) => {
        if (from_donor == donor.donor_id) {
          value = donor.first_name;
        }
        return value;
      }, "")
    }
  }

  class InventoryState {
    constructor() {
      this.items = [];

      // object.keys = {category_id, category_name, status}
      this.categories = [];

      this.donors = [];

      window.dispatchEvent(new CustomEvent("app.register.callback", {
        detail: {
          eventName: "inventory.add",
          callback: this.showInventoryModal.bind(this)
        }
      }));

      window.dispatchEvent(new CustomEvent("app.register.callback", {
        detail: {
          eventName: "aid_category.add",
          callback: this.showCategoryModal.bind(this)
        }
      }));

      // Fetch categories, inventory records and donors from the server
      new Promise((resolve, reject) => {
        this.refreshCategories(resolve);
      })
      .then(() => {
        return new Promise((resolve, reject) => {
          this.refreshDonors(resolve);
        })
      })
      .then(() => {
        this.refreshRecords();
      }
      )
    }

    addInventory(inventory) {
      this.items.push(inventory);
    }

    updateInventory(id, inventory) {
      alert("To implement");
    }

    deleteInventory(id) {
      alert("To implement");
    }

    showInventoryModal(modalElements) {
      // alert("To implement")
      const {
        modalHeading,
        modalBody,
        modalAction
      } = modalElements

      // Heading
      modalHeading.innerHTML = "Add new inventory";

      // Form elements in the body
      const inputForm = window.UiFactory.createModalForm(
        state.template.addInventoryFormElements.map((element) => {
          // Map categories to selector
          if (element.name == "category_id") {
            element.options = this.categories.map((category) => {
              return {
                name: category.category_name,
                value: category.category_id
              }
            });
          }
          if (element.name == "from_donor") {
            element.options = this.donors.map((donor) => {
              return {
                name: donor.first_name,
                value: donor.donor_id
              }
            });
          }

          return element;
        })
      )
      modalBody.innerHTML = ""
      modalBody.appendChild(inputForm)

      // Submit button
      modalAction.innerHTML = "Submit";
      modalAction.addEventListener("click", onCreateInventory)

    }

    showCategoryModal(modalElements) {
      // alert("To implement")
      const {
        modalHeading,
        modalBody,
        modalAction
      } = modalElements

      // Heading
      modalHeading.innerHTML = "Add aid category";

      // Form elements in the body
      const inputForm = window.UiFactory.createModalForm(
        state.template.addAidCategoryFormElements
      )
      modalBody.innerHTML = ""
      modalBody.appendChild(inputForm)

      // Submit button
      modalAction.innerHTML = "Submit";
      modalAction.addEventListener("click", onCreateCategory)
    }

    /**
      Renders the state into the page
     */
    renderStateTable = () => {
      const tableData = {
        headers: [
          "ID",
          "Name", "Brand", "Category", "Quantity", "Size", "Expiry Data",
          "Main Ingredients", "Allergens", "From Donor"
        ],
        data: state.inventory.items
      }
      const tableNode = UiFactory && UiFactory.createTable(tableData)
      const el = document.getElementById("dataTarget")
      el.innerHTML = ""
      el.appendChild(tableNode)
    }

    /**
      Refreshes inventory records from the server
     */
    refreshRecords = async (done) => {
      await fetch("/search", {
        method: "POST",
        headers: new Headers({
          "content-type": "application/json"
        }),
        body: JSON.stringify({ context: "item" })
      })
        .then((response) => {
          if (response.status == 401) { throw new Error("Invalid credentials"); }
          if (response.status != 200) { throw new Error("Bad Server Response"); }
          return response.json();
        })
        .then((json) => {
          if (("error" in json) && json.error != undefined) {
            throw new Error(json.error);
          }
          // Clear state
          this.items = [];

          // Add
          json.map((row) => {
            this.addInventory(new Inventory(row));
          });

          // Render the table
          this.renderStateTable();
        })
        .catch((error) => {
          alert(error);
        })
        .finally(() => {
          done && done();
        })
    }

    /**
      Refreshes inventory categories from the server
      @param {function} done - Call back once the fetch promise is complete.
     */
    refreshCategories = async (done) => {
      await fetch("/search", {
        method: "POST",
        headers: new Headers({
          "content-type": "application/json"
        }),
        body: JSON.stringify({ context: "category" })
      })
        .then((response) => {
          if (response.status == 401) { throw new Error("Invalid credentials"); }
          if (response.status != 200) { throw new Error("Bad Server Response"); }
          return response.json();
        })
        .then((json) => {
          if (("error" in json) && json.error != undefined) {
            throw new Error(json.error);
          }
          // Set categories to those returned from server
          this.categories = json;

          console.log("categories updated");
        })
        .catch((error) => {
          alert(error);
        })
        .finally(() => {
          done && done();
        });
    }
    /**
      Refreshes inventory categories from the server
      @param {function} done - Call back once the fetch promise is complete.
     */
    refreshDonors = async (done) => {
      await fetch("/search", {
        method: "POST",
        headers: new Headers({
          "content-type": "application/json"
        }),
        body: JSON.stringify({ context: "aid_donors" })
      })
        .then((response) => {
          if (response.status == 401) { throw new Error("Invalid credentials"); }
          if (response.status != 200) { throw new Error("Bad Server Response"); }
          return response.json();
        })
        .then((json) => {
          if (("error" in json) && json.error != undefined) {
            throw new Error(json.error);
          }
          // Set donors to those returned from server
          this.donors = json;

          console.log("donors updated");
        })
        .catch((error) => {
          alert(error);
        })
        .finally(() => {
          done && done();
        });
    }

  }

  /** State of aidRecipients in the system */
  state.inventory = new InventoryState()

  /**
    Retrieves all child `input` elements of a given element by its `id`
    @param {String} id - ID of the target element.
    @return {Array} An array of `input` elements.
   */
  const getFormInputsById = (id) => {
    const formElements = [
        ...document
          .getElementById(id)
          // .getElementsByTagName("input")
          .querySelectorAll("input,select") // Get both input and select
    ];
    return formElements;
  }

  /**
   Validates a form of given `id` by checking all required elements have
  values.

  @param {String} id - ID of the target element.
  @return {Boolean} `true` if valid.
  */
  const validateForm = (id) => {
    const formElements = getFormInputsById(id);
    if (!formElements) {
      console.error(`Could not valid form with id ${formElements}`)
    }

    const isValid = formElements.reduce((state, inputEl) => {
      // If false, remain false
      if (state == false) {
        return false;
      }

      // If required and not filled, apply false
      if (inputEl.required && inputEl.value == "") {
        console.log(inputEl, inputEl.value)
        return false;
      }

      return true;
    }, true);
    return isValid;
  }

  /**
   Submits data to the API endpoint to create an aid recipient
  */
  const onCreateInventory = () => {
    const formId = "modalForm";

    // Get form elements as an array
    const formElements = getFormInputsById(formId);

    // Check that all required elements have values
    const isValid = validateForm(formId);

    if (!isValid) {
      alert("Please enter all required information.");
      return;
    }

    // Get data from form fields
    const formData = formElements.reduce((inputVals, inputEl) => {
      const field = inputEl.getAttribute("name");
      let value = inputEl.value;
      if (value != undefined) {
        if (inputEl.type == "number" || field == "category_id") {
          value = parseFloat(value);
        }
        inputVals[field] = value;
      }
      return inputVals;
    }, {})

    // Generate a request to the API
    fetch("/inventory", {
        method: "POST",
        headers: new Headers({
          "content-type": "application/json"
        }),
        body: JSON.stringify(formData)
      }
    )
    .then((response) => {
      if (response.status == 401) { throw new Error("Invalid credentials"); }
      if (response.status != 200) { throw new Error("Bad Server Response"); }
      return response.json();
    })
    .then((json) => {
      if (("error" in json) && json.error != undefined) {
        throw new Error(json.error);
      }

      // Close the modal
      document.getElementById("modalDismiss").click();

      // Additional behaviour after success
      console.log(json)
      alert("Success!")

      // Refresh the inventory list
      state.inventory.refreshRecords();

      return json;
    })
    .catch((error) => {
      alert(error);
      return [];
    })
    .finally((json) => {
      // TODO
      // Additional behaviour if required
      return json
    });
  }

  /**
   Submits data to the API endpoint to create category
  */
  const onCreateCategory = () => {
    const formId = "modalForm";

    // Get form elements as an array
    const formElements = getFormInputsById(formId);

    // Check that all required elements have values
    const isValid = validateForm(formId);

    if (!isValid) {
      alert("Please enter all required information.");
      return;
    }

    // Get data from form fields
    const formData = formElements.reduce((inputVals, inputEl) => {
      const field = inputEl.getAttribute("name");
      let value = inputEl.value;
      if (value != undefined) {
        if (inputEl.type == "number") {
          value = parseFloat(value);
        }
        inputVals[field] = value;
      }
      return inputVals;
    }, {})

    // Generate a request to the API
    fetch("/aid_category", {
        method: "POST",
        headers: new Headers({
          "content-type": "application/json"
        }),
        body: JSON.stringify(formData)
      }
    )
    .then((response) => {
      if (response.status == 401) { throw new Error("Invalid credentials"); }
      if (response.status != 200) { throw new Error("Bad Server Response"); }
      return response.json();
    })
    .then((json) => {
      if (("error" in json) && json.error != undefined) {
        throw new Error(json.error);
      }

      // Close the modal
      document.getElementById("modalDismiss").click();

      // Additional behaviour after success
      console.log(json)
      alert("Success!")

      return json;
    })
    .catch((error) => {
      alert(error);
      return [];
    })
    .finally((json) => {
      // Update the category list from server
      state.inventory.refreshCategories();
    });
  }
})()