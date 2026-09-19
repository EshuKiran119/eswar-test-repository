from pytest_bdd import given, when, then, parsers


@given("an anonymous API client")
def anonymous(api):
    assert api.token is None


@given("an authenticated API customer")
def authenticated(api, credentials):
    assert api.login(*credentials).status_code == 200


@when("the customer signs in with valid demo credentials")
def valid(api, credentials, state):
    state["response"] = api.login(*credentials)


@when("the customer signs in with an incorrect password")
def invalid(api, credentials, state):
    state["response"] = api.login(credentials[0], "incorrect-demo-password")


@when("the customer signs out and replays the old token")
def replay(api, state):
    old = api.token
    assert api.logout().status_code == 204
    state["response"] = api.request(
        "GET", "/api/products", headers={"Authorization": "Bearer " + old}
    )


@then(parsers.parse("the response status is {status:d}"))
def status(state, status):
    assert state["response"].status_code == status


@then(parsers.parse('the error code is "{code}"'))
def error(state, code):
    assert state["response"].json() == {"error": code}


@then("a usable session is returned")
def session(api, state, credentials):
    data = state["response"].json()
    assert data["username"] == credentials[0]
    assert data["token"]
    assert data["expires_in"] == 300
    assert api.request("GET", "/api/products").status_code == 200
