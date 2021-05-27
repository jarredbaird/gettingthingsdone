import { NavBar } from "./modules/nav-bar.js";
import { InputBox } from "./modules/input-box.js";
import { ListGroup } from "./modules/list-group.js";
import { ListGroupItem, data } from "./modules/list-group-item.js";

let navBar = new NavBar();
navBar.makeNavbar($("body"));
let inputBox = new InputBox();
inputBox.makeInputBox($("#main-grid"));

let listGroup = new ListGroup();
listGroup.makeListGroup(navBar.$gridInit);

debugger;
let listGroupItem = new ListGroupItem(data);
listGroup.addItem(listGroupItem.makeItem());
