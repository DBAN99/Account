# 나만의 가계부 만들기

**로컬호스트에서 실행하도록 제작 (localhost = 127.0.0.1)**<br>
**mySQL을 이용한 DB 구축**<br>
**fastAPI를 이용한 서버 구축**<br>
**도커파일이 빌드 시 안될 경우 mysql 설치 후 빌드 할 것**<br>
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

{ <br>
  "user_email": "user@example.com",<br>
  "user_password": "string"<br>
}

<br>
<br>

### 로그인
#### POST 127.0.0.1/login/login
body에 아래와 같은 형식으로 API에 요청하면 jwt 토큰이 발급된다.<br>
발급된 토큰을 가지고 Header에 (**Authorization : JWT 토큰**) 형식으로 요청해야지만 CRUD기능을 이용할 수 있다. <br><br>
{<br>
  "login_email": "user@example.com",<br>
  "login_password": "string"<br>
}<br>

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
{<br>
  "user_amount": "string",<br>
  "user_memo": "string"<br>
}
<br><br>

### 특정 메모 수정
#### PATCH 127.0.0.1/crud/accountmemo/{id}
body에 아래와 같은 형식으로 API에 요청하면 id값에 일치한 메모 내용을 body에 있는 내용으로 수정됨<br>

{<br>
  "user_amount": "string",<br>
  "user_memo": "string"<br>
}
<br><br>

### 특정 메모 삭제
#### DELETE 127.0.0.1/crud/accountmemo/{id}
body에 아래와 같은 형식으로 API에 요청하면 id값에 일치한 메모를 삭제한다.<br>

{<br>
  "memo_del": true<br>
}<br>

<br><br>

### 특정 메모 복구
#### POST 127.0.0.1/crud/accountmemo/{id}
body에 아래와 같은 형식으로 API에 요청하면 id값에 일치한 메모를 한다.<br>
{<br>
  "memo_del": true<br>
}<br>

<br><br>

# 왜 이렇게 구현을 했는가?

<br>

### 회원가입/로그인

**회원가입**<br>
회원가입을 할 때에는 다른 기능 없이 그저 body에 email,password를 입력하면 그대로 입력하게끔 구현함 <br>
보안의 취약성이 있지만 해시개념을 정확하게 파악 후 사용하는 것이 더 좋을 것이라고 판단하여 추후 추가 예정

<br>

**로그인**<br>
로그인 기능을 토큰을 이용해서 로그인,로그아웃 상태를 나타내도록 구현함<br>
처음에는 DB 테이블에 login_active라는 column을 만들어 login API가 호출되면 True상태로 logout API가 호출 되면 False상태로 만듬 <br>
crud 부분을 호출 할 때 매번 유저 테이블을 select하는 상황이 발생함 <br>
이러한 문제점을 해결하기 위해서 FastAPI 튜토리얼 Security 부분을 참고하여 token을 가지고 인증을 하면 어떨까 판단하여 현재의 로그인 API가 만들어짐<br>
진행을 하면서 JWT에 대한 개념을 파악할 수 있었고 토큰을 활용하면서 데이터를 어떻게 더 안전하게 보관 할 수 있을지 생각하게됨<br>

### CRUD
**RESTAPI Method**<br>
REST API Method 규격(GET,POST,PATCH,DELETE)에 벗어나지 않도록 진행<br> 
프로젝트를 진행하면서 GET으로만 API를 구현하던 내게 다양한 메소드를 사용해보는 기회가 됨<br>
<br>
모든 CRUD API는 Header에 login에서 생성한 토큰을 담아 요청을 해야지만 데이터를 CRUD 할 수 있도록 만들었음 <br>
왜냐하면 login에서 생성된 토큰을 기준으로 로그인이 되었는지 안되었는지 파악하는 하나의 수단이기 때문에 해당 형태로 API를 만듬 <br>
발급 받은 토큰을 body에 담아 호출하는 것이 아닌 Header라는 곳에 담아 호출을 해보면서 HTTP Header에 대한 개념을 알 수 있게 됨<br>

<br>
 
# DataBase 

### DB 테이블 register_form, account_memo

<br><br>
![Untitled (1)](https://user-images.githubusercontent.com/52847151/142620359-c4fdb455-d9ac-4bfc-8e15-c6d665516491.png)

<br><br>
create table account_memo <br>
(<br>
	owner_id int not null,<br>
	user_memo text null,<br>
	user_amount text null,<br>
	memo_id int auto_increment,<br>
	memo_del tinyint(1) default 0 not null,<br>
	constraint account_memo_memo_id_uindex<br>
		unique (memo_id),<br>
	constraint owner_id<br>
		unique (owner_id, memo_id),<br>
	constraint account_memo_register_form_user_id_fk<br>
		foreign key (owner_id) references register_form (user_id)<br>
);

![제목 없음](https://user-images.githubusercontent.com/52847151/142620032-c89c58e0-7eaa-48af-971b-0b0f4ba070f5.png)

<br> <br> <br>

create table register_form<br>
(<br>
	user_id int auto_increment<br>
		primary key,<br>
	user_email varchar(255) not null,<br>
	user_password text not null,<br>
	constraint register_form_user_email_uindex<br>
		unique (user_email)<br>
);<br>

 ![1234](https://user-images.githubusercontent.com/52847151/142620039-cd31e829-29d8-4569-9294-c247d2f4e53a.png)
