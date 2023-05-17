/**
  Methods relating to recipient functionality
 */
"use strict";

(() => {

  console.log("loaded recipients")

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
      label: "Enter age", placeholder: "Enter age", required: true,
      name: "age", type: "number"
    },
    {
      label: "Address", placeholder: "Enter address (optional)",
      name: "address"
    },
    {
      label: "Famly Size", placeholder: "Number in family (optional)",
      name: "n_family"
    },
    {
      label: "Partner", placeholder: "Enter partner details (optional)",
      name: "common_law_partner"
    },
    {
      label: "Dependents", placeholder: "Enter dependents details (optional)",
      name: "dependents"
    },
    {
      label: "Nationality", placeholder: "Enter nationality (optional)",
      name: "nationality"
    },
    {
      label: "ID No.", placeholder: "Enter ID no. (optional)",
      name: "id_no"
    },
    {
      label: "ID Expiry", placeholder: "Enter ID expiry date (optional)",
      name: "id_expiry", type: "date"
    },
    {
      label: "Upload Documents", id: "file",
      name: "file", type: "file", multiple:"multiple"
    }

  ];

  /**
    Representing info for a person, this should match `recipients.py`
   */
  class Person {
    constructor(params) {
      const {
        // id = undefined,
        first_name,
        last_name = "NO_LAST_NAME",
        age,
        nationality = "",
        id_no = "",
        id_expiry = ""
      } = params
      // this.id = id;
      this.first_name = first_name;
      this.last_name = last_name;
      this.age = age;
      this.nationality = nationality;
      this.id_no = id_no;
      this.id_expiry = id_expiry;
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
        n_family = 1,
        common_law_partner = "",
        dependents = "",
      } = params
      this.address = address;
      this.n_family = n_family;
      this.common_law_partner = common_law_partner;
      this.dependents = dependents;
    }
  }

  class AidRecipientsState {
    constructor() {
      this.aidRecipients = []

      window.dispatchEvent(new CustomEvent("app.register.callback", {
        detail: {
          eventName: "recipient.add",
          callback: this.showRecipientModal.bind(this)
        }
      }));
    }

    addRecipient(aidRecipient) {
      this.aidRecipients.push(aidRecipient);
      this.renderStateTable();
    }

    updateRecipient(id, aidRecipient) {
      alert("To implement");
    }

    deleteRecipient(id) {
      alert("To implement");
    }

    showRecipientModal(modalElements) {
      // alert("To implement")
      const {
        modalHeading,
        modalBody,
        modalAction
      } = modalElements

      // Heading
      modalHeading.innerHTML = "Add new recipient";

      // Form elements in the body
      const inputForm = window.UiFactory.createModalForm(
        state.template.addRecipientFormElements
      )
      modalBody.innerHTML = ""
      modalBody.appendChild(inputForm)

      // Submit button
      modalAction.innerHTML = "Submit";
      modalAction.addEventListener("click", onCreateRecipient)

    }

    /**
      Renders the state into the page
     */
    renderStateTable = () => {
      const tableData = {
        headers: [
          // "ID",
          "First Name", "Last Name", "Age",
          "Nationality", "ID Number", "ID Expiry",
          "Address", "Family Size", "Partner", "Dependents"
        ],
        data: state.aidRecipient.aidRecipients
      }
      const tableNode = UiFactory && UiFactory.createTable(tableData)
      const el = document.getElementById("dataTarget")
      el.innerHTML = ""
      el.appendChild(tableNode)
    }
  }

  /** State of aidRecipients in the system */
  state.aidRecipient = new AidRecipientsState()

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

  // Sends aid recipient form data to API endpoint
  const fetchForm = async (formData) => {
     await fetch("/aid_recipient", {
      method: "POST",
      headers: new Headers({
        "content-type": "application/json"
      }),
      body: JSON.stringify(formData)
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

      // TODO
      // Additional behaviour after success
      //console.log(json)
      alert("Success!")
      console.log(json);
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
    })
  }


  // Uploads file to API endpoint and adds the file ID (returned from API) to the form data
  // TO DO: Test again after backend completed
  // TO DO: Add file_id field to Person
  const fetchFile = async (files, formData) => {
    await fetch("/aid_recipient", {
      method: "POST",
      body: files
    })
    .then((response) => {
      // TO DO: Change status no. accordingly when backend is completed
      if (response.status != 201) {
        throw new Error("Unable to upload file!");
      }
      return response.json();
    })
    .then((json) => {
      // gets the file ID from API and adds to form data
      formData["file_id"] =  json.file_id;
      return json;
    })
    .catch((error) => {
      alert(error.message);
    })
  }

  /**
   Submits data to the API endpoint to create an aid recipient
  */
  const onCreateRecipient = () => {
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
    var formData = formElements.reduce((inputVals, inputEl) => {
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

    const newRecipient = new AidRecipient(formData)
    state.aidRecipient.addRecipient(newRecipient)

    // Close the modal
    document.getElementById("modalDismiss").click()

    // Directly render to table while backend is being completed.
    return;

    // Check if user uploaded any files
    if (document.getElementById("file").value != "") {
      // If files present
      var files = new FormData();
      for (const file of document.getElementById("file").files) {
        files.append("file", file);
      }
      // Upload file to DB and add linking file ID key to recipient form
      fetchFile(files, formData);
    }
    fetchForm(formData);
  }

  /**
    Run on load
   */
  window.addEventListener("load", () => {
    console.log("recipients.js")

    /**
      @debug Dummy state
     */
    state.aidRecipient.addRecipient(
      new AidRecipient({
        // id: 1,
        first_name: "Jim", last_name: "Raynor", age: 32, n_family: 2,
        address: "101 Raiders Way, Sunshine, VIC, 3020",
        common_law_partner: "Kerrigan (Age 28)",
        dependents: "",
        nationality: "Australian", id_no: "102432", id_expiry: "31/12/2023"
      })
    )
    state.aidRecipient.addRecipient(
      new AidRecipient({
        // id: 1,
        first_name: "Rick", last_name: "Sanchez", age: 70, n_family: 2,
        address: "56 Sunset Blvd, Brighton, VIC, 3186",
        common_law_partner: "",
        dependents: "Morty Smith (Age 14)",
        nationality: "Australian", id_no: "124352", id_expiry: "31/12/2023"
      })
    )

    console.log(state)
  })
})()