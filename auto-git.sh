c=1
while true; do
echo "GIT PUSH: $c"
git add .
git commit -m "M"
git branch -M main
git push -u origin main
c=$((c+1))
sleep 5
done