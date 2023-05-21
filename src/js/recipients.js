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
      label: "Family Size", placeholder: "Number in family (optional)",
      name: "n_family", type: "number"
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
      name: "document_id", id: "document_id", type: "number", hidden: true
    },
    {
      label: "Upload Documents", id: "id_images",
      type: "file", multiple:"multiple"
    }

  ];

  /**
    Representing info for a person, this should match `recipients.py`
   */
  class Person {
    constructor(params) {
      const {
        person_id = undefined,
        first_name,
        last_name = "NO_LAST_NAME",
        age,
        nationality = undefined,
        id_no = undefined,
        id_expiry = undefined,
        document_id = undefined,
      } = params
      this.person_id = person_id;
      this.first_name = first_name;
      this.last_name = last_name;
      this.age = age;
      this.nationality = nationality;
      this.id_no = id_no;
      this.id_expiry = id_expiry;
      this.document_id = document_id;
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

      this.refreshRecords()
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
          "ID",
          "First Name", "Last Name", "Age",
          "Nationality", "ID Number", "ID Expiry", "ID Doc",
          "Address", "Family Size", "Partner", "Dependents"
        ],
        data: state.aidRecipient.aidRecipients
      }
      const tableNode = UiFactory && UiFactory.createTable(tableData)
      const el = document.getElementById("dataTarget")
      el.innerHTML = ""
      el.appendChild(tableNode)
    }

    /**
      Refreshes records from the server database
     */
    refreshRecords = async () => {
      await fetch ("/search", {
        method: "POST",
        headers: new Headers({
          "content-type": "application/json"
        }),
        body: JSON.stringify({context: "aid_recipients"})
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
        this.aidRecipients = [];

        // Add
        json.map((row) => {
          this.addRecipient(new AidRecipient(row));
        });

        // Render the table
        this.renderStateTable();
      })
      .catch((error) => {
        alert(error);
      })
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
    return await fetch("/aid_recipient", {
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
      // alert("Success!")
      // console.log(json);

      // Refresh the displayed table
      state.aidRecipient.refreshRecords();

      // Close the modal
      document.getElementById("modalDismiss").click();

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


  // Uploads file to API endpoint
  const uploadFiles = async (files) => {
    return await fetch("/id_img", {
      method: "POST",
      body: files
    })
    .then((response) => {
      if (!response.ok) {
        throw new Error("Unable to upload file!");
      }
      return response.json();
    })
    .catch((error) => {
      alert(error.message);
      return {id: undefined}
    });
  }

  /**
   Submits data to the API endpoint to create an aid recipient
  */
  const onCreateRecipient = () => {

    // Use a promise to first upload files if any
    // then retrieve the file id to set as the "document_id" field
    new Promise((resolve, reject) => {
      // Check the file selector
      const fileSelector = document.getElementById("id_images");
      const docIdField = document.getElementById("document_id");

      // Resolve immediately if docIdField has already been filled
      // or if there are no files in the fileSelector
      if (docIdField.value != "" || fileSelector.value == "") {
        return resolve();
      }

      // Generate FormData to upload the files to the server
      const files = new FormData();
      for (const file of fileSelector.files) {
        files.append("files", file);
      }

      // Upload the files by querying the endpoint
      uploadFiles(files)
      .then((json) => {
        // Get the document_id from the endpoint response
        const { id: document_id } = json;

        // Reject if document_id is undefined
        (!document_id) && reject("Could not upload files.");

        // Set the document_id
        document.getElementById("document_id").value = document_id;

        resolve();
      });
    })
    .then(() => {
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
        let { value } = inputEl;

        if (field && value != undefined) {
          if (inputEl.type == "number") {
            value = parseFloat(value);
          }
          inputVals[field] = value;
        }
        return inputVals;
      }, {})

      // Add data to server database
      return fetchForm(formData);
    })
    .catch((error) => {
      alert("Failed to add new recipient.");
    });

    return;

  }

  /**
    Run on load
   */
  window.addEventListener("load", () => {
    console.log("recipients.js")
  })
})()