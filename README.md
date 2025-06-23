# fast-stock-trading

## Start/Stop App

### Start App
- Prepare a `.env` file that contains the variables as below:
1. MONGO_USER=\<your setting>
2. MONGO_PASSWORD=\<your setting>
3. MONGO_HOST=\<your setting>
4. MONGO_PORT=\<your setting>
5. MONGO_DB=\<your setting>
- Execute `docker compose --env-file .env -f docker/docker-compose.yml up`

### Stop App

- Execute `docker compose --env-file .env -f docker/docker-compose.yml down`

## Grafana

### Add connection

- Go to localhost:3000 and endter the default credential: admin/admin.
- In the left panel, find **Connections** --> **Add new connection** --> select **prometheus**.
- In the **Settings** tab, find the **Connection** section, and enter **http:http://prometheus:9090** for the Prometheus server URL.
- Click **Save & test** button in the bottom.

### Explore the data

- In the left panel, find **Explore**
- Select the metrics in the **Metric** dropdown list, you can find the metrics you have exposed.
- Click **Run query** button and give it a shot.
