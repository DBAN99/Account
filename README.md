# 나만의 가계부 만들기

**로컬호스트에서 실행하도록 제작 (localhost = 127.0.0.1)**<br>
**mySQL을 이용한 DB 구축**<br>
**fastAPI를 이용한 서버 구축**<br>
**Insomnia를 이용해서 API를 호출 시킴 (insomnia.json 참조)**<br>
<br>

**실행법** <br>

```
git clone https://github.com/DBAN99/Account.git
cd .\Account\
pip install -r .\requirements.txt
uvicorn main:app --reload     #start server
visit  127.0.0.1:8000/
```

<br>
<br>

# 회원가입/로그인
### 회원가입
#### POST 127.0.0.1/login/register
body에 아래와 같은 형식으로 API에 요청하면 DB에 저장된다.
```
{ 
  "user_email": "user@example.com",
  "user_password": "string"
}
```
<br>
<br>

### 로그인
#### POST 127.0.0.1/login/login
body에 아래와 같은 형식으로 API에 요청하면 jwt 토큰이 발급된다.<br>
발급된 토큰을 가지고 Header에 (**Authorization : JWT 토큰**) 형식으로 요청해야지만 CRUD기능을 이용할 수 있다. <br><br>
```
{
  "login_email": "user@example.com",
  "login_password": "string"
}
```
<br>
<br>


# CRUD 기능
### 모든 요청은 반드시 login에서 발급받은 토큰을 Header에 넣고 사용한다.

### 전체 메모 리스트 조회
#### GET 127.0.0.1/crud/accountmemo
요청 시 전체 메모 리스트를 JSON형식으로 불러온다.

<br><br>

### 특정 메모 조회
#### GET 127.0.0.1/crud/accountmemo/{id}
요청 시 id값과 일치한 메모를 JSON형식으로 불러온다.

<br><br>

### 메모 작성
#### POST 127.0.0.1/crud/accountmemo
body에 아래와 같은 형식으로 API에 요청하면 DB에 내용이 저장됨 <br>
```
{
  "user_amount": "string",
  "user_memo": "string"
}
```
<br><br>

### 특정 메모 수정
#### PATCH 127.0.0.1/crud/accountmemo/{id}
body에 아래와 같은 형식으로 API에 요청하면 id값에 일치한 메모 내용을 body에 있는 내용으로 수정됨<br>
```
{
  "user_amount": "string",
  "user_memo": "string"
}
```
<br><br>

### 특정 메모 삭제
#### DELETE 127.0.0.1/crud/accountmemo/{id}
body에 아래와 같은 형식으로 API에 요청하면 id값에 일치한 메모를 삭제한다.<br>
```
{
  "memo_del": true
}
```
<br><br>

### 특정 메모 복구
#### POST 127.0.0.1/crud/accountmemo/{id}
body에 아래와 같은 형식으로 API에 요청하면 id값에 일치한 메모를 한다.<br>
```
{
  "memo_del": false
}
```
<br><br>

# 왜 이렇게 구현을 했는가?

<br> <br>

### API Router 
<br>
한 곳에 모든 API를 집어넣어 개발하는 것이 아닌 FastAPI에 존재하는 API Router 기능을 이용하여 모듈화 시킴<br>
API Router는 Flask의 블루 프린트와 동일한 기능을 가지고 있음 따라서 프로젝트를 구조적으로 관리가 가능해짐<br>

<br>
**폴더 설명**<br>
api => RESTAPI 실행 <br>
api_router => 라우터 맵핑 <br>
dbconn => DB 연결,클래스 <br>
mk_package => 기능 구현 <br>
<br>

### 회원가입/로그인

**회원가입**<br>
회원가입을 할 때에는 다른 기능 없이 그저 body에 email,password를 입력하면 그대로 DB에 저장이 되도록 구현함 <br>
이메일 중복을 피하기 위해 uniqe 설정 시 DB에서는 커밋이 되지 않는 점을 이용하여 오류가 발생하면 <br>
이메일이 중복되었다는 메세지를 보여줌으로써 이메일 중복을 막음<br>

완성된 후 데이터베이스에 이메일과 비밀번호가 암호화 되지 않고 그대로 저장되는 것을 보면서 <br>
데이터 베이스에 저장이 될 때 해시를 이용해 암호화 시킨 후 저장되도록 구현하고 싶음<br>

<br>

**로그인**<br>
로그인 기능을 토큰을 이용해서 로그인,로그아웃 상태를 나타내도록 구현함<br>
처음에는 DB 테이블에 login_active라는 column을 만들어 login API가 호출되면 True상태로 logout API가 호출 되면 False상태로 만듬 <br>
하지만 crud 부분을 호출 할 때 매번 유저 테이블을 select하는 상황이 발생하여 지속적으로 commit을 해야되는 상황 발생 <br>
리소스를 많이 잡아 먹는다고 판단하여 해당 부분을 수정하기로 생각함 <br>
이러한점을 해결하기 위해서 FastAPI 튜토리얼 Security 부분을 참고하여 token을 헤더 Authorization 부분에 집어넣어 <br>
Header 값을 받아와 인증하는 형식으로 만들면 어떨까 생각하여 현재의 로그인 형태로 제작함 <br>
로그인 시 DB에 해당 login, password가 일치하면 토큰을 만들어 사용자에게 리턴해주고 일치하지 않으면 재입력 메세지를 리턴<br>


<br>

### CRUD

**RESTAPI Method**<br>
REST API Method 규격(GET,POST,PATCH,DELETE)에 벗어나지 않도록 진행<br> 
프로젝트를 진행하면서 GET으로만 API를 구현하던 내게 다양한 메소드를 사용해보는 기회가 됨<br><br>

모든 CRUD API는 Header에 login에서 생성한 토큰을 담아 요청을 해야지만 데이터를 CRUD 할 수 있도록 만들었음 <br>
왜냐하면 login에서 생성된 토큰을 기준으로 로그인이 되었는지 안되었는지 파악하는 하나의 수단이기 때문에 해당 형태로 API를 만듬 <br>
매 요청 마다 토큰을 Decoding하여 DB에 존재하는 이메일과 비밀번호가 일치하는지 파악하면서 로그인 유무를 판단하도록 만듬<br>
초기에 했던 작업(column 생성 후 DB에 데이터 입력)하는 방식보다 오히려 효율적일 것이라고 판단하여 현재와 같은 코드로 개발 <br>
발급 받은 토큰을 body에 담아 호출하는 것이 아닌 Header라는 곳에 담아 호출을 해보면서 HTTP Header에 대한 개념을 알 수 있게 됨<br>
<br>
Del 부분은 DB에 데이터를 직접 삭제하는 것이 아닌 삭제되어있는 상태를 판단할 수 있도록 구현하여 데이터를 삭제,복구에 용이 하도록 만듬 <br>
삭제가 되어있다면 memo_del이 True 삭제가 되지 않았다면 False 형태로 저장하여 유저가 True 상태에 있는 데이터를 호출 했을 때에는 <br>
삭제된 데이터라고 알리고 False상태일 때에는 데이터 값을 출력하는 형태로 만듬<br>
<br>

GET 부분은 memo_del 값이 False 인 데이터들만 조회하는 것과 memo_id가 일치하는 특정 데이터만 조회하여 호출하는 2가지 기능을 만듬<br>
전체 조회는 user_memo, user_amount 즉 메모와 가격만 조회되어 출력되지만 <br>
특정 데이터 조회는owner_id,user_memo,user_amount,memo_id,memo_del 모든 내용을 조회하여 출력함 <br>
이렇게 만든 이유는 전체 조회는 어떤 내용을 내가 적었는지 전체적으로 보여준 것이고 <br>
특정 데이터 조회는 특정한 데이터의 모든 내용을 출력하는 것이 맞다고 판단하여 구현함<br>
<br>
POST와 PATCH 부분은 body로 받은 데이터를 직접 insert하거나 update하도록 만듬 <br>
INSERT한 데이터를 UPDATE를 통해 수정을 할 때 전체의 데이터만을 수정할 수 있도록 만듬 <br>
이 부분을 조금 더 보완하여 사용자가 기존의 데이터를 수정 할 때 자신이 원하는 부분만 수정이 되도록 기능을 만들고 싶음 <br>

<br>
CRUD에 포함되어 있는 API는 모든 구문에 토큰 값을 받아 decoding을 할 때 <br>
DB에 존재하는 데이터와 일치 하지 않거나 일정 시간(60분)이 경과 되었을 때 <br>
토큰 값이 만료되었다는 알림을 띄워 사용자에게 토큰을 재발급 받도록 유도함<br>

 
 
 
# DataBase 

### DB 테이블 register_form, account_memo

<br><br>
![Untitled (1)](https://user-images.githubusercontent.com/52847151/142620359-c4fdb455-d9ac-4bfc-8e15-c6d665516491.png)

<br><br>
```
create table account_memo
(
	owner_id int not null,
	user_memo text null,
	user_amount text null,
	memo_id int auto_increment,
	memo_del tinyint(1) default 0 not null,
	constraint account_memo_memo_id_uindex
		unique (memo_id),
	constraint owner_id
		unique (owner_id, memo_id),
	constraint account_memo_register_form_user_id_fk
		foreign key (owner_id) references register_form (user_id)
);
```

![제목 없음](https://user-images.githubusercontent.com/52847151/142620032-c89c58e0-7eaa-48af-971b-0b0f4ba070f5.png)

<br> <br> <br>

```
create table register_form
(
	user_id int auto_increment
		primary key,
	user_email varchar(255) not null,
	user_password text not null,
	constraint register_form_user_email_uindex
		unique (user_email)
);
```
 ![1234](https://user-images.githubusercontent.com/52847151/142620039-cd31e829-29d8-4569-9294-c247d2f4e53a.png)
