
Create SSH Key
```
ssh-keygen -t rsa -b 2048 -f ~/.ssh/capstone-eks-key

aws ec2 import-key-pair \
  --region us-east-1 \
  --key-name capstone-eks-key \
  --public-key-material fileb://~/.ssh/capstone-eks-key.pub
```
Create Cluster
```
eksctl create cluster \
  --name capstone \
  --region us-east-1 \
  --nodes 3 \
  --node-type t3.large \
  --with-oidc \
  --ssh-access \
  --ssh-public-key capstone-eks-key \
  --managed

 eksctl create addon \
  --name aws-ebs-csi-driver \
  --cluster capstone \
  --region us-east-1
```
Configure kubectl
```
aws eks update-kubeconfig --name capstone --region us-east-1
```
Verify
```
kubectl get nodes
```
Install ArgoCD
```
kubectl create namespace argocd
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

kubectl wait --for=condition=available --timeout=300s deployment/argocd-server -n argocd
```
Get ArhoCD Password
```
kubectl -n argocd get secret argocd-initial-admin-secret -o jsonpath="{.data.password}" | base64 -d
```
Deploy Monitoring App
```
kubectl apply -f apps/argocd-apps.yaml
```
Check Sync status
```
kubectl get applications -n argocd
```
##Get Endpoints

### Grafana
```bash
kubectl get svc grafana-lb -n monitoring -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```
Default credentials: `admin` / `admin`

### FastAPI
```bash
kubectl get svc fastapi-lb -n fastapi -o jsonpath='{.status.loadBalancer.ingress[0].hostname}'
```
### ArgoCD UI
```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```
Open: https://localhost:8080
## Directory Structure

```
apps/
├── argocd-apps.yaml      # Parent App of Apps
├── argocd-apps/          # Individual ArgoCD Application manifests
├── terraform/            # EKS infrastructure
├── prometheus/           # Prometheus Helm wrapper
├── loki/                 # Loki Helm wrapper
├── grafana/              # Grafana Helm wrapper
├── tempo/                # Tempo Helm wrapper
├── k8s-monitoring/       # Alloy collectors
├── mysql/                # MySQL + exporter
├── redis/                # Redis + exporter
└── fastapi/              # Sample FastAPI app
```

