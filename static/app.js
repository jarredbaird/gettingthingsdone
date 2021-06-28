import { NavBar } from "./modules/nav-bar.js";
import { InputBox } from "./modules/input-box.js";
import { ListGroup } from "./modules/list-group.js";
import { ListGroupItem } from "./modules/list-group-item.js";

let navBar = new NavBar();
navBar.makeNavbar($("body"));

let inputBox = new InputBox();
inputBox.makeInputBox($("#main-grid"));

let listGroup = new ListGroup();
listGroup.makeListGroup(navBar.$gridInit);

let listGroupItems = await listGroup.getItems();
listGroupItems.forEach((item) => {
  let nonDOMitem = new ListGroupItem(item);
  listGroup.addItem(nonDOMitem.makeItem());
});

function updateTimeSinceCreation() {
  for (let i of $(".list-group").find($("small"))) {
    i.innerText = `${ListGroupItem.findDateDiff(i.dataset.iDtCreated)}`;
  }
}

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
