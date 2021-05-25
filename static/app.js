import { NavBar } from "./modules/nav-bar.js";
import { InputBox } from "./modules/input-box.js";
import { ListGroup } from "./modules/list-group.js";
import { ListGroupItem, data } from "./modules/list-group-item.js";

let navBar = new NavBar();
navBar.makeNavbar();

let inputBox = new InputBox();
let orderedInputBox = inputBox.makeInputField();
navBar.$gridInit.append(orderedInputBox);

let listGroup = new ListGroup();
listGroup.makeListGroup(navBar.$gridInit);

let listGroupItem = new ListGroupItem(data);
listGroup.addItem(listGroupItem.makeItem());
