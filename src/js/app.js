/**
  Control center for the app through interactions via CustomEvents.
  Maintains modal state and resets when modal closes.

  @event app.register.callback - Registers a callback with the an event name
    by receiving event.detail.eventName and event.detail.callback.
 */
"use strict";

(() => {
  class App {
    constructor() {
      // State components
      this.state = {};
      this.callbacks = {};

      // Initialises event handlers
      this.init();

      // Modal state
      this.state.modalContext = undefined;

      console.log("loaded app");
    }

    init() {
      // Open modal
      document.getElementById("modal")
      .addEventListener("show.bs.modal", this.onModalOpen.bind(this));

      // Open modal
      document.getElementById("modal")
      .addEventListener("hide.bs.modal", this.onModalHide.bind(this));

      // Register a callback
      window.addEventListener(
        "app.register.callback", this.registerCallback.bind(this)
      )
    }

    registerCallback(event) {
      try {
        const{ detail: { eventName, callback } } = event;
        this.callbacks[eventName] = callback;
        console.log(this.callbacks)
      } catch(e) {
        console.error("Could not register callback")
      }
    }

    getModalElements() {
      const modal = document.getElementById("modal");
      const modalHeading = document.getElementById("modalHeading");
      const modalBody = document.getElementById("modalBody");
      const modalAction = document.getElementById("modalAction");

      return { modal, modalHeading, modalBody, modalAction }
    }

    resetModalElements() {
      const {
        modalHeading,
        modalBody,
        modalAction
      } = this.getModalElements();

      modalHeading.innerHTML = "id:modalHeading";
      modalBody.innerHTML = "id:modalBody";
      modalAction.innerHTML = "id:modalAction";
      const modalActionNoEvents = modalAction.cloneNode(true)
      modalAction.replaceWith(modalActionNoEvents)
    }

    onModalOpen(event) {
      const { relatedTarget } = event;
      const action = relatedTarget.getAttribute("app-action")
      if (action in this.callbacks) {
        this.state.modalContext = action;
        this.callbacks[action](this.getModalElements());
      } else {
        this.onModalHide();
        console.error(`Unrecognised callback: ${action}`)
      }
    }

    onModalHide(event) {
      this.state.modalOpen = undefined;
      this.resetModalElements();
    }
  }

  new App()
})()