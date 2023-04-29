/**
  Methods relating to recipient functionality
 */
"use strict";

(() => {

  /**
    Representing info for a person, this should match `recipients.py`
   */
  class Person {
    constructor(params) {
      const {
        id = undefined,
        first_name,
        last_name = "NO_LAST_NAME",
        age
      } = params
      this.id = id;
      this.first_name = first_name;
      this.last_name = last_name;
      this.age = age;
    }
  }

  /**
    Representing infor for a AidRecipient, this should match `recipients.py`
   */
  class AidRecipient extends Person {
    constructor(params) {
      super(params)
      const {
        address = "NO_KNOWN_ADDRESS",
        common_law_partner = undefined,
        dependents = []
      } = params
      this.address = address;
      this.common_law_partner = common_law_partner;
      this.dependents = dependents;
    }
  }

  class AidRecipientsState {
    constructor() {
      this.aidRecipients = []
    }

    addRecipient(aidRecipient) {
      this.aidRecipients.push(aidRecipient);
    }

    updateRecipient(id, aidRecipient) {
      alert("To implement");
    }

    deleteRecipient(id) {
      alert("To implement");
    }

    showRecipientModal(event) {
      // alert("To implement")

      const modal = document.getElementById("modal");
      const modalHeading = document.getElementById("modalHeading");
      const modalBody = document.getElementById("modalBody");
      const modalAction = document.getElementById("modalAction");

      modalHeading.innerHTML = "Add new recipient";
      modalAction.innerHTML = "Submit";

      const bodyWrapper = document.createElement("div");

      const inputWrapper = document.createElement("div")
      inputWrapper.innerHTML = "Hello World"
      bodyWrapper.appendChild(inputWrapper)

      modalBody.replaceWith(bodyWrapper)
    }
  }

  /** The state for this page */
  const state = {}

  /** State of aidRecipients in the system */
  state.aidRecipient = new AidRecipientsState()

  /**
    Adds event listeners to various DOM elements
   */
  const addEventListeners = () => {
    document
      .getElementById("createRecipient")
      .addEventListener("click", onCreateRecipient)
    ;

    document
      .getElementById("modal")
      .addEventListener("show.bs.modal", state.aidRecipient.showRecipientModal)
    ;
  }

  const onShowRecipientModal = () => {
    alert("To implement")
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
    const isValid = formElements.reduce((state, inputEl) => {
      // If false, remain false
      if (state == false) {
        return false;
      }

      // If required and not filled, apply false
      if (inputEl.required && inputEl.value == "") {
        return false;
      }

      return true;
    }, true);
    return isValid;
  }

  /**
    Submits data to the API endpoint to create an aid recipient
   */
  const onCreateRecipient = () => {
    // alert("To implement")

    const formId = "newRecipientForm";

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
    const responseJson = fetch("/aid_recipient", {
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

    // TODO
    // Additional behaviour after success
    console.log(responseJson)
    alert("Success!")
  }

  /**
    Run on load
   */
  window.onload = () => {
    addEventListeners();

    /**
      @debug
     */
    state.aidRecipient.addRecipient(
      new AidRecipient({first_name: "foo", age: 25})
    )

    console.log(state)
  }

})()