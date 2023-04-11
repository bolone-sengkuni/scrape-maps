c=1
while true; do
echo -e "\n==============="
echo -e "GIT PUSH: $c"
echo -e "==============="
git add .
git commit -m "M"
git branch -M main
git push -u origin main

c=$((c+1))
sleep 5
done
