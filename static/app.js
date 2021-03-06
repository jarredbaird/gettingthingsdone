import { NavBar } from "./modules/nav-bar.js";
import { InputBox } from "./modules/input-box.js";
import { ListGroup } from "./modules/list-group.js";
import { ListGroupItem } from "./modules/list-group-item.js";
import { SignInSignUp } from "./modules/signin-signup.js";

/* DOM Rendering */

let socket = null;
let navBar = new NavBar();
navBar.makeNavbar($("body"));
navBar.$signin.on("click", function (event) {
  event.preventDefault();
  displaySignIn();
});
navBar.$signup.on("click", function (event) {
  event.preventDefault();
  displaySignUp();
});
navBar.$signout.on("click", async function (event) {
  event.preventDefault;
  await signOut();
});

await userFlow();

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
    $(`#${nonDOMitem.i_id}-btn-group`).hide();
    $(`#${nonDOMitem.i_id}-del`).hide();
    $(`#${nonDOMitem.i_id}-chk`).hide();
    $(`#${nonDOMitem.i_id}`).hover(
      function () {
        $(this).find(`#${nonDOMitem.i_id}-card-body`).removeClass("col-md-12");
        $(this).find(`#${nonDOMitem.i_id}-card-body`).addClass("col-md-10");
        $(this).find(`#${nonDOMitem.i_id}-btn-group`).show();
        $(this).find(`#${nonDOMitem.i_id}-del`).show();
        $(this).find(`#${nonDOMitem.i_id}-chk`).show();
      },
      function () {
        $(this).find(`#${nonDOMitem.i_id}-card-body`).addClass("col-md-12");
        $(this).find(`#${nonDOMitem.i_id}-card-body`).removeClass("col-md-10");
        $(this).find(`#${nonDOMitem.i_id}-btn-group`).hide();
        $(this).find(`#${nonDOMitem.i_id}-del`).hide();
        $(this).find(`#${nonDOMitem.i_id}-chk`).hide();
      }
    );
    if (nonDOMitem.$cardContainer.data("iDone")) {
      $(`#${nonDOMitem.i_id}-i-title`).wrap("<strike>");
    }
    $(`#${nonDOMitem.i_id}-chk`).on("click", async function (event) {
      await checkItem(
        event.target.parentElement.parentElement.parentElement.getAttribute(
          "id"
        )
      );
    });
    $(`#${nonDOMitem.i_id}-del`).on("click", async function (event) {
      await deleteItem(
        event.target.parentElement.parentElement.parentElement.getAttribute(
          "id"
        )
      );
    });
  });

  inputBox.$randBtn.on("click", async function (event) {
    event.preventDefault();
    let response = await ListGroupItem.generateRandomItem();
    console.log(response);
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

function updateTimeSinceCreation() {
  for (let i of $(".list-group").find($("small"))) {
    i.innerText = `${ListGroupItem.findDateDiff(i.dataset.iDtCreated)}`;
  }
}

/****** User flow ******/

async function userFlow() {
  let userSession = await getSession();
  if (userSession["user_id"]) {
    $("#signout").show();
    $("#signup").hide();
    $("#signin").hide();
    $("#gmail").show();

    if (userSession["google_refresh_token"]) {
      $("#gmail")
        .text("Connected to gmail (sorry...you can't disconnect)")
        .addClass("disabled")
        .attr("href", null);
    } else {
      $("#gmail")
        .text("Connect to Gmail")
        .removeClass("disabled")
        .attr("href", "/googleoauth2callback");
    }
    if (!socket) {
      socket = io();
    }
    socket.on("new_email_item", function (msg, cb) {
      let nonDOMitem = new ListGroupItem(msg);
      $("#inbox-list").prepend(nonDOMitem.makeItem());
      $(`#${nonDOMitem.i_id}-btn-group`).hide();
      $(`#${nonDOMitem.i_id}-del`).hide();
      $(`#${nonDOMitem.i_id}-chk`).hide();
      $(`#${nonDOMitem.i_id}`).hover(
        function () {
          $(this)
            .find(`#${nonDOMitem.i_id}-card-body`)
            .removeClass("col-md-12");
          $(this).find(`#${nonDOMitem.i_id}-card-body`).addClass("col-md-10");
          $(this).find(`#${nonDOMitem.i_id}-btn-group`).show();
          $(this).find(`#${nonDOMitem.i_id}-del`).show();
          $(this).find(`#${nonDOMitem.i_id}-chk`).show();
        },
        function () {
          $(this).find(`#${nonDOMitem.i_id}-card-body`).addClass("col-md-12");
          $(this)
            .find(`#${nonDOMitem.i_id}-card-body`)
            .removeClass("col-md-10");
          $(this).find(`#${nonDOMitem.i_id}-btn-group`).hide();
          $(this).find(`#${nonDOMitem.i_id}-del`).hide();
          $(this).find(`#${nonDOMitem.i_id}-chk`).hide();
        }
      );
      if (nonDOMitem.$cardContainer.data("iDone")) {
        $(`#${nonDOMitem.i_id}-i-title`).wrap("<strike>");
      }
      $(`#${nonDOMitem.i_id}-chk`).on("click", async function (event) {
        await checkItem(
          event.target.parentElement.parentElement.parentElement.getAttribute(
            "id"
          )
        );
      });
      $(`#${nonDOMitem.i_id}-del`).on("click", async function (event) {
        await deleteItem(
          event.target.parentElement.parentElement.parentElement.getAttribute(
            "id"
          )
        );
      });
      console.log(nonDOMitem.makeItem());
      if (cb) cb();
    });
    await showUserInbox();
  } else {
    $("#signout").hide();
    $("#signup").show();
    $("#signin").show();
    $("#gmail").hide();
    if (socket) {
      socket.disconnect();
    }
    socket = null;
    let buttons = new SignInSignUp(signIn, signUp);
    $("#main-grid").append(
      $("<div>")
        .addClass("input-group input-group-lg")
        .append(
          buttons.$signInBtn.on("click", async function (event) {
            event.preventDefault();
            displaySignIn();
          }),
          buttons.$signUpBtn.on("click", async function (event) {
            event.preventDefault();
            displaySignUp();
          })
        )
    );
  }
}

function displaySignUp() {
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
              .attr("id", "signup")
              .on("click", async function (event) {
                event.preventDefault();
                await passCreds($("#username").val(), $("#password").val());
              })
          )
      )
  );
}

function displaySignIn() {
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
              .attr("id", "signin")
              .on("click", async function (event) {
                event.preventDefault();
                await passCreds($("#username").val(), $("#password").val());
              })
          )
      )
  );
}

async function passCreds(username, password) {
  if ($("h2").text() === "Sign In") {
    await signIn(username, password);
    await userFlow();
  } else if ($("h2").text() === "Sign Up") {
    await signUp(username, password);
    await userFlow();
  }
}

async function signUp(username, password) {
  let session = await fetch("/api/session", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
      type: "signup",
    }),
  }).then((response) => response.json());
  return session;
}

async function signIn(username, password) {
  let session = await fetch("/api/session", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      username: username,
      password: password,
      type: "signin",
    }),
  }).then((response) => response.json());
  return session;
}

async function getSession() {
  let session = await fetch("/api/session", {
    method: "GET",
  }).then((resp) => resp.json());
  console.log(session);
  return session;
}

async function signOut() {
  $("#main-grid").empty();
  await fetch("api/session", { method: "HEAD" });
  await userFlow();
}

async function checkItem(i_id) {
  let checked = await fetch("api/item", {
    method: "PATCH",
    body: JSON.stringify({ i_id: i_id }),
  }).then((response) => response.json());
  if (checked["i_done"]) {
    $(`#${i_id}-i-title`).wrap("<strike>");
    $(`${i_id}`).append($("#inbox-list"));
  } else {
    $(`#${i_id}-i-title`).unwrap().prepend($("#inbox-list"));

    $(`${i_id}`).prepend($("#inbox-list"));
  }
}

async function deleteItem(i_id) {
  let deleted = await fetch("api/item", {
    method: "DELETE",
    body: JSON.stringify({ i_id: i_id }),
  }).then((response) => response.json());
  $(`#${i_id}`).remove();
}
