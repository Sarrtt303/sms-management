
![alt text](<Screenshot 2024-10-22 180222.png>)

## 1. System Components

### 1.1 Backend Services

#### API Gateway (FastAPI)
- Entry point for all client requests
- Implements rate limiting and request validation
- Routes requests to appropriate service components
- WebSocket support for real-time metrics

#### Authentication Service
- JWT token generation and validation
- Role-based access control (Admin, Operator, Viewer)
- Password hashing using bcrypt
- Token refresh mechanism
- Rate limiting for auth requests

#### Process Manager
```python
class ProcessManager:
    def start_session(self, country: str, operator: str) -> bool
    def stop_session(self, session_id: str) -> bool
    def restart_session(self, session_id: str) -> bool
    def get_session_status(self, session_id: str) -> dict
    def list_active_sessions(self) -> List[dict]
```

#### Metrics Manager
```python
class MetricsManager:
    def collect_metrics(self, country: str, operator: str) -> dict
    def calculate_success_rate(self, country: str) -> float
    def get_realtime_stats(self) -> dict
    def check_rate_limits(self, country: str) -> bool
```

#### Config Manager
```python
class ConfigManager:
    def add_country_operator(self, config: CountryOperatorConfig) -> bool
    def update_priority(self, country: str, operator: str, priority: int) -> bool
    def get_configuration(self, country: str, operator: str) -> dict
    def list_configurations(self) -> List[dict]
```

#### Alert Manager
```python
class AlertManager:
    def check_thresholds(self, metrics: dict) -> List[Alert]
    def send_telegram_notification(self, alert: Alert) -> bool
    def get_alert_history(self) -> List[dict]
```

### 1.2 Data Models

```python
class CountryOperator(BaseModel):
    country_code: str
    operator_name: str
    priority: int
    max_rate: int
    threshold: float
    active: bool

class SMSMetrics(BaseModel):
    session_id: str
    country_code: str
    operator_name: str
    messages_sent: int
    success_rate: float
    errors: List[str]
    timestamp: datetime

class Alert(BaseModel):
    severity: str
    message: str
    country_code: str
    operator_name: str
    timestamp: datetime
```

## 2. Database Schema

### 2.1 PostgreSQL Tables

```sql
CREATE TABLE country_operators (
    id SERIAL PRIMARY KEY,
    country_code VARCHAR(3),
    operator_name VARCHAR(50),
    priority INTEGER,
    max_rate INTEGER,
    threshold FLOAT,
    active BOOLEAN,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

CREATE TABLE metrics (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(50),
    country_code VARCHAR(3),
    operator_name VARCHAR(50),
    messages_sent INTEGER,
    success_rate FLOAT,
    errors JSONB,
    timestamp TIMESTAMP
);

CREATE TABLE alerts (
    id SERIAL PRIMARY KEY,
    severity VARCHAR(20),
    message TEXT,
    country_code VARCHAR(3),
    operator_name VARCHAR(50),
    timestamp TIMESTAMP
);

CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE,
    password_hash VARCHAR(255),
    role VARCHAR(20),
    created_at TIMESTAMP
);
```

### 2.2 Redis Cache Structure

```
# Rate Limiting
rate_limit:{country_code} -> {current_count, timestamp}

# Real-time Metrics
metrics:{session_id} -> {messages_sent, success_rate, errors}

# Session Status
session:{session_id} -> {status, pid, start_time}
```

## 3. API Endpoints

### 3.1 Authentication
```
POST /api/auth/login
POST /api/auth/refresh
POST /api/auth/logout
```

### 3.2 Process Management
```
GET /api/sessions
POST /api/sessions/{country}/{operator}
DELETE /api/sessions/{session_id}
PUT /api/sessions/{session_id}/restart
```

### 3.3 Metrics
```
GET /api/metrics/realtime
GET /api/metrics/{country}/{operator}
GET /api/metrics/summary
```

### 3.4 Configuration
```
GET /api/config/operators
POST /api/config/operators
PUT /api/config/operators/{id}
DELETE /api/config/operators/{id}
```

### 3.5 Alerts
```
GET /api/alerts
GET /api/alerts/history
POST /api/alerts/settings
```

## 4. Implementation Guidelines

### 4.1 Screen Session Management
```python
def create_screen_session(session_name: str, program: str, country: str, operator: str):
    command = f"screen -dmS {session_name} python {program} --country {country} --operator {operator}"
    subprocess.run(command, shell=True)

def kill_screen_session(session_name: str):
    command = f"screen -X -S {session_name} quit"
    subprocess.run(command, shell=True)
```

### 4.2 Rate Limiting Implementation
```python
async def check_rate_limit(country: str, limit: int = 10, window: int = 60):
    key = f"rate_limit:{country}"
    current = await redis.get(key)
    
    if not current:
        await redis.set(key, 1, ex=window)
        return True
    
    if int(current) >= limit:
        return False
        
    await redis.incr(key)
    return True
```

### 4.3 Alert Thresholds
```python
def check_success_rate(metrics: SMSMetrics) -> Optional[Alert]:
    if metrics.success_rate < metrics.threshold:
        return Alert(
            severity="HIGH",
            message=f"Success rate below threshold for {metrics.country_code}",
            country_code=metrics.country_code,
            operator_name=metrics.operator_name
        )
    return None
```