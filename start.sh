echo "Cloning Repo...."
if [ -z $BRANCH ]
then
  echo "Cloning main branch...."
  git clone https://github.com/bisnuray/TelecastBot /TelecastBot
else
  echo "Cloning $BRANCH branch...."
  git clone https://github.com/bisnuray/TelecastBot -b $BRANCH /TelecastBot
fi
cd /TelecastBot
pip3 install -U -r requirements.txt
echo "Starting Bot...."
python3 main.py
