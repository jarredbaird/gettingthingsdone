export class NavBar {
  constructor() {
    this.$nav = $("<nav>").addClass([
      "navbar",
      "navbar-expand-lg",
      "navbar-dark",
      "bg-primary",
    ]);
    this.$barContainer = $("<div>").addClass("container").attr("id", "main");
    this.$brand = $("<a>")
      .addClass("navbar-brand")
      .text("Getting Things Done")
      .attr("href", "/");
    this.$toggler = $("<button>").addClass("navbar-toggler").attr({
      type: "button",
      "data-bs-toggle": "collapse",
      "data-bs-target": "#navbarToggler",
      "aria-controls": "navbarToggler",
      "aria-expanded": "false",
      "aria-label": "Toggle navigation",
    });
    this.$toggleIcon = $("<span>").addClass("navbar-toggler-icon");
    this.$navbar = $("<div>")
      .addClass(["collapse", "navbar-collapse"])
      .attr("id", "navbarToggler");
    this.$menuItemList = $("<ul>").addClass("navbar-nav me-auto mb-2 mb-lg-0");
    this.$signin = $("<li>")
      .addClass("nav-item")
      .append(
        $("<a>")
          .addClass("nav-link active")
          .attr({ "aria-current": "page", id: "signin", href: "#" })
          .text("Sign In")
      );
    this.$signup = $("<li>")
      .addClass("nav-item")
      .append(
        $("<a>")
          .addClass("nav-link")
          .attr({ "aria-current": "page", id: "signup", href: "#" })
          .text("Sign Up")
      );
    this.$signout = $("<li>")
      .addClass("nav-item")
      .append(
        $("<a>")
          .addClass("nav-link")
          .attr({ "aria-current": "page", id: "signout", href: "#" })
          .text("Sign Out")
      );
    this.$connectToGmail = $("<li>")
      .addClass("nav-item")
      .append(
        $("<a>")
          .addClass("nav-link")
          .attr({
            "aria-current": "page",
            id: "gmail",
            href: "/googleoauth2callback",
          })
          .text("Connect to Gmail")
      );
    this.$menuItems = [
      this.$signin,
      this.$signup,
      this.$signout,
      this.$connectToGmail,
    ];
    this.$subNavContainer = $("<div>")
      .addClass("container p-4")
      .attr("id", "subnav");
    this.$gridInit = $("<div>").addClass("row g-3").attr("id", "main-grid");
  }

  makeNavbar($mama) {
    $mama.append(
      this.$nav.append(
        this.$barContainer.append(
          this.$brand,
          this.$toggler.append(this.$toggleIcon),
          this.$navbar.append(this.$menuItemList.append(this.$menuItems))
        )
      ),
      this.$subNavContainer.append(this.$gridInit)
    );
  }
}
