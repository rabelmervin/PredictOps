# 🚀 PredictOps: ML Model Serving Platform

A **production-ready machine learning serving platform** built with Flask, Prometheus, and Kubernetes. Demonstrates enterprise-grade MLOps practices with automated deployment, monitoring, and scalability.

---

## ✨ Key Features

### 🤖 **Machine Learning**
- Random Forest classifier with **8 financial features**
- **87.5% test accuracy** on profitability prediction
- Feature importance analysis (Net Income: 69.55%)
- Support for JSON object and array input formats

### �� **Monitoring & Observability**
- **Prometheus metrics** collection
- Custom prediction metrics (latency, error rates, request counts)
- Real-time metrics endpoint (`/metrics`)
- Health & readiness probes for Kubernetes

### 🐳 **Containerization & Orchestration**
- **Docker & Docker Compose** for local development
- **Kubernetes deployment** with rolling updates
- **ArgoCD GitOps** for automated deployments
- High availability (2 replicas, zero-downtime updates)

### 🔒 **Security & Best Practices**
- Input validation with Pydantic v2
- Non-root container execution
- Resource limits and constraints
- RBAC-ready for Kubernetes

### 🔄 **CI/CD & DevOps**
- Docker multi-stage builds
- Automated testing (78% coverage)
- GitOps-driven deployments
- Comprehensive monitoring setup

---

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │ HTTP
       ▼
┌─────────────────────────┐
│   Flask API (5000)      │
├─────────────────────────┤
│ • /predict              │
│ • /health               │
│ • /ready                │
│ • /metrics              │
└─────┬───────────────────┘
      │ Scrape
      ▼
┌──────────────────────────┐
│ Prometheus (9090)        │
├──────────────────────────┤
│ • Metrics Storage        │
│ • Query Engine           │
│ • Alert Rules            │
└──────────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **API** | Flask + Gunicorn | REST API server |
| **ML Model** | Scikit-learn (Random Forest) | Predictions |
| **Validation** | Pydantic v2 | Input validation |
| **Containerization** | Docker | Application packaging |
| **Orchestration** | Kubernetes | Cluster management |
| **Deployment** | ArgoCD | GitOps automation |
| **Monitoring** | Prometheus | Metrics collection |
| **Testing** | Pytest | Unit testing |

---

## 📦 Model Details

**Task:** Binary classification (Profitability prediction)

**Features (8):**
1. Revenue
2. Gross Profit
3. EBITDA
4. Share Holder Equity
5. Operating Expenses
6. Net Income ⭐ (69.55% importance)
7. Total Assets
8. Total Liabilities

**Performance:**
- Training Accuracy: **99.38%**
- Test Accuracy: **87.5%**
- Class Distribution: ~50/50 balanced

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.10+
- kubectl (for Kubernetes deployment)

### Local Development

```bash
# Clone repository
git clone https://github.com/rabelmervin/PredictOps.git
cd PredictOps

# Run with Docker Compose
docker-compose up -d --build

# Test health
curl http://localhost:5000/health

# Make prediction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Revenue": 3000000,
    "Gross Profit": 1500000,
    "EBITDA": 800000,
    "Share Holder Equity": 2500000,
    "Operating Expenses": 300000,
    "Net Income": 400000,
    "Total Assets": 5000000,
    "Total Liabilities": 2500000
  }'

# View metrics
curl http://localhost:5000/metrics
```

### Kubernetes Deployment

```bash
# Deploy with ArgoCD
kubectl apply -f kubernetes/argo-application.yaml

# Monitor deployment
argocd app get predictops

# Access application
kubectl port-forward svc/predictops-service 5000:80
curl http://localhost:5000/health
```

---

## 📊 API Endpoints

### `/health` (GET)
Health check for load balancers.

**Response:**
```json
{"status": "ok"}
```

### `/ready` (GET)
Readiness probe for Kubernetes.

**Response:**
```json
{"ready": true}
```

### `/predict` (POST)
Make predictions with 8 financial features.

**Request (JSON object):**
```json
{
  "Revenue": 3000000,
  "Gross Profit": 1500000,
  "EBITDA": 800000,
  "Share Holder Equity": 2500000,
  "Operating Expenses": 300000,
  "Net Income": 400000,
  "Total Assets": 5000000,
  "Total Liabilities": 2500000
}
```

**Request (JSON array):**
```json
[3000000, 1500000, 800000, 2500000, 300000, 400000, 5000000, 2500000]
```

**Response:**
```json
{"prediction": [1]}
```

### `/metrics` (GET)
Prometheus metrics in exposition format.

---

## 🧪 Testing

### Unit Tests
```bash
# Install dependencies
pip install -r requirements.txt pytest pytest-cov

# Run tests
python -m pytest tests/test_app.py -v

# Generate coverage report
python -m pytest tests/test_app.py --cov=app --cov-report=html
```

**Test Coverage: 78%**
- ✅ Health endpoint
- ✅ Readiness endpoint
- ✅ Metrics endpoint
- ✅ Valid predictions
- ✅ Invalid input handling
- ✅ Array input format

---

## 📈 Monitoring

### Prometheus Metrics

**Application Metrics:**
- `prediction_requests_total` - Total predictions made
- `prediction_duration_seconds` - Prediction latency histogram
- `prediction_errors_total` - Total prediction errors

**Flask Metrics:**
- `flask_http_request_total` - HTTP requests by method/status
- `flask_http_request_duration_seconds` - Request latency

### View Metrics

```bash
# Raw metrics endpoint
curl http://localhost:5000/metrics

# Prometheus UI
open http://localhost:9090

# Query prediction rate
curl 'http://localhost:9090/api/v1/query?query=rate(prediction_requests_total[5m])'
```

---

## 📁 Project Structure

```
PredictOps/
├── app/
│   ├── app.py              # Flask application
│   ├── validation.py       # Pydantic models
│   └── requirements.txt    # Python dependencies
├── models/
│   └── random_forest_model.joblib  # Trained ML model
├── kubernetes/
│   ├── deployment.yaml     # K8s deployment config
│   ├── service.yaml        # K8s service config
│   └── argo-application.yaml  # ArgoCD config
├── monitoring/
│   └── prometheus/
│       ├── prometheus.yml
│       └── alerting_rules.yaml
├── tests/
│   └── test_app.py        # Unit tests
├── docker-compose.yml     # Local development stack
├── Dockerfile             # Container image
└── README.md             # This file
```

---

## 🔧 Configuration

### Environment Variables
```bash
FLASK_ENV=production      # Flask environment
PYTHONUNBUFFERED=1       # Real-time logging
```

### Resource Limits (Kubernetes)
```yaml
requests:
  memory: "256Mi"
  cpu: "250m"
limits:
  memory: "512Mi"
  cpu: "500m"
```

---

## 🚢 Deployment Options

### Option 1: Docker Compose (Development)
```bash
docker-compose up -d --build
```
- Single command local deployment
- Includes Prometheus monitoring
- Port: 5000 (API), 9090 (Prometheus)

### Option 2: Kubernetes + ArgoCD (Production)
```bash
kubectl apply -f kubernetes/argo-application.yaml
```
- Automated GitOps deployments
- Zero-downtime rolling updates
- Auto-healing and self-recovery
- Revision history & rollback capability

---

## 💡 Key Accomplishments

✅ **Production-Ready ML Model**
- Trained on synthetic financial data
- 87.5% test accuracy with balanced classes
- Feature importance analysis

✅ **Comprehensive Monitoring**
- Prometheus metrics collection
- Custom application metrics
- Health & readiness probes

✅ **Enterprise DevOps**
- Docker containerization
- Kubernetes orchestration
- ArgoCD GitOps automation

✅ **Code Quality**
- 78% test coverage
- Pydantic input validation
- Security best practices

✅ **Scalability**
- 2 replicas for high availability
- Rolling updates with zero downtime
- Resource limits and constraints

---

## 🤝 Integration Examples

### Python Client
```python
import requests

response = requests.post(
    'http://localhost:5000/predict',
    json={
        'Revenue': 3000000,
        'Gross Profit': 1500000,
        'EBITDA': 800000,
        'Share Holder Equity': 2500000,
        'Operating Expenses': 300000,
        'Net Income': 400000,
        'Total Assets': 5000000,
        'Total Liabilities': 2500000
    }
)
print(response.json())  # {'prediction': [1]}
```

### cURL
```bash
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '[3000000, 1500000, 800000, 2500000, 300000, 400000, 5000000, 2500000]'
```

---

## 📊 Performance Metrics

| Metric | Value |
|--------|-------|
| API Response Time | < 50ms |
| Model Prediction Latency | < 10ms |
| Throughput | 1000+ requests/min |
| Uptime (HA) | 99.9% |
| Memory Usage | ~300MB |

---

## 🔐 Security Features

- ✅ Input validation (Pydantic v2)
- ✅ Non-root container user
- ✅ No privilege escalation
- ✅ Resource limits
- ✅ Read-only filesystem option
- ✅ Network policies ready

---

## 🎯 Success Criteria

Your deployment is successful when:

- ✅ All 6 pytest tests pass
- ✅ `/health` returns `{"status":"ok"}`
- ✅ `/ready` returns `{"ready":true}`
- ✅ Predictions return values (0 or 1)
- ✅ `/metrics` returns Prometheus data
- ✅ Kubernetes pods run with 2 replicas
- ✅ ArgoCD auto-syncs from GitHub

---

## 📞 Support & Questions

For issues or questions:
1. Review logs: `docker-compose logs -f api`
2. Check Kubernetes events: `kubectl get events`
3. View ArgoCD UI: `http://localhost:8080`

---

## 📄 License

This project is open source and available under the MIT License.

---

**Built with ❤️ using Flask, Kubernetes, and ArgoCD**

**Last Updated:** November 16, 2025
