export class InputBox {
  constructor() {
    this.$inputForm = $("<form>").addClass("row g-3");
    this.$btnCol = $("<div>").addClass("col-md-3");
    this.$inputCol = $("<div>").addClass("col-md-9");
    this.$inputGroup = $("<div>").addClass("input-group input-group-lg");
    this.$randBtn = $("<a>")
      .addClass("btn btn-warning btn-lg")
      .text("Go ahead, make my day");
    this.$fieldDescr = $("<span>")
      .addClass("input-group-text")
      .text("Your Task");
    this.$inputField = $("<input>")
      .addClass("form-control")
      .attr({ type: "text", placeholder: "Enter your own task here" });
    this.$submitBtn = $("<button>").addClass("btn btn-primary").text("Submit");
  }

  makeInputBox($container) {
    $container.append(
      this.$inputForm.append(
        this.$inputCol.append(
          this.$inputGroup.append(
            this.$fieldDescr,
            this.$inputField,
            this.$submitBtn
          )
        ),
        this.$btnCol.append(this.$randBtn)
      )
    );
  }
}
