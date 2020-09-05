function goback() {
  window.history.back();
}

function goToMe() {
  window.location.href = 'me';
}

function goToHome() {
  window.location.href = 'home';
}

const tx = document.getElementsByTagName('textarea');
for (let i = 0; i < tx.length; i++) {
  tx[i].setAttribute('style', 'height:' + (tx[i].scrollHeight) + 'px;overflow-y:hidden;');
  tx[i].addEventListener("input", OnInput, false);
}

function OnInput() {
  this.style.height = 'auto';
  this.style.height = (this.scrollHeight) + 'px';
}


function goRegister() {
  window.location.href = 'register';
}

function goLogin() {
  window.location.href = 'login';
}
