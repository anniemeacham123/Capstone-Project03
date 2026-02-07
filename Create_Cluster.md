
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
```
