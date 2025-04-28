Initial documentation for de-anonymizing programmers from executable binaries.
Original repository: https://github.com/calaylin/bda

For details see the paper: https://www.cs.drexel.edu/~greenie/caliskan-islam_when.pdf

Please cite: (bibtex entry)
@inproceedings{caliskan2018coding,
  title={When coding style survives compilation: De-anonymizing programmers from executable binaries},
  author={Caliskan, Aylin and Yamaguchi, Fabian and Dauber, Edwin and Harang, Richard and Rieck, Konrad and Greenstadt, Rachel and Narayanan, Arvind},
  booktitle={Network and Distributed System Security Symposium (NDSS) 2018},
  year={2018},
  organization={Internet Society}
}

Requirements:
1.	Bjoern https://github.com/octopus-platform/bjoern 
2.	IDA pro and hexrays https://www.hex-rays.com 
3.	Llvm* for obfuscation - ObfuscateBinaries.java https://github.com/obfuscator-llvm/obfuscator/wiki 

	∗	optional


Take binaries or if you have source code compile them.
1.	Preprocess the binary: 
      1.	Disassemble, 
              1.	BinaryDisassemble.java		
              2.	bjoernDisassemble.java

      2.	Generate abstract syntax trees, 
              1.	FeatureCalculators.java		
 
	      java -cp .:.jars/commons-exec-1.2.jar:jars/commons-io-2.6-sources.jar:jars/commons-io_2.0.1.jar:jars/commons-lang3-3.3.2.jar:jars/lingpipe-4.1.0.jar:jars/javacsv.jar:jars/weka.jar FeatureCalculators
     
      3.	Generate control flow graphs. 	
              1.	bjoernGenerateGraphmlCFG.java
	      

2.	Extract features from four data sources 
        (This produces about 700,000 features for 100 programmers each with 9 files.)  
      1.	assembly code, 
      2.	decompiled source code, 
      3.	abstract syntax trees, and 
      4.	control flow graphs. 
      
      ♣	FeatureExtractorAllFeatures.java - remove the feature types that you do not want in your feature set.
 

 		java -cp .:.jars/commons-exec-1.2.jar:jars/commons-io-2.6-sources.jar:jars/commons-io_2.0.1.jar:jars/commons-lang3-3.3.2.jar:jars/lingpipe-4.1.0.jar:jars/javacsv.jar:jars/weka.jar FeatureExtractorAllFeatures
3.	Apply information gain criterion to use to highly effective features. 
      1.	Extract features high in information gain.
              1.	AuthorClassificationBasic.java 
	      
	      
**To compile the project run the Makefile included.

*** Edit config/binary_project.conf to include all the neccessary paths
