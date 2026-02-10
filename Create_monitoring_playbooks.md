## We need to set up playbooks for monitoring 
Pulled files from k8s-argo-monitoring

### apps/argocd-apps/k8s-monitoring.yaml the file below defines the argocd application resource.
```
Notes on what the following playbook is doing:
It also deletes all the clusters if you delete the Argo CD application (resource-finalizer)
It points to our repo for the configuration 
It deploys the resources below ti the cluster in a namespace called monitoring. Argo will create it once this is deployed.
It has auto-sync meaning it automatically updates as the github repo updates
```

```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: capstone
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/Ali0926/Platform-Engineering-Capstone-Project.git  
    targetRevision: HEAD
    path: apps/capstone
    helm:
      valueFiles:
        - values.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: monitoring
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
```

### Updated Prometheus Values.yaml file
```
prometheus:
  alertmanager:
    enabled: true  
  
  prometheus-node-exporter:
    enabled: true 
  
  kube-state-metrics:
    enabled: true  

  server:
    service:
      type: LoadBalancer
    
    extraFlags:
      - "web.enable-remote-write-receiver"

    extraScrapeConfigs: |
      # 1. Scrape the Legacy Batch System
      - job_name: 'legacy-batch-system'
        static_configs:
          - targets: ['<LEGACY_SERVER_IP>:9100'] 
        metrics_path: /metrics

      # 2. Scrape External Linux Servers
      - job_name: 'external-linux-nodes'
        static_configs:
          - targets: ['<LINUX_SERVER_1_IP>:9100', '<LINUX_SERVER_2_IP>:9100']

    persistentVolume:
      enabled: true
      storageClass: "gp3"
      size: 20Gi 

    resources:
      requests:
        cpu: 500m
        memory: 1Gi
      limits:
        cpu: 1000m
        memory: 2Gi
```
Past one:
```
/* # Prometheus (standalone) - Lab Configuration
# Chart: prometheus 27.0.0

prometheus:
  # Disable components we don't need
  alertmanager:
    enabled: false

  prometheus-pushgateway:
    enabled: false

  kube-state-metrics:
    enabled: false

  prometheus-node-exporter:
    enabled: false

  # Prometheus server
  server:
    service:
      type: LoadBalancer

    # Enable remote write receiver for Alloy/Tempo
    extraFlags:
      - "web.enable-remote-write-receiver"

    persistentVolume:
      enabled: true
      storageClass: "gp3"
      size: 10Gi

    resources:
      requests:
        cpu: 250m
        memory: 512Mi
      limits:
        cpu: 500m
        memory: 1Gi
```

### Updated Prometheus playbook book from path apps/argocd-apps/prometheus.yaml:
```
apiVersion: argoproj.io/v1alpha1
kind: Application
metadata:
  name: prometheus
  namespace: argocd
  finalizers:
    - resources-finalizer.argocd.argoproj.io
spec:
  project: default
  source:
    repoURL: https://github.com/Ali0926/Platform-Engineering-Capstone-Project.git
    targetRevision: main  
    path: apps/prometheus
    helm:
      valueFiles:
        - values.yaml
  destination:
    server: https://kubernetes.default.svc
    namespace: capstone1 #change yours to "capstone" I had to use capstone1 because I made another cluster
  syncPolicy:
    automated:
      prune: true
      selfHeal: true
    syncOptions:
      - CreateNamespace=true
      - Replace=true     
      - ApplyOutOfSyncOnly=true
```

The Dockerfile he provided:
```
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY main.py .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```




