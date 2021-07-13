export class ListGroup {
  constructor() {
    this.$group = $("<div>")
      .addClass("container bcontent")
      .attr("id", "inbox-list");
  }
  makeListGroup(container) {
    container.append(this.$group);
  }

  addItem(madeGroupItem) {
    if (madeGroupItem.data("iDone")) {
      this.$group.append(madeGroupItem);
    } else {
      this.$group.prepend(madeGroupItem);
    }
  }

  async getItems() {
    let allItems = await fetch("/api/items/all").then((resp) => resp.json());
    return allItems;
  }
}
