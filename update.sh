#!/bin/bash
if [ -f "/usr/bin/slrh" ];then
	echo "slrh already installed : update the commande"
else :
	echo "slrh installation"
	echo "#!/bin/bash" > /usr/bin/slrh
	echo "python3 /usr/bin/SLRHelper_0.1/main.py \$1" >> /usr/bin/slrh
	chmod +x /usr/bin/slrh
fi
if [ -d "/usr/bin/SLRHelper_0.1" ]; then
	rm -rf /usr/bin/SLRHelper_0.1/
fi
cp -r SLRHelper_0.1/ /usr/bin