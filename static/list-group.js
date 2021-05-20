class ListGroup {
  constructor() {
    this.$group = $("<div>").addClass("list-group").attr("id", "inbox-list");
  }
  makeListGroup() {
    $(".row").append(this.$group);
  }
}

let inboxGroup = new ListGroup();
inboxGroup.makeListGroup();
