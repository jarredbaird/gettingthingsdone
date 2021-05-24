import { mainNav as navbar } from "nav-bar.js";

class ListGroup {
  constructor() {
    this.$group = $("<div>").addClass("list-group").attr("id", "inbox-list");
  }
  makeListGroup(container) {
    container.append(this.$group);
  }
}

export let inboxGroup = new ListGroup();
inboxGroup.makeListGroup(navbar.$gridInit);
