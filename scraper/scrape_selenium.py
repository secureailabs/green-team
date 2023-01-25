import json

from breaker_core.common.tools_identity import ToolsIdentity
from breaker_selenium.common.system_webdriver import SystemWebdriver
from context_tiktok import ContextTiktok
from tab_manager_tiktok import TabManagerTiktok

with open('config.cfg', 'r') as file:
    config = json.load(file)

id_identity = 'identity_jaap_oosterbroek'
path_file_webdriver = "C:\\project\\green-team\\chromedriver_win32\\chromedriver.exe"
identity = ToolsIdentity.identity_load(config["path_dir_data"], id_identity)
webdriver = ToolsIdentity.webdriver_load(config["path_dir_data"], path_file_webdriver, id_identity)
handle_tiktok = SystemWebdriver.get_handle(webdriver, 0)
context = ContextTiktok("C:\\data\\team-green\\")

tm = TabManagerTiktok(config, webdriver, handle_tiktok)
list_handle = ["@aprilgrierson2", "@katiekickscancer"]
for user_handle in list_handle:
    tm.action_scrape_user(context, user_handle)




