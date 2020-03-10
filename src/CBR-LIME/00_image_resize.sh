for f in *.jpg;do
	convert $f -resize 224x224^ -gravity center -crop 224x224+0+0 $f
	echo $f
done
