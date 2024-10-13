2024.03.30 
현재 셀레늄 접속하면 차단된다. 이거 ip 우회등 방법을 찾아 보고 있으면 뚫으면 코드는 사용할 수 있다.

[해결]
webdriver 아닌 것 처럼 요청하는 설정
		- options.add_argument("--disable-blink-features=AutomationControlled")