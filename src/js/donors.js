/**
  Methods relating to recipient functionality
 */
"use strict";

(() => {

  console.log("loaded donors")

  /** The state for this page */
  const state = {}

  /** Templates for various elements */
  state.template = {}
  state.template.addRecipientFormElements = [
    {
      label: "First name", placeholder: "Enter first name", required: true,
      name:"first_name"
    },
    {
      label: "Last name", placeholder: "Enter last name (optional)",
      name: "last_name"
    },
    {
      label: "Mailing Address", placeholder: "Enter address (optional)",
      name: "address"
    },
    {
      label: "Phone number", placeholder: "",
      name: "phone", type: "tel"
    },
    {
      label: "Email", placeholder: "Enter email address", required: true,
      name: "email"
    },
    {
      label: "Preferred mode of communication",
      placeholder: "Enter either email or phone",
      name: "communication_mode",
      required: true
    }
  ];

  /**
    Representing info for a person, this should match `donors.py`
    @todo Match this with donors.py once it is complete
   */
  class AidDonor {
    constructor(params) {
      const {
        id = undefined,
        first_name,
        last_name = "NO_LAST_NAME",
        address = "NO_KNOWN_ADDRESS",
        phone = "",
        email,
        communication_mode
      } = params
      this.id = id;
      this.first_name = first_name;
      this.last_name = last_name;
      this.address = address;
      this.phone = phone;
      this.email = email;
      this.communication_mode = communication_mode;
    }
  }

  class AidDonorsState {
    constructor() {
      this.aidDonors = []

      window.dispatchEvent(new CustomEvent("app.register.callback", {
        detail: {
          eventName: "donor.add",
          callback: this.showDonorModal.bind(this)
        }
      }));
    }

    addDonor(aidDonor) {
      this.aidDonors.push(aidDonor);
    }

    updateDonor(id, aidRecipient) {
      alert("To implement");
    }

    deleteDonor(id) {
      alert("To implement");
    }

    showDonorModal(modalElements) {
      // alert("To implement")
      const {
        modalHeading,
        modalBody,
        modalAction
      } = modalElements

      // Heading
      modalHeading.innerHTML = "Add new donor";

      // Form elements in the body
      const inputForm = window.UiFactory.createModalForm(
        state.template.addRecipientFormElements
      )
      modalBody.innerHTML = ""
      modalBody.appendChild(inputForm)

      // Submit button
      modalAction.innerHTML = "Submit";
      modalAction.addEventListener("click", onCreateDonor)

    }
  }

  /** State of aidRecipients in the system */
  state.aidDonor = new AidDonorsState()

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
              "ID", "First Name", "Last Name", "Address", "Phone", "Email",
              "Mode of Communication"
            ], data: state.aidDonor.aidDonors
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
  const onCreateDonor = () => {
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
    fetch("/aid_donor", {
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
    state.aidDonor.addDonor(
      new AidDonor({
        first_name: "foo", last_name: "bar", address: "101 Rescue Lane",
        phone: "+61 3 9035 5511", email: "hello@world.com", communication_mode: "email"
      })
    )
    state.aidDonor.addDonor(
      new AidDonor({
        first_name: "John", last_name: "Doe", address: "102 Rescue Lane",
        phone: "+61 3 9035 5511", communication_mode: "phone"
      })
    )

    console.log(state)
  })
})()