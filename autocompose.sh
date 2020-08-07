for i in $(seq $(expr $RANDOM % 8)); do
    echo $i
    echo '"test, and deploy your project.\n"' >> poem.h
    git add poem.h
    git commit -m "automation composer NO.$i ($(date))"
done