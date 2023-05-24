/**
  Methods relating to aid kits
 */
"use strict";

(() => {

  console.log("loaded kits")

  /** The state for this page */
  const state = {}

  /** Templates for various elements */
  state.template = {}
  state.template.addAidKitFormElements = [
    {
      label: "Kit Name", placeholder: "Enter aid kit name",
      name: "aidkit_name", required: true
    },
    {
      label: "Kit Description", placeholder: "Enter aid kit description",
      name: "aidkit_description", required: true
    }
  ]

  state.template.editAidKitFormElements = [
    {
      type: "select", name: "aid_kit_id", required: true,
      options: [], label: "Kit"
    },
    {
      type: "select", name: "item_id", required: true,
      options: [], label: "Item"
    },
    {
      label: "Quantity", placeholder: "Enter Quantity",
      name: "quantity", type: "number", step: 1, min: 1, required: true
    }
  ]

  class KitsState {
    constructor() {
      this.aidKits = [];
      this.aidKitItems = [];
      this.items = [];

      window.dispatchEvent(new CustomEvent("app.register.callback", {
        detail: {
          eventName: "aid_kit.add",
          callback: this.showKitModal.bind(this)
        }
      }));
      window.dispatchEvent(new CustomEvent("app.register.callback", {
        detail: {
          eventName: "aid_kit.edit",
          callback: this.showEditKitModal.bind(this)
        }
      }));

      new Promise((resolve, reject) => {
        this.refreshKits(resolve);
      })
      .then(() => {
        this.refreshItems();
      });
    }

    showKitModal(modalElements) {
      const {
        modalHeading,
        modalBody,
        modalAction
      } = modalElements

      // Heading
      modalHeading.innerHTML = "Edit aid kit";

      // Form elements in the body
      const inputForm = window.UiFactory.createModalForm(
        state.template.addAidKitFormElements
      )
      modalBody.innerHTML = ""
      modalBody.appendChild(inputForm)

      // Submit button
      modalAction.innerHTML = "Submit";
      modalAction.addEventListener("click", onCreateKit)
    }

    showEditKitModal(modalElements) {
      const {
        modalHeading,
        modalBody,
        modalAction
      } = modalElements

      // Heading
      modalHeading.innerHTML = "Add an Item to a Kit";

      // Form elements in the body
      const inputForm = window.UiFactory.createModalForm(
        state.template.editAidKitFormElements.map((element) => {
          // Map aid kits to selector
          if (element.name == "aid_kit_id") {
            element.options = this.aidKits.map((aidKit) => {
              return {
                name: aidKit.aidkit_name,
                value: aidKit.aid_kit_id
              }
            });
          }
          // Map items to selector
          if (element.name == "item_id") {
            element.options = this.items.map((item) => {
              return {
                name: item.item_name,
                value: item.item_id
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
      modalAction.addEventListener("click", onEditKit)
    }

    refreshKits = async (done) => {
      await fetch("/search", {
        method: "POST",
        headers: new Headers({
          "content-type": "application/json"
        }),
        body: JSON.stringify({ context: "aid_kits" })
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

          this.aidKits = json;

          console.log("kits updated");
        })
        .catch((error) => {
          alert(error);
        })
        .finally(() => {
          done && done();
        });
    }

    refreshItems = async (done) => {
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
          // Set categories to those returned from server
          this.items = json;

          console.log("items updated");
        })
        .catch((error) => {
          alert(error);
        })
        .finally(() => {
          done && done();
        });
    }
  }

  /** State of aidKits in the system */
  state.aidKit = new KitsState()

  /**
    Retrieves all child `input` elements of a given element by its `id`
    @param {String} id - ID of the target element.
    @return {Array} An array of `input` elements.
   */
  const getFormInputsById = (id) => {
    const formElements = [
      ...document
        .getElementById(id)
        .querySelectorAll("input,select")
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
     Submits data to the API endpoint to create kit
    */
  const onCreateKit = () => {
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
    fetch("/aid_kit", {
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

      state.aidKit.refreshKits();

      // Close the modal
      document.getElementById("modalDismiss").click();

      alert("Success!")

      return json;
    })
    .catch((error) => {
      alert(error);
      return [];
    });
  }

  const onEditKit = () => {
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
        if (inputEl.type == "number" || field == "item_id" || field == "aid_kit_id") {
          value = parseFloat(value);
        }
        inputVals[field] = value;
      }
      return inputVals;
    }, {})
    // Generate a request to the API
    fetch("/aid_kit", {
      method: "PUT",
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
      alert("Success!")

      return json;
    })
    .catch((error) => {
      alert(error);
      return [];
    });
  }

  /**
    Run on load
   */
  window.addEventListener("load", () => {
    console.log("kit.js")
  })
})()