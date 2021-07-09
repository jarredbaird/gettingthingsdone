export class SignInSignUp {
  constructor() {
    this.$signInBtn = $("<button>").addClass("btn btn-success").text("Sign In");
    this.$signUpBtn = $("<button>")
      .addClass("btn btn-primary")
      .text("Sign Up")
      .on("click", function () {
        $("#main-grid").empty();
        $("#main-grid").append(
          $("<h2>").text("Sign Up"),
          $("<form>")
            .addClass("row g-3")
            .append(
              $("<div>")
                .addClass("input-group input-group-lg")
                .append(
                  $("<input>").addClass("form-control").attr({
                    type: "text",
                    placeholder: "Username",
                    id: "username",
                  }),
                  $("<input>").addClass("form-control").attr({
                    type: "text",
                    placeholder: "Password",
                    id: "password",
                  }),
                  $("<button>")
                    .addClass("btn btn-primary")
                    .text("Submit")
                    .on("click", async function (event) {
                      event.preventDefault();
                      let response = await createUser(
                        $("#username").val(),
                        $("#password").val()
                      );
                      if (!response.message) {
                        $("#main-grid").empty();
                        await showUserInbox();
                      } else {
                        $("#main-grid").empty();
                        await userFlow();
                      }
                    })
                )
            )
        );
      });
  }
}
