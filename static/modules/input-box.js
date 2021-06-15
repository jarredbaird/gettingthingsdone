export class InputBox {
  constructor() {
    this.$inputForm = $("<form>").addClass("row g-3");
    this.$btnCol = $("<div>").addClass("col-md-3");
    this.$inputCol = $("<div>").addClass("col-md-9");
    this.$inputGroup = $("<div>").addClass("input-group input-group-lg");
    this.$randBtn = $("<button>")
      .addClass("btn btn-warning btn-lg")
      .text("Are you feelin' lucky, punk?")
      .on("click", function (event) {
        event.preventDefault();
        generateRandomItem();
      });
    this.$fieldDescr = $("<span>")
      .addClass("input-group-text")
      .text("Your Task");
    this.$inputField = $("<input>")
      .addClass("form-control")
      .attr({ type: "text", placeholder: "Enter your own task here" });
    this.$submitBtn = $("<a>").addClass("btn btn-primary").text("Submit");
  }

  makeInputBox($mama) {
    $mama.append(
      this.$inputForm.append(
        this.$btnCol.append(this.$randBtn),
        this.$inputCol.append(
          this.$inputGroup.append(
            this.$fieldDescr,
            this.$inputField,
            this.$submitBtn
          )
        )
      )
    )};

    async static generateRandomItem() {
      let newTitle = await fetch("/api/item/random-item").then((resp) =>
        resp.json()
      );
      return newTitle;
    }
  }
}
