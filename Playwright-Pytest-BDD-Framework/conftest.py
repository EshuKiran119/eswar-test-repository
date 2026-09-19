from pathlib import Path
import os, pytest, allure
from dotenv import load_dotenv
from demo_app.server import start_server
from framework.config import Settings
from framework.clients.store_client import StoreClient

pytest_plugins = ["steps.auth_steps", "steps.order_steps", "steps.ui_steps"]
load_dotenv(Path(__file__).with_name(".env"), override=False)


def pytest_addoption(parser):
    parser.addoption("--env", choices=["LOCAL", "QAT", "UAT"], default="LOCAL")
    parser.addoption("--target-url", default=None)


@pytest.fixture(scope="session")
def settings(pytestconfig):
    env = pytestconfig.getoption("--env")
    url = pytestconfig.getoption("--target-url") or os.getenv(env + "_BASE_URL")
    server = None
    if not url and env == "LOCAL":
        server = start_server()
        url = f"http://127.0.0.1:{server.server_port}"
    if not url:
        raise pytest.UsageError(f"Set {env}_BASE_URL or --target-url")
    try:
        yield Settings.load(url)
    finally:
        if server:
            server.shutdown()
            server.server_close()


@pytest.fixture(scope="session")
def credentials(pytestconfig):
    worker = getattr(pytestconfig, "workerinput", {}).get("workerid", "gw0")
    i = int(worker.removeprefix("gw")) + 1
    env = pytestconfig.getoption("--env")
    if i > 20:
        raise pytest.UsageError("At most 20 demo workers")
    name = os.getenv(f"{env}_USER_{i:02}", f"sample{i:02}" if env == "LOCAL" else "")
    password = os.getenv(
        f"{env}_PASSWORD_{i:02}", f"DemoOnly{i:02}!" if env == "LOCAL" else ""
    )
    if not name or not password:
        raise pytest.UsageError(
            "Missing synthetic credentials for selected environment/worker"
        )
    return name, password


@pytest.fixture
def api(settings):
    client = StoreClient(settings)
    try:
        yield client
    finally:
        client.close()


@pytest.fixture
def state():
    return {}


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {**browser_context_args, "viewport": {"width": 1366, "height": 900}}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    result = yield
    report = result.get_result()
    if report.when == "call" and report.failed and "page" in item.funcargs:
        page = item.funcargs["page"]
        if not page.is_closed():
            allure.attach(
                page.screenshot(full_page=True),
                name="failure",
                attachment_type=allure.attachment_type.PNG,
            )
