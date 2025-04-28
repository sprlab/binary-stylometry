import java.io.BufferedReader;
import java.io.*;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.Reader;
import java.util.List;

import javax.script.ScriptException;

import org.apache.commons.exec.ExecuteException;
import org.apache.commons.io.FilenameUtils;

public class bjoernDisassemble {
	
	public static final String configPath = "config/binary_project.conf";
        public static String testFolder;  
	public static String bjoernJar;  
	public static String bjoern_radareFolder;
	public static String localBin;    
        public static void readConfig(String fpath) throws IOException {
                //ClassLoader classLoader = FeatureCalculators.class.getClass().getClassLoader();
                File file = new File(fpath);
                System.out.println(file.getAbsolutePath());
                //System.out.println(classLoader.getResource(configPath));
                BufferedReader reader = new BufferedReader(new InputStreamReader(new FileInputStream(file)));
                //BufferedReader reader = new BufferedReader(new InputStreamReader(classLoader.getResourceAsStream(configPath)));
                String line = reader.readLine();
                String parts[];
                while(line != null) {
                        parts = line.split(" = ", 2);
                        switch(parts[0]) {
                                case "testFolder":
                                        testFolder = parts[1];
                                        break;
                                case "bjoernJar":
                                        bjoernJar = parts[1];
                                        break;
				case "bjoern-radare":
                                        bjoern_radareFolder = parts[1];
                                        break;
				 case "localBin":
                                        localBin = parts[1];
                                        break;
				default:
                                        //System.err.println("Invalid option: " + parts[0]);
                                        break;
                        }
                        line = reader.readLine();
                }
                reader.close();
            }

	public static void main(String[] args) throws IOException, InterruptedException, ScriptException{
	  	try { readConfig(args[0]); } catch(ArrayIndexOutOfBoundsException ex) { readConfig(configPath); }	
		String folderToProcess = testFolder;
		
		List binary_paths = Util.listBinaryFiles(folderToProcess);
		for(int i=0; i< binary_paths.size(); i++){
			disassembleWithBjoern(binary_paths.get(i).toString());			
		}
	}
	
	public static void disassembleWithBjoern(String filePath) throws IOException, InterruptedException, ScriptException{
		//disassembles binary in filePath with bjoern-radare to outdir as nodes.csv and edges.csv
		//should take filename to test each time
		//just needs the name of the directory with the authors and their binaries as an input
		//and outputs .csv files in binary file's outdir directory - disassembles with radare 
	
		File processing = new File(filePath);
		String path = FilenameUtils.getPath(filePath);
		String filename = processing.getName();
		 Runtime run = Runtime.getRuntime();
		 String outdir = File.separator + path + filename +"_bjoernDisassembly" + File.separator ;
		 File output = new File(outdir);
		 output.mkdir();
		 
       //  System.out.println("outdir: "+outdir);
        // System.out.println("filepath: "+filePath);
//         System.out.println("path: "+path);



			 String bjoern_radare_tmp=  "#!/bin/sh" +"\n"+
			 "export PATH=$PATH:" + localBin +" \n"+
					 "java -cp "
		    	   		+ bjoernJar.trim() + ":" + localBin
		    	   		+ " exporters.radare.RadareExporterMain "
		    	   		+ filePath+" "+ " -outdir "+outdir +"\n";

			
			 PrintWriter writer = new PrintWriter( bjoern_radareFolder.trim() + "/bjoern-radare2.sh");
			 writer.println(bjoern_radare_tmp);
			 writer.close();

			 Process fileProcess = run.exec(new String[]{"/bin/sh", "-c",
					  "chmod 777 "+ bjoern_radareFolder.trim() + "/bjoern-radare2.sh \n"
					 });
		  
				       fileProcess.waitFor();
				       BufferedReader br = new BufferedReader(new InputStreamReader(fileProcess.getInputStream()));
				       while(br.ready())
				           System.out.println(br.readLine());
			
		

			 Process runScript = run.exec(new String[]{"/bin/bash", "-c",
				"cd " + bjoern_radareFolder+ "  \n"
			    +"/bin/bash "+ bjoern_radareFolder.trim() + "/bjoern-radare2.sh "
			 });
			 System.out.println(filename +": Waiting for process to finish.");
			
			 runScript.waitFor();
			 int exitCode = runScript.exitValue();
			 System.out.println("Process exit code: " + exitCode); 
		     br = new BufferedReader(new InputStreamReader(runScript.getInputStream()));
		     while(br.ready())
		           System.out.println(br.readLine());
	}
}
