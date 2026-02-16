# System Architecture & Design

## 1. High-Level Architecture
The system follows a microservices-based architecture with separate components for Data Engineering, ML Training, Inference API, and Frontend.

## 2. Mermaid Flowchart (End-to-End System Flow)

```mermaid
graph TD
    A[User/Sales Rep] -->|Request Quote| B[Frontend UI]
    B -->|Submit Shipment Details| C[FastAPI Backend]
    
    subgraph "Data Layer"
    D[PostgreSQL Quote DB]
    E[Market Data API]
    F[Historical Win/Loss Data]
    end
    
    subgraph "ML Engine"
    G[Feature Engineering]
    H[Win Probability Model (XGBoost)]
    I[Price Optimization Model]
    J[SHAP Explainability]
    end
    
    C --> G
    G --> H
    G --> I
    H -->|Win Chance| K[Optimization Logic]
    I -->|Base Price| K
    K -->|Recommended Price + Confidence| C
    C -->|Return Quote| B
    
    F -->|Weekly Retraining| L[Model Training Pipeline]
    L -->|Update Models| H
    L -->|Update Models| I
```

## 3. Core Components

### A. Data Engineering Layer
- **Source**: Historical shipment data, External Market APIs.
- **Storage**: PostgreSQL for structured data, S3/MinIO for model artifacts.
- **Processing**: Pandas for batch processing, Airflow for orchestration.

### B. Feature Engineering
- **Shipment Features**: Weight, Volume, Distance (Haversine).
- **Market Features**: Fuel index, Carrier base rates.
- **Customer Features**: Segment, sensitivity score.

### C. Predictive ML Models
- **Win Probability**: Classification model (XGBoost) predicting `P(Win | Price)`.
- **Price Optimization**: Regression/RL model maximizing expected profit.

### D. Business Rule Engine
- **Constraints**: Minimum margin floor (e.g., 5%), Strategic account overrides.
- **Logic**: Applies final adjustments to ML output.

## 4. Deployment Strategy
- **Containerization**: Docker for all services.
- **Orchestration**: Kubernetes (K8s) for scalability.
- **Monitoring**: Prometheus + Grafana for system metrics, MLflow for model metrics.
