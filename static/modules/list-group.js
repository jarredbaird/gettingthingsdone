export class ListGroup {
  constructor() {
    this.$group = $("<div>").addClass("list-group").attr("id", "inbox-list");
  }
  makeListGroup(container) {
    container.append(this.$group);
  }

  addItem(madeGroupItem) {
    this.$group.prepend(madeGroupItem);
  }
}
