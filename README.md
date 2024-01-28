# MakeMeLaugh
<img width="1257" alt="makemelaugh-cover" src="https://github.com/codethazine/makemelaugh/assets/41583025/becafa05-7316-4f13-935f-dd5c52dc72a1">
Video-chat based game with 1vs1 logics, where players try to make laugh the other person. 
Every laugh (automatically tracked through AI) makes the user loose health points.

### Local setup
Open two terminals and:
1. Run the webapp. Make sure to install Vue.
```
cd webapp
npm install
npm run dev
```
2. Run the python AI FER server. Install the requirements if needed.
```
cd server
sh downloadPretrainedModels.sh
python mainDailyco.py
```
