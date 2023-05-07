/**
  Methods relating to the base html
 */
(() => {
  const overwriteCookie = () => {
    const currTime = new Date().getTime();
    const currUTC = new Date(currTime).toUTCString();
    document.cookie =`token=; expires=${currUTC}`;
  }

  const bindButtonActions = () => {
    document.getElementById("log-out").addEventListener("click", logout);
  }

  const logout = () => {
    overwriteCookie();
  }
  /**
  Run on load
  */
  window.addEventListener("load", () => {
    bindButtonActions();
  })

})()