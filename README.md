## 📊 Мониторинг (Loki + Grafana)

### Запуск стека мониторинга:
bash
cd monitoring
docker compose up -d


### Доступ:
- Grafana: http://161.104.18.65:3000 (логин/пароль: анонимный доступ включён)
- Loki API: http://161.104.18:3100

### Data Source:
Loki подключается автоматически через provisioning. 
Если нет — добавь вручную:
- Name: `Loki`
- URL: `http://loki:3100`

### Тест отправки лога:
```bash
curl -X POST http://localhost:3100/loki/api/v1/push \
  -H "Content-Type: application/json" \
  -d '{"streams":[{"stream":{"app":"time-server","level":"info"},"values":[["'$(date +%s)000000000'","Test log"]]}]}'

  
