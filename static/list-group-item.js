let data = {
  date: "2021-05-14 16:31:00",
  title: "Jarred's title",
  descr: "Jarred's description",
  id: "1",
};

class ListGroupItem {
  constructor(data) {
    // find the difference between the date the task was opened and now
    this.dateDiff = this.findDateDiff(data.date);

    // create list container for everything else
    this.$listItemContainer = $("<a>")
      .attr("id", data.id)
      .addClass("list-group-item list-group-item-action");

    // create the div to go in the <a>
    this.$contentDiv = $("<div>").addClass(
      "d-flex w-100 justify-content-between"
    );

    // create h5
    this.$title = $("<h5>").text(`${data.title}`);

    // create first small
    this.$timer = $("<small>").text(this.dateDiff);

    // create p
    this.$descr = $("<p>").text(`${data.descr}`);

    // create second small
    this.$littleDescr = $("<small>").text("Jarred's small text");
  }

  // 1 minute = 60000 milliseconds
  // 1 hour = 3600000 milliseconds
  // 1 day = 86400000 milliseconds
  // 1 wk = 604800000 milliseconds
  findDateDiff(date) {
    let diff = Date.now() - Date.parse(date);
    let toReturn;
    switch (true) {
      case diff < 60000:
        toReturn = `Created ${Math.round(diff / 1000)} seconds ago`;
        break;
      case diff < 3600000:
        toReturn = `Created ${Math.round(diff / 1000 / 60)} minutes ago`;
        break;
      case diff < 86400000:
        toReturn = `Created ${Math.round(diff / 1000 / (60 * 60))} hours ago`;
        break;
      case diff < 604800000:
        toReturn = `Created ${Math.round(
          diff / 1000 / (60 * 60 * 24)
        )} days ago`;
        break;
      default:
        toReturn = `Created a super long time ago`;
    }
    return toReturn;
  }

  addItem(listGroup) {
    // put it all together
    listGroup.append(
      this.$listItemContainer.append(
        this.$contentDiv.append(this.$title, this.$timer),
        this.$descr,
        this.$littleDescr
      )
    );
  }
}

let newItem = new ListGroupItem(data);
newItem.addItem($("#inbox-list"));
