CONTROL=package/DEBIAN/control

all: deb clean

clean:
	rm -rf package/DEBIAN

control:
	mkdir -p package/DEBIAN
	echo 'Package: lapy' > $(CONTROL)
	echo 'Priority: optional' >> $(CONTROL)
	echo 'Section: texlive' >> $(CONTROL)
	echo 'Installed-Size:' `du -s deb/usr|sed 's/\t.*//'` >> $(CONTROL)
	echo 'Maintainer: root@laptop' >> $(CONTROL)
	echo 'Architecture: all' >> $(CONTROL)
	echo 'Version: 0.1' >> $(CONTROL)
	echo 'Depends: python3, texlive-latex-base' >> $(CONTROL)
	echo 'Provides: lapy' >> $(CONTROL)
	echo 'Conflicts: ' >> $(CONTROL)
	echo 'Replaces: ' >> $(CONTROL)
	echo 'Description: {\\LaTeX} + Python = <3' >> $(CONTROL)

conffiles:
	mkdir -p package/DEBIAN
	touch package/DEBIAN/conffiles

deb: control conffiles
	mkdir -p package/DEBIAN
	echo "#!/bin/sh" > package/DEBIAN/postinst
	echo "mktexlsr /usr/share/texlive/texmf-dist/" >> package/DEBIAN/postinst
	chmod +x package/DEBIAN/postinst
	echo "#!/bin/sh" > package/DEBIAN/postrm
	echo "mktexlsr /usr/share/texlive/texmf-dist/" >> package/DEBIAN/postrm
	chmod +x package/DEBIAN/postrm
	dpkg-deb -b package lapy.deb
