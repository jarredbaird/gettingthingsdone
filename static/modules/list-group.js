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

  async getItems() {
    let allItems = await fetch("/api/items/all").then((resp) => resp.json());
    return allItems;
  }
}
