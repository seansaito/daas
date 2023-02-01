# Dakoku-as-a-Service AI (DaaSAI)

Repo for the DaaSAI app

## Troubleshooting

---

When running `./prestart.sh` you might run into an error like:

```shell
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) no such table: user
[SQL: SELECT user.id AS user_id, user.company_code AS user_company_code, user.employee_code AS user_employee_code, user.password AS user_password, user.is_superuser AS user_is_superuser
FROM user
WHERE user.employee_code = ?
 LIMIT ? OFFSET ?]
[parameters: ('150127', 1, 0)]
(Background on this error at: https://sqlalche.me/e/14/e3q8)
```

Troubleshooting tips:
* Is the model added to app/db/base.py?
* Is the db up to date with `alembic upgrade head`?
* If the above seem okay, then you can run `alembic revision --autogenerate -m "<commit_message>"`

---

