import { mainNav as navbar } from "./nav-bar.js";

class InputGroup {
  constructor() {
    this.$inputForm = $("<form>").addClass("row g-3");
    this.$btnCol = $("<div>").addClass("col-md-3");
    this.$inputCol = $("<div>").addClass("col-md-9");
    this.$inputGroup = $("div>").addClass("input-group input-group-lg");
    this.$randBtn = $("<button>").addclass("btn btn-success");
    this.$fieldDescr = $("<span>")
      .addClass("input-group-text")
      .text("Your Task");
    this.$inputField = $("<input>")
      .addClass("form-control")
      .attr({ type: "text", placeholder: "Enter your own task here" });
    this.$submitBtn = $("<a>").addClass("btn btn-primary").text("Submit");
  }
  makeInputField($parent) {
    $parent.prepend(
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
    );
  }
  generateRandomTask() {
    fetch("/api/endpoint")
      .then((payload) => payload.json())
      .then((resp) => {
        var data = resp.data; // array of Reddit subs returned from "endpoint.js"
        console.log(JSON.stringify(data));
        var html = "<ol>";
        data.forEach(function (sub) {
          html +=
            '<a href="/axios/' + sub.path + '">' + sub.name + "</a><br />";
        });
        html += "</ol>";
        document.getElementById("list").innerHTML = html;
      })
      .catch((err) => {
        console.log("ERROR. Something went wrong.");
      });
  }
}

export let inputGroup = new InputGroup();
inputGroup.makeInputField(navbar);
