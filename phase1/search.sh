args=("$@")
a=0
for i in "${args[@]}"; do
	if [[ $a == 0 ]] 
	then
		# echo "${i}"
		filepath=${i}
		let "a=a+1"
	else
		# echo "${i}"
		query="${query} ${i}"
	fi
done

python3 2019201044/wiki_search.py $filepath $query