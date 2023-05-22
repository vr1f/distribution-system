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

  /**
    Representing info a kit item, this should match `items.py`
   */
  class Kit {
    constructor(params) {
      const {
        aid_kit_id = undefined,
        aidkit_name,
        aidkit_description
      } = params
      this.aid_kit_id = aid_kit_id;
      this.aidkit_name = aidkit_name;
      this.aidkit_description = aidkit_description;
    }
  }

  class KitsState {
    constructor() {
      this.aidKits = []

      window.dispatchEvent(new CustomEvent("app.register.callback", {
        detail: {
          eventName: "aid_kit.add",
          callback: this.showKitModal.bind(this)
        }
      }));

    }

    addKit(aidKit) {
      this.aidKits.push(aidKit);
    }

    showKitModal(modalElements) {
      // alert("To implement")
      const {
        modalHeading,
        modalBody,
        modalAction
      } = modalElements

      // Heading
      modalHeading.innerHTML = "Add aid kit";

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
      });
    }

  /**
    Run on load
   */
  window.addEventListener("load", () => {
    console.log("kit.js")
  })
})()