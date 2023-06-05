# VulnAlert
최신 취약점 알림 툴
## Branch Rule
master, develop, feature로 진행.  
feature Branch의 경우 로컬 저장.(Remote x)  
참고 사이트 : <https://gmlwjd9405.github.io/2018/05/11/types-of-git-branch.html>
## Commit Rule
제목만 규칙 지정. 나머지는 자유롭게..  
`<type>: <subject>`   
Type 규칙 :  
+ feat : 새로운 기능 추가, 기존의 기능을 요구 사항에 맞추어 수정
+ fix : 기능에 대한 버그 수정
+ chore : 패키지 매니저 수정, 그 외 기타 수정 ex) .gitignore
+ docs : 문서(주석) 수정
+ style : 코드 스타일, 포맷팅에 대한 수정
+ refactor : 기능의 변화가 아닌 코드 리팩터링 ex) 변수 이름 변경
+ test : 테스트 코드 추가/수정
+ release : 버전 릴리즈  

Subject는 보기 쉬운 커밋 내용 요약 제목.  
참고 사이트 : <https://velog.io/@jiheon/Git-Commit-message-%EA%B7%9C%EC%B9%99>
## venv 사용
가상환경 들어갈 때 : `venv\Scripts\activate.bat`  
나올 때 : `deactivate`  
설치된 pip 패키지 확인 : `pip freeze` 자세하게 확인하려면 `pip list`   
