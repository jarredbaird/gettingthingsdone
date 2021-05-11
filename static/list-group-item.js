data = {
  date: "2021-05-10",
  title: 'Jarred\'s title',
  descr: 'Jarred\'s description',
  id: '1'
};

class ListGroupItem {

  constructor(data) {
    // find the difference between the date the task was opened and now
    this.dateDiff = this.findDateDiff(data.date);

    // create list container for everything else
    this.$listItemContainer = $(document.createElement('a'))
      .attr('id', data.id)
      .addClass("list-group-item list-group-item-action");


    // create the div to go in the <a>
    this.$contentDiv = $(document.createElement('div'))
      .addClass("d-flex w-100 justify-content-between")

    // create h5
    this.$title = $(document.createElement('h5'))
      .text(`${data.title}`);

    // create first small
    this.$timer = $(document.createElement('small'))
      .text(`${this.dateDiff} outstanding`);

    // create p
    this.$descr = $(document.createElement('p'))
      .text(`${data.descr}`);

    // create second small
    this.$s2 = $(document.createElement('small'))
      .text("Jarred's small text");

    // put it all together
    $('.list-group').append(this.$listItemContainer.append(this.$contentDiv.append(this.$title, this.$timer), this.$descr, this.$s2));

  };

  findDateDiff(date) {
    let diff = (Date.now() - Date.parse(date))
    if (diff / 1000 < 60) {
      return `${Math.round(diff/1000)} seconds`
    } else if (diff / (1000 * 3600) < 24) {
      return `${Math.round(diff/(1000*3600))} hours`
    } else {
      return "A really long time ago"
      // (1000 * 3600 * 24);
    };

  };
}