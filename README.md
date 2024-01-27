# makemelaugh

### Local setup
Open three terminals and:
1. Run the webapp
```
cd webapp
npm install
npm run serve
```
2. Run the node server
```
cd node-server
docker build -t node-server .
docker run -p 3000:3000 node-server
```

### Deploy to AWS
Create ECR private repo on AWS called node-server. Then run:
1. Deploy image to ECR repo:
```
export AWS_PROFILE=dariocloud
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 908339666016.dkr.ecr.us-east-1.amazonaws.com
docker build -t node-server .
docker tag node-server:latest 908339666016.dkr.ecr.us-east-1.amazonaws.com/node-server:latest
docker push 908339666016.dkr.ecr.us-east-1.amazonaws.com/node-server:latest
```
2. Create a cluster, service and task definition running on ARM64 and deploy on the AWS Console. To update, after the subsequent push commands:
```
aws ecs update-service --cluster node-server-cluster --service node-server-service --force-new-deployment
```

Note: your AWS IDs and regions may vary.
