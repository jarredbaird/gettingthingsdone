document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("#sortable").sortable();
  document.querySelector("#sortable").disableSelection();
});
document
  .querySelector("#sortable li")
  .addClass("ui-state-default col-md-3 col-sm-4 col-xs-12");
document
  .querySelector(".nostatus h4")
  .insertBefore('<i class="fa fa-circle-o"></i>', ".nostatus h4");
document
  .querySelector(".danger h4")
  .insertBefore('<i class="fa fa-exclamation-circle"></i>', ".danger h4");
document
  .querySelector(".good h4")
  .insertBefore('<i class="fa fa-check"></i>', ".good h4");
document
  .querySelector(".excellent h4")
  .insertBefore('<i class="fa fa-star"></i>', ".excellent h4");
