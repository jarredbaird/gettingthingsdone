export class ListGroupItem {
  constructor(data) {
    // find the difference between the date the task was opened and now
    this.dateDiff = this.findDateDiff(data.i_dt_created);

    // create list container for everything else
    this.$listItemContainer = $("<a>")
      .attr("id", data.id)
      .addClass("list-group-item list-group-item-action");

    // create the div to go in the <a>
    this.$contentDiv = $("<div>").addClass(
      "d-flex w-100 justify-content-between"
    );

    // create h5
    this.$i_title = $("<h5>").text(`${data.i_title}`);

    // create first small
    this.$timer = $("<small>").text(this.dateDiff);

    // create p
    this.$descr = $("<p>").text(`${data.i_descr}`);

    // create slider - not gonna use for now
    // this.$rangeLabel = $("<label>")
    //   .addClass("form-label")
    //   .attr("for", `${data.i_id}`)
    //   .text("How pwned is this?");
    // this.$slideRange = $("<input>")
    //   .addClass("form-range")
    //   .attr({ id: `${data.i_id}`, type: "range", min: "0", max: "5" });
    // this.$rangeDescr = $("<div>")
    //   .addClass("row px-5")
    //   .append(
    //     $("<div>").addClass("col").text("not pwned"),
    //     $("<div>").addClass("col").text("slightly pwned"),
    //     $("<div>").addClass("col").text("getting pwned"),
    //     $("<div>").addClass("col").text("pretty darn pwned"),
    //     $("<div>").addClass("col").text("pwned 2 the max")
    //   );
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
        let secDiff = Math.round(diff / 1000);
        toReturn = `Created ${secDiff} second${secDiff === 1 ? "" : "s"} ago`;
        break;
      case diff < 3600000:
        let minDiff = Math.round(diff / 1000 / 60);
        toReturn = `Created ${minDiff} minute${minDiff === 1 ? "" : "s"} ago`;
        break;
      case diff < 86400000:
        let hrDiff = Math.round(diff / 1000 / (60 * 60));
        toReturn = `Created ${hrDiff} hour${hrDiff === 1 ? "" : "s"} ago`;
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

  makeItem() {
    // put it all together
    let item = this.$listItemContainer.append(
      this.$contentDiv.append(this.$i_title, this.$timer),
      this.$descr
      // range slider is unnecessary
      // this.$rangeLabel,
      // this.$slideRange,
      // this.$rangeDescr
    );
    return item;
  }
}
