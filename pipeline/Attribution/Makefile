JC = javac
JA = java

default: build-run

build-run:
	make clean && make compile

clean:
	$(RM) -r *.class

compile:
	$(JC) -cp /home/bjacobsen/ComprehensiveAttribution/bjoern-radare/bin/bjoern.jar:jars/commons-exec-1.2.jar:jars/commons-io-2.6-sources.jar:jars/commons-io_2.0.1.jar:jars/commons-lang3-3.4.jar:jars/lingpipe-4.1.0.jar:jars/javacsv.jar:jars/weka.jar -d ./ src/*.java







