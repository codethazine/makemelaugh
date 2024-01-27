# makemelaugh

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