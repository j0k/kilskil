host="http://a.kilskil.com:80"


for user in $( ls user*)
do
  echo $user
  http POST $host"/users" < $user
done

for skill in $( ls skill*)
do
  echo $skill
  http POST $host"/skills" < $skill
done

for progress in $( ls progress*)
do
  echo $progress
  http POST $host"/progress" < $progress
done
