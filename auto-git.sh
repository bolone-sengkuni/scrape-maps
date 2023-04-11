c=1
while true; do
echo -e "==============="
echo -e "GIT PUSH: $c"
echo -e "===============\n"
echo ""
git add .
git commit -m "M"
git branch -M main
git push -u origin main

c=$((c+1))
sleep 8
done