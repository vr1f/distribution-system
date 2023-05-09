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
      name:"name", required: true
    },
    {
      label: "Brand", placeholder: "Enter Brand (optional)",
      name: "brand"
    },
    {
      label: "TODO Category", placeholder: "TODO, SELECT CATEGORY",
      name: "category", required: true
    },
    {
      label: "Quantity", placeholder: "Enter Quantity",
      name: "quantity", type: "number", required: true
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
      name: "main_ingredients"
    },
    {
      label: "Allergens", placeholder: "Enter any allergens (optional)",
      name: "allergens"
    },
  ];

  /**
    Representing info an inventory item, this should match `inventory.py`
    @todo Match this with inventory.py once it is complete
   */
  class Inventory {
    constructor(params) {
      const {
        id = undefined,
        name,
        brand = "",
        category, //TODO
        quantity,
        size = "",
        expiry_date = "",
        main_ingredients = "",
        allergens = "",
      } = params
      this.id = id;
      this.name = name;
      this.brand = brand;
      this.category = category;
      this.quantity = quantity;
      this.size = size;
      this.expiry_date = expiry_date;
      this.main_ingredients = main_ingredients;
      this.allergens = allergens;
    }
  }

  class InventoryState {
    constructor() {
      this.items = []

      window.dispatchEvent(new CustomEvent("app.register.callback", {
        detail: {
          eventName: "inventory.add",
          callback: this.showInventoryModal.bind(this)
        }
      }));
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
        state.template.addInventoryFormElements
      )
      modalBody.innerHTML = ""
      modalBody.appendChild(inputForm)

      // Submit button
      modalAction.innerHTML = "Submit";
      modalAction.addEventListener("click", onCreateInventory)

    }
  }

  /** State of aidRecipients in the system */
  state.inventory = new InventoryState()

  /**
    Adds event listeners to various DOM elements
   */
  const addEventListeners = () => {
    /** @debug */
    document
      .getElementById("testFactory")
      .addEventListener("click", () => {
        const testData = {
          headers: [
              "ID", "Name", "Brand", "Category", "Quantity", "Size",
              "Expiry Date", "Main Ingredients", "Allergens"
            ], data: state.inventory.items
        }
        const tableNode = UiFactory && UiFactory.createTable(testData)
        const el = document.getElementById("factoryTarget")
        el.innerHTML = ""
        el.appendChild(tableNode)
      })
    ;
  }

  /**
    Retrieves all child `input` elements of a given element by its `id`
    @param {String} id - ID of the target element.
    @return {Array} An array of `input` elements.
   */
  const getFormInputsById = (id) => {
    const formElements = [
        ...document
          .getElementById(id)
          .getElementsByTagName("input")
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
        if (inputEl.type == "number") {
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

      // TODO
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
      // TODO
      // Additional behaviour if required
      return json
    });
  }

  /**
    Run on load
   */
  window.addEventListener("load", () => {

    addEventListeners();

    /**
      @debug Dummy state
     */
    state.inventory.addInventory(
      new Inventory({
        name: "Spam", category: "Canned Food", quantity: 5
      })
    )
    state.inventory.addInventory(
      new Inventory({
        name: "Mee Goreng", category: "Instant Noodles", quantity: 8
      })
    )

    console.log(state)
  })
})()