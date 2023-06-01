function login() {
	var username = document.getElementById("loginUsername");
	var password = document.getElementById("loginPassword");
	var csrf = document.getElementById("csrf").value;

	if (username == "" && password == "") {
		alert("You must enter both");
	}

	var data = {
		usename: username,
		password: password,
	};

	fetch("/api/login/", {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": csrf,
		},
		body: JSON.stringify(data),
	})
		.then((result) => result.json())
		.then((response) => {
			console.log(response);
		});
}
