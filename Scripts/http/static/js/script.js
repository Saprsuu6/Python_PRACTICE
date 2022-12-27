alert("Hello world");

document.addEventListener("DOMContentLoaded", () => {
  var token = window.sessionStorage.getItem("access_token");
  console.log(token);

  if (token == null) {
    const loginButton = document.querySelector("#login-button");
    if (!loginButton) throw "DOMContentLoaded: #login-button not found";
    loginButton.addEventListener("click", loginButtonClick);
  } else {
    hide_auth();
  }

  const itemsButton = document.querySelector("#items-button");
  if (!itemsButton) throw "DOMContentLoaded: #items-button not found";
  itemsButton.addEventListener("click", itemsButtonClick);
});
function hide_auth() {
  var div = document.querySelector("#top_form");
  div.style.display = "none";
}
function itemsButtonClick(e) {
  var access_token = window.sessionStorage.getItem("access_token");
  var term = new Date(window.sessionStorage.getItem("expires_in"));
  if (!access_token) {
    alert("Сначала авторизуйтесь");
    return;
  }
  if (new Date() >= term) {
    alert("Срок действия токена истёк");
  } else {
    fetch("/items", {
      method: "GET",
      headers: {
        Authorization: "Bearer " + access_token,
      },
    }).then(async (r) => {
      if (r.status == 401) {
        alert(await r.text());
        // проверка токена отклонена - удалить токен из хранилища
      } else if (r.status == 200) {
        out.innerText = await r.text();
      } else {
        console.log(r);
      }
    });
  }
}
function loginButtonClick(e) {
  const userLogin = document.querySelector("#user-login");
  if (!userLogin) throw "loginButtonClick: #user-login not found";
  const userPassword = document.querySelector("#user-password");
  if (!userPassword) throw "loginButtonClick: #user-password not found";
  // проверить поля на пустоту, логин - на допустимые символы
  const credentials = btoa(userLogin.value + ":" + userPassword.value);
  fetch("/auth", {
    method: "GET",
    headers: {
      Authorization: "Basic " + credentials,
    },
  }).then((r) => {
    if (r.status != 200) {
      alert("Логин или пароль неправильные");
    } else {
      r.json().then((j) => {
        console.log(j);
        // сохраняем полученный токен
        window.sessionStorage.setItem("access_token", j.access_token);
        window.sessionStorage.setItem("expires_in", j.expires_in);
      });
    }
  });
}
