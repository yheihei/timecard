# Getting Started

## Start Container

```
docker compose build
docker compose up -d
```

## Migration

```
docker compose run app bash
# python -m api.migrate_db

or

docker compose run app poetry poe migrate
```

# API Doc

after `docker compose up`, see http://localhost:8000/docs

# How to test

```
docker compose run app bash
# pytest -s -p no:warnings -v

or

docker compose run app poetry poe test
```

# Formatter and check tool

```
docker compose run app poetry poe autoflake
docker compose run app poetry poe isort
docker compose run app poetry poe mypy
```

# DDDを実践する際の気付き

```
.
├── app_services  # ユースケース
│   └── clock_in
│       └── create_clock_in_app_service.py
├── auth  # 認証系。ここは FastAPI の仕組みをそのまま使いDDDしてない
├── db.py
├── domain
│   ├── models
│   │   ├── attendance_record
│   │   │   ├── attendance_record.py
│   │   │   ├── attendance_time.py
│   │   │   └── i_attendance_record.py
│   │   ├── clock_in
│   │   │   └── clock_in_record.py
│   │   └── user
│   │       ├── user.py
│   │       └── user_name.py
│   ├── services
│   │   └── clock_in
│   │       ├── clock_in_service.py
│   │       ├── exceptions.py
│   │       └── i_clock_in_service.py
│   └── shared  # いらんかも
├── infrastructure
│   └── sqlalchemy
│       └── clock_in
│           ├── clock_in_repository.py
│           └── i_clock_in_repository.py
├── main.py
├── migrate_db.py
├── models  # FastAPI+SQLAlchemyの部分
│   ├── attendance_record.py
│   ├── base.py
│   └── user.py
├── routers
│   ├── __init__.py
│   └── clock_in.py  # FastAPIのルーティング部分 ここから app_services を呼ぶ
├── schemas  # APIのリクエスト、レスポンス定義部分。routersのみが使う
│   └─── __init__.py
└── utils
    └── custom_datetime.py
```

* routersは ドメイン層の app_servicesだけを呼ぶ。結果に応じて、レスポンスを組み立てる

* app_services
    * routersに呼ばれ、APIに応じて作業をする。domain/models、domain/servicesのものを使ってやりたいことを実現する。エラーが起きたときは、専用のエラーをraiseし、routers内でそれを解釈し、レスポンスする。結果どうなったかの情報は、DTOを介して返却するが、APIレスポンスの中身には感知しない。レスポンスはFastAPI側の層にやらせるのがよいと考えている
    * ここで書かれるメソッドは抽象的なものであるべき。人が人に指示を出すような感じ
        * ダメ：XXテーブルからtype=出勤打刻の条件で出勤記録を取ってくる
        * 良い：既にその日の出勤打刻があるかどうかを確認する
* domain/models
    * ドメインモデル。エンティティ、値オブジェクトがいる。エンティティ≠テーブル定義。ビジネス側が分からない単語はここに出てきてはいけない。ビジネス側の言葉と同等かつ仕様もここに書かれるべき
* domain/services
    * ドメインサービス。ドメインモデルとinfrastructure層のリポジトリ(DAOと考えても良い)を使ってビジネスロジックを作る。アプリケーションサービスから呼ばれ、各ユースケースのやりたいことを実現する
* infrastructure
    * SQLAlchemyを使ってDBにアクセスする部分。ドメインサービスから呼ばれる。ドメインモデルを返す。SQLAlchemy固有のものを返し始めたらおかしい。ここで書かれるメソッドも抽象的なものである。RDBを使っていることを意識しないような名前になる

# ざっくり思っていること
* domain層のメソッドやコンストラクタが扱う引数は、エンティティか値オブジェクトのどれかになる。プリミティブ型をほぼ渡さない
* infrastructureをinterface化しなければいけないのは割とめんどい。が、interfaceを使っているという脳みそに切り替わるため、結果ドメインサービス層の記述が抽象化され可読性が良くなる
