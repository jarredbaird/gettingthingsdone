import { NavBar } from "./modules/nav-bar.js";
import { InputBox } from "./modules/input-box.js";
import { ListGroup } from "./modules/list-group.js";
import { ListGroupItem } from "./modules/list-group-item.js";
import { SignInSignUp } from "./modules/signin-signup.js";

/* DOM Rendering */

let navBar = new NavBar();
navBar.makeNavbar($("body"));

$("#logout").on("click", async function () {
  await fetch("/logout");
  $("#main-grid").empty();
  await userFlow();
});

await userFlow();

let socket = io();
socket.on("my_response", function (msg, cb) {
  let nonDOMitem = new ListGroupItem(msg);
  console.log(nonDOMitem.makeItem());
  $("#inbox-list").prepend(nonDOMitem.makeItem());
  if (cb) cb();
});

async function userFlow() {
  let userSession = await getSession();
  if (userSession) {
    await showUserInbox();
  } else {
    let buttons = new SignInSignUp();
    $("#main-grid").append(
      $("<div>")
        .addClass("input-group input-group-lg")
        .append(buttons.$signUpBtn, buttons.$signInBtn)
    );
    buttons.$signUpBtn.on("click", function () {
      $("#main-grid").empty();
      $("#main-grid").append(
        $("<h2>").text("Sign Up"),
        $("<form>")
          .addClass("row g-3")
          .append(
            $("<div>")
              .addClass("input-group input-group-lg")
              .append(
                $("<input>").addClass("form-control").attr({
                  type: "text",
                  placeholder: "Username",
                  id: "username",
                }),
                $("<input>").addClass("form-control").attr({
                  type: "text",
                  placeholder: "Password",
                  id: "password",
                }),
                $("<button>")
                  .addClass("btn btn-primary")
                  .text("Submit")
                  .on("click", async function (event) {
                    event.preventDefault();
                    let response = await createUser(
                      $("#username").val(),
                      $("#password").val()
                    );
                    debugger;
                    if (!response.message) {
                      $("#main-grid").empty();
                      await showUserInbox();
                    } else {
                      $("#main-grid").empty();
                      await userFlow();
                    }
                  })
              )
          )
      );
    });
    buttons.$signInBtn.on("click", function () {
      $("#main-grid").empty();
      $("#main-grid").append(
        $("<h2>").text("Sign In"),
        $("<form>")
          .addClass("row g-3")
          .append(
            $("<div>")
              .addClass("input-group input-group-lg")
              .append(
                $("<input>").addClass("form-control").attr({
                  type: "text",
                  placeholder: "Username",
                  id: "username",
                }),
                $("<input>").addClass("form-control").attr({
                  type: "text",
                  placeholder: "Password",
                  id: "password",
                }),
                $("<button>")
                  .addClass("btn btn-primary")
                  .text("Submit")
                  .on("click", async function (event) {
                    event.preventDefault();
                    let response = await getUser(
                      $("#username").val(),
                      $("#password").val()
                    );
                    if (!response.message) {
                      $("#main-grid").empty();
                      await showUserInbox();
                    } else {
                      $("#main-grid").empty();
                      await userFlow();
                    }
                  })
              )
          )
      );
    });
  }
}

async function showUserInbox() {
  $("#main-grid").empty();

  let inputBox = new InputBox();
  inputBox.makeInputBox($("#main-grid"));

  let listGroup = new ListGroup();
  listGroup.makeListGroup($("#main-grid"));

  let listGroupItems = await listGroup.getItems();
  listGroupItems.forEach((item) => {
    let nonDOMitem = new ListGroupItem(item);
    listGroup.addItem(nonDOMitem.makeItem());
  });

  /* event listeners */

  inputBox.$randBtn.on("click", async function (event) {
    event.preventDefault();
    let response = await ListGroupItem.generateRandomItem();
    let nonDOMitem = new ListGroupItem(response);
    listGroup.addItem(nonDOMitem.makeItem());
    updateTimeSinceCreation();
  });

  inputBox.$submitBtn.on("click", async function (event) {
    event.preventDefault();
    if (inputBox.$inputField.val() === "") {
      let popover = new bootstrap.Popover(document.querySelector("input"), {
        content: "Input something...please",
        trigger: "focus",
        container: "body",
        placement: "top",
      });
      popover.show();
    } else {
      let response = await ListGroupItem.createCustomItem(
        inputBox.$inputField.val()
      );
      inputBox.$inputField.val("");
      let nonDOMitem = new ListGroupItem(response);
      listGroup.addItem(nonDOMitem.makeItem());
      updateTimeSinceCreation();
      if (document.querySelector(".popover")) {
        popover.hide();
      }
    }
  });
}

/* functions */

async function createUser(username, password) {
  let user = await fetch("/signup", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  }).then((response) => response.json());
  return user;
}

async function getUser(username, password) {
  let user = await fetch("/signin", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
    }),
  }).then((response) => response.json());
  return user;
}

async function getSession() {
  let sessionInfo = await fetch("/api/user", {
    method: "GET",
  }).then((resp) => resp.json());
  return sessionInfo["user_id"];
}

function updateTimeSinceCreation() {
  for (let i of $(".list-group").find($("small"))) {
    i.innerText = `${ListGroupItem.findDateDiff(i.dataset.iDtCreated)}`;
  }
}
