export let data = {
  date: "2021-05-16 16:31:00",
  title: "Jarred's title",
  descr: "Jarred's description",
  id: "1",
};

export class ListGroupItem {
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
    this.$rangeLabel = $("<label>")
      .addClass("form-label")
      .attr("for", `${data.id}`)
      .text("How pwned is this?");
    this.$sliderMain = $("<div>").addClass("slider slider-horizontal").attr({
      id: "ex19",
      type: "text",
      "data-provide": "slider",
      "data-slider-ticks": "[1, 2, 3, 4, 5]",
      "data-slider-ticks-labels":
        "['not pwned','slightly pwned', 'getting pwned', 'pretty darn pwned', 'pwned 2 the max']",
      "data-slider-min": "1",
      "data-slider-max": "3",
      "data-slider-step": "1",
      "data-slider-value": "3",
      "data-slider-tooltip": "hide",
    });
    this.$sliderTrack = $("<div>").addClass("slider-track");
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

  makeItem() {
    // put it all together
    let item = this.$listItemContainer.append(
      this.$contentDiv.append(this.$title, this.$timer),
      this.$descr,
      this.$rangeLabel,
      this.$sliderMain.append(this.$sliderTrack)
    );
    return item;
  }
}
